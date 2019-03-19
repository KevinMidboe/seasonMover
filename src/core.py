#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Author: KevinMidboe
# @Date:   2017-08-25 23:22:27
# @Last Modified by:   KevinMidboe
# @Last Modified time: 2019-02-02 01:04:25

from guessit import guessit
from babelfish import Language, LanguageReverseError
import hashlib
import os, errno
import shutil
import logging
import re
import tvdb_api
import click
from pprint import pprint
from titlecase import titlecase
import langdetect

import env_variables as env
from exceptions import InsufficientNameError

from video import VIDEO_EXTENSIONS, Episode, Movie, Video
from subtitle import SUBTITLE_EXTENSIONS, Subtitle, get_subtitle_path
from utils import sanitize, refine

logging.basicConfig(filename=env.logfile, level=logging.INFO)
logger = logging.getLogger('seasonedParser')
fh = logging.FileHandler(env.logfile)
fh.setLevel(logging.INFO)
sh = logging.StreamHandler()
sh.setLevel(logging.WARNING)

fh_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh_formatter = logging.Formatter('%(levelname)s: %(message)s')
fh.setFormatter(fh_formatter)
sh.setFormatter(sh_formatter)

logger.addHandler(fh)
logger.addHandler(sh)

def search_external_subtitles(path, directory=None):
    dirpath, filename = os.path.split(path)
    dirpath = dirpath or '.'
    fileroot, fileext = os.path.splitext(filename)

    subtitles = {}
    for p in os.listdir(directory or dirpath):
        if not p.endswith(SUBTITLE_EXTENSIONS):
            continue

        language = Language('und')
        language_code = p[len(fileroot):-len(os.path.splitext(p)[1])].replace(fileext, '').replace('_','-')[1:]
        if language_code:
            try:
                language = Language.fromietf(language_code)
            except (ValueError, LanguageReverseError):
                logger.error('Cannot parse language code %r', language_code)

                f = open(os.path.join(dirpath, p), 'r', encoding='ISO-8859-15')

                pattern = re.compile('[0-9:\,-<>]+')
                # head = list(islice(f.read(), 10))
                filecontent = pattern.sub('', f.read())
                filecontent = filecontent[0:1000]
                language = langdetect.detect(filecontent)
                f.close()

        subtitles[os.path.join(dirpath, p)] = language
    logger.debug('Found subtitles %r', subtitles)

    return subtitles

def find_file_size(video):
    return os.path.getsize(video.name)

def scan_video(path):
    """Scan a video from a `path`.

    :param str path: existing path to the video.
    :return: the scanned video.
    :rtype: :class:`~subliminal.video.Video`

    """
    # check for non-existing path
    if not os.path.exists(path):
        raise ValueError('Path does not exist')

    # check video extension
    if not path.endswith(VIDEO_EXTENSIONS):
        raise ValueError('%r is not a valid video extension' % os.path.splitext(path)[1])

    dirpath, filename = os.path.split(path)
    logger.info('Scanning video %r in %r', filename, dirpath)

    # guess
    video = Video.fromguess(path, guessit(path))

    video.subtitles |= set(search_external_subtitles(video.name))
    refine(video)

    # hash of name
    # if isinstance(video, Movie):
    #     if type(video.title) is str and type(video.year) is int:
    #         home_path = '{} ({})'.format(video.title, video.year)
    #         hash_str = ''.join([video.title, str(video.year) or ''])
    # elif isinstance(video, Episode):
    #     if type(video.series) is str and type(video.season) is int and type(video.episode) is int:
    #         home_path = '{} ({})'.format(video.title, video.year)
    #         hash_str = ''.join([video.series, str(video.season), str(video.episode)])
    #     video.hash = hashlib.md5(hash_str.encode()).hexdigest() 
    # except:
    #     print(video)

    return video


def scan_subtitle(path):
   if not os.path.exists(path):
      raise ValueError('Path does not exist')

   dirpath, filename = os.path.split(path)
   logger.info('Scanning subtitle %r in %r', filename, dirpath)

   # guess
   parent_path = path.strip(filename)
   subtitle = Subtitle.fromguess(parent_path, guessit(path))


   return subtitle

def subtitle_path(sibling, subtitle):
    parent_path = os.path.dirname(sibling)
    return os.path.join(parent_path, os.path.basename(subtitle))

