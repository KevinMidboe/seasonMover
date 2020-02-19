#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Author: KevinMidboe
# @Date:   2017-10-02 16:29:25
# @Last Modified by:   KevinMidboe
# @Last Modified time: 2018-01-15 17:18:36

try:
    from os import scandir
except ImportError:
    from scandir import scandir  # use scandir PyPI module on Python < 3.5

import env_variables as env
import multiprocessing as mp
import logging, re, datetime
from guessit import guessit

from video import VIDEO_EXTENSIONS, Episode, Movie, Video
from subtitle import SUBTITLE_EXTENSIONS, Subtitle, get_subtitle_path

logging.basicConfig(filename=env.logfile, level=logging.INFO)

""" Move to utils file """
def removeLeadingZero(number):
    stringedNumber = str(number)
    if (len(stringedNumber) > 1 and stringedNumber[0] == '0'):
        return int(stringedNumber[1:])
    return int(number)

class movie(object):
    def __init__(self, path, title=None, year=None):
        self.path = path
        self.title = title
        self.year = year

class Episode(object):
    def __init__(self, path, name, title=None, season=None, episode=None):
        super(Episode, self).__init__()
        self.path = path
        self.name = name
        self.title = title
        self.season = season
        self.episode = episode

    @classmethod
    def fromname(cls, path, name):
        title = cls.findTitle(cls, name)
        season = cls.findSeasonNumber(cls, name)
        episode = cls.findEpisodeNumber(cls, name)

        return cls(path, name, title, season, episode)

    def findTitle(self, name):
        m = re.search("([a-zA-Z0-9\'\.\-\ ])+([sS][0-9]{1,3})", name)
        if m:
           return re.sub('[\ \.]*[sS][0-9]{1,2}', '', m.group(0))

    def findSeasonNumber(self, name):
        m = re.search('[sS][0-9]{1,2}', name)
        if m:
            seasonNumber = re.sub('[sS]', '', m.group(0))
            return removeLeadingZero(seasonNumber)

    def findEpisodeNumber(self, name):        
        m = re.search('[eE][0-9]{1,3}', name)
        if m:
            episodeNumber = re.sub('[eE]', '', m.group(0))
            return removeLeadingZero(episodeNumber)

def get_tree_size(path):
    """Return total size of files in given path and subdirs."""
    total = 0
    for entry in scandir(path):
        if not ('.DS_Store' in entry.path or 'lost+found' in entry.path):
            if entry.is_dir(follow_symlinks=False):
                total += get_tree_size(entry.path)
            else:
                total += entry.stat(follow_symlinks=False).st_size
    return int(total)

def scantree(path):
    """Recursively yield DirEntry objects for given directory."""
    for entry in scandir(path):
        # Skip .DS_Store and lost+found
        # TODO have a blacklist here
    	if not ('.DS_Store' in entry.path or 'lost+found' in entry.path):
	        if entry.is_dir(follow_symlinks=False):
	            yield from scantree(entry.path)
	        else:
	        	yield entry

# Find all the mediaobjects for a given path
# TODO handle list of path's
def get_objects_for_path(path, archives=None, match=False):
    # Declare list to save the media objects found in the given path
    hashList = {}
    mediaFiles = []
    # All entries given from scantree functoin
    for entry in scantree(path):
        logging.debug('Looking at file %s', str(entry.name))
        name = entry.name # Pull out name for faster index

        # Skip if not corrent media extension
        if not (name.endswith(VIDEO_EXTENSIONS) or name.endswith(SUBTITLE_EXTENSIONS) or archives and name.endswith(ARCHIVE_EXTENSIONS)):
            continue

        # Skip if the file is a dotfile
        if name.startswith('.'):
            logging.debug('Skipping hidden file %s' % str(name))
            continue

        # If we have a video, create a class and append to mediaFiles
        if name.endswith(VIDEO_EXTENSIONS):  # video
            episode = Episode.fromname(entry.path, entry.name)
            if (episode.title is None):
                logging.debug('None found for %s' % name)
                continue
            
            title = re.sub('[\.]', ' ', episode.title)
            mediaFiles.append(episode)

    return mediaFiles

if __name__ == '__main__':
    logging.info('Started: %s' % str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")))
    import sys
    from pprint import pprint
    total = 0
    missed = 0

    # print(get_tree_size(sys.argv[1] if len(sys.argv) > 1 else '.'))
    # print(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")))
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    mediaFiles = get_objects_for_path(path)
    getTitle = lambda ep: ep.title

    for ep in mediaFiles:
        print(getTitle(ep))


    mediaList = []
    for entry in scantree(sys.argv[1] if len(sys.argv) > 1 else '.'):
        name = entry.name
        manual = Episode.fromname(entry.path, entry.name)
        size = int(entry.stat(follow_symlinks=False).st_size) / 1024 / 1024 / 1024
        # print(name + ' : ' + str(round(size, 2)) + 'GB')

        title = manual.title
        if title is None:
            logging.debug('None found for %s' % (name))
            continue

        title = re.sub('[\.]', ' ', manual.title)

        # try: 
        #     print(name + ' : ' + "%s S%iE%i" % (str(title), manual.season, manual.episode))
        # except TypeError:
        #     logging.error('Unexpected error: ' + name)

        mediaList.append(manual)
        if ('-m' in sys.argv):
            guess = guessit(name)
            
            logging.info('Manual is: {} and guess is {}'.format(title, guess['title']))
        # # if not (guess['season'] == manual.season and guess['episode'] == manual.episode):
            if (guess['title'].lower() != title.lower()):
                logging.info('Missmatch: %s by manual guess: %s : %s' % (name, guess['title'], title))
                missed += 1
            
            total += 1


    print('Total: %i, missed was: %i' % (total, missed))
    logging.info('Ended: %s' % str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")))
    logging.info(' - - - - - - - - - ')
