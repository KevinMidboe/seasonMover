# -*- coding: utf-8 -*-
from datetime import datetime
import hashlib
import os
import logging
import re
import struct

from babelfish import Error as BabelfishError, Language
from enzyme import MalformedMKVError, MKV

def sanitize(string, ignore_characters=None):
    """Sanitize a string to strip special characters.

    :param str string: the string to sanitize.
    :param set ignore_characters: characters to ignore.
    :return: the sanitized string.
    :rtype: str

    """
    # only deal with strings
    if string is None:
        return

    ignore_characters = ignore_characters or set()

    # replace some characters with one space
    # characters = {'-', ':', '(', ')', '.'} - ignore_characters
    # if characters:
    #     string = re.sub(r'[%s]' % re.escape(''.join(characters)), ' ', string)

    # remove some characters
    characters = {'\''} - ignore_characters
    if characters:
        string = re.sub(r'[%s]' % re.escape(''.join(characters)), '', string)

    # replace multiple spaces with one
    string = re.sub(r'\s+', ' ', string)

    # strip and lower case
    return string.strip().lower()


def refine(video, embedded_subtitles=True, **kwargs):
    """Refine a video by searching its metadata.
    Several :class:`~subliminal.video.Video` attributes can be found:
      * :attr:`~subliminal.video.Video.resolution`
      * :attr:`~subliminal.video.Video.video_codec`
      * :attr:`~subliminal.video.Video.audio_codec`
      * :attr:`~subliminal.video.Video.embeded_subtitles`
    :param bool embedded_subtitles: search for embedded subtitles.
    """
    # skip non existing videos
    if not video.exists:
        return

    # check extensions
    extension = os.path.splitext(video.name)[1]
    if extension == '.mkv':
        with open(video.name, 'rb') as f:
            try:
                mkv = MKV(f)
            except MalformedMKVError:
                logging.error('Failed to parse mkv, malformed file')
                return
            except KeyError:
                logging.error('Key error while opening file, uncompatible mkv container')
                return

        # main video track
        if mkv.video_tracks:
            video_track = mkv.video_tracks[0]

            # resolution
            if video_track.height in (480, 720, 1080, 2160):
                if video_track.interlaced:
                    video.resolution = '%di' % video_track.height
                else:
                    video.resolution = '%dp' % video_track.height
                logging.debug('Found resolution %s', video.resolution)

            # video codec
            if video_track.codec_id == 'V_MPEG4/ISO/AVC':
                video.video_codec = 'h264'
                logging.debug('Found video_codec %s', video.video_codec)
            elif video_track.codec_id == 'V_MPEG4/ISO/SP':
                video.video_codec = 'DivX'
                logging.debug('Found video_codec %s', video.video_codec)
            elif video_track.codec_id == 'V_MPEG4/ISO/ASP':
                video.video_codec = 'XviD'
                logging.debug('Found video_codec %s', video.video_codec)
        else:
            logging.warning('MKV has no video track')

        # main audio track
        if mkv.audio_tracks:
            audio_track = mkv.audio_tracks[0]
            # audio codec
            if audio_track.codec_id == 'A_AC3':
                video.audio_codec = 'AC3'
                logging.debug('Found audio_codec %s', video.audio_codec)
            elif audio_track.codec_id == 'A_DTS':
                video.audio_codec = 'DTS'
                logging.debug('Found audio_codec %s', video.audio_codec)
            elif audio_track.codec_id == 'A_AAC':
                video.audio_codec = 'AAC'
                logging.debug('Found audio_codec %s', video.audio_codec)
        else:
            logging.warning('MKV has no audio track')

        # subtitle tracks
        if mkv.subtitle_tracks:
            if embedded_subtitles:
                embeded_subtitles = set()
                for st in mkv.subtitle_tracks:
                    if st.language:
                        try:
                            embeded_subtitles.add(Language.fromalpha3b(st.language))
                        except BabelfishError:
                            logging.error('Embedded subtitle track language %r is not a valid language', st.language)
                            embeded_subtitles.add(Language('und'))
                    elif st.name:
                        try:
                            embeded_subtitles.add(Language.fromname(st.name))
                        except BabelfishError:
                            logging.debug('Embedded subtitle track name %r is not a valid language', st.name)
                            embeded_subtitles.add(Language('und'))
                    else:
                        embeded_subtitles.add(Language('und'))
                logging.debug('Found embedded subtitle %r', embeded_subtitles)
                video.embeded_subtitles |= embeded_subtitles
        else:
            logging.debug('MKV has no subtitle track')
    else:
        logging.debug('Unsupported video extension %s', extension)