def scan_videos(path):
    """Scan `path` for videos and their subtitles.

    See :func:`refine` to find additional information for the video.

    :param str path: existing directory path to scan.
    :return: the scanned videos.
    :rtype: list of :class:`~subliminal.video.Video`

    """
    # check for non-existing path
    if not os.path.exists(path):
        raise ValueError('Path does not exist')

    # check for non-directory path
    if not os.path.isdir(path):
        raise ValueError('Path is not a directory')

    # setup progress bar
    path_children = 0
    for _ in os.walk(path): path_children += 1
    with click.progressbar(length=path_children, show_pos=True, label='Collecting videos') as bar:

        # walk the path
        videos = []
        insufficient_name = []
        errors_path = []
        for dirpath, dirnames, filenames in os.walk(path):
            logger.debug('Walking directory %r', dirpath)

            # remove badly encoded and hidden dirnames
            for dirname in list(dirnames):
                if dirname.startswith('.'):
                    logger.debug('Skipping hidden dirname %r in %r', dirname, dirpath)
                    dirnames.remove(dirname)

            # scan for videos
            for filename in filenames:
                if not (filename.endswith(VIDEO_EXTENSIONS)):
                    logger.debug('Skipping non-video file %s', filename)
                    continue

                # skip hidden files
                if filename.startswith('.'):
                    logger.debug('Skipping hidden filename %r in %r', filename, dirpath)
                    continue

                # reconstruct the file path
                filepath = os.path.join(dirpath, filename)

                if os.path.islink(filepath):
                    logger.debug('Skipping link %r in %r', filename, dirpath)
                    continue

                # scan
                if filename.endswith(VIDEO_EXTENSIONS):  # video
                    try:
                        video = scan_video(filepath)
                    except InsufficientNameError as e:
                        logger.info(e)
                        insufficient_name.append(filepath)                        
                        continue
                    except ValueError:  # pragma: no cover
                        logger.exception('Error scanning video')
                        errors_path.append(filepath)
                        continue
                else:  # pragma: no cover
                    raise ValueError('Unsupported file %r' % filename)

                videos.append(video)

            bar.update(1)

        return videos, insufficient_name, errors_path


def organize_files(path):
   hashList = {}
   mediafiles = scan_files(path)
   # print(mediafiles)

   for file in mediafiles:
        hashList.setdefault(file.__hash__(),[]).append(file)
         # hashList[file.__hash__()] = file

   return hashList


def save_subtitles(files, single=False, directory=None, encoding=None):
    t = tvdb_api.Tvdb()

    if not isinstance(files, list):
        files = [files]

    for file in files:
        # TODO this should not be done in the loop
        dirname = "%s S%sE%s" % (file.series, "%02d" % (file.season), "%02d" % (file.episode))

        createParentfolder = not dirname in file.parent_path
        if createParentfolder:
            dirname = os.path.join(file.parent_path, dirname)
            print('Created: %s' % dirname)
            try:
                os.makedirs(dirname)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

        # TODO Clean this !
        try:
            tvdb_episode = t[file.series][file.season][file.episode]
            episode_title = tvdb_episode['episodename']
        except:
            episode_title = ''

        old = os.path.join(file.parent_path, file.name)

        if file.name.endswith(SUBTITLE_EXTENSIONS):
            lang = file.getLanguage()
            sdh = '.sdh' if file.sdh else ''
            filename = "%s S%sE%s %s%s.%s.%s" % (file.series, "%02d" % (file.season), "%02d" % (file.episode), episode_title, sdh, lang, file.container)
        else:
            filename = "%s S%sE%s %s.%s" % (file.series, "%02d" % (file.season), "%02d" % (file.episode), episode_title, file.container)

        if createParentfolder:
            newname = os.path.join(dirname, filename)
        else:
            newname = os.path.join(file.parent_path, filename)

        
        print('Moved: %s ---> %s' % (old, newname))
        os.rename(old, newname)

def scan_folder(path):
    videos = []
    insufficient_name = []
    errored_paths = []
    logger.debug('Collecting path %s', path)


    # non-existing
    if not os.path.exists(path):
        errored_paths.append(path)
        logger.exception("The path '{}' does not exist".format(path)) 

    # file
    # if path is a file
    if os.path.isfile(path):
        logger.info('Path is a file')

        try:
            video = scan_video(path)
            videos.append(video)

        except InsufficientNameError as e:
            logger.info(e)
            insufficient_name.append(path)

    # directories
    if os.path.isdir(path):
        logger.info('Path is a directory')

        scanned_videos = []
        try:
            videos, insufficient_name, errored_paths = scan_videos(path)
        except:
            logger.exception('Unexpected error while collecting directory path %s', path)
            errored_paths.append(path)

        click.echo('%s video%s collected / %s file%s with insufficient name / %s error%s' % (
        click.style(str(len(videos)), bold=True, fg='green' if videos else None),
        's' if len(videos) > 1 else '',
        click.style(str(len(insufficient_name)), bold=True, fg='yellow' if insufficient_name else None),
        's' if len(insufficient_name) > 1 else '',
        click.style(str(len(errored_paths)), bold=True, fg='red' if errored_paths else None),
        's' if len(errored_paths) > 1 else '',
    ))

    return videos, insufficient_name

def pickforgirlscouts(video):
    if video.sufficientInfo():
        video.moveLocation()
        return True

    return False

def moveHome(video):
    wantedFilePath = video.wantedFilePath()
    dir = os.path.dirname(wantedFilePath)

    if not os.path.exists(dir):
        logger.info('Creating directory {}'.format(dir))
        os.makedirs(dir)

    logger.info("Moving video file from: '{}' to: '{}'".format(video.name, wantedFilePath))
    shutil.move(video.name, wantedFilePath)
    for sub in video.subtitles:
        if not os.path.isfile(sub):
            continue
        oldpath = sub
        newpath = subtitle_path(wantedFilePath, sub) 
        logger.info("Moving subtitle file from: '{}' to: '{}'".format(oldpath, newpath))
        shutil.move(oldpath, newpath)

# Give feedback before delete ?
def empthDirectory(paths):
    pass
