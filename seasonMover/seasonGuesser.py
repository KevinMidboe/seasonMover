#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: KevinMidboe
# @Date:   2017-08-25 23:22:27
# @Last Modified by:   KevinMidboe
# @Last Modified time: 2017-09-09 14:59:48

from core import organize_files, save_subtitles
from pprint import pprint

import os

def main():

  # path = '/Volumes/media/tv/Black Mirror/Black Mirror Season 01/'
  path = '/Volumes/media-1/tv/Community.720p.1080p.WEB-DL.DD5.1.H.264/S04/'
  # path = '/Volumes/media/tv/Fargo/Fargo Season 03/'
  # path = '/Volumes/media/tv/Rick and Morty/Rick and Morty Season 03/'
  # path = '/Volumes/media/movies/Interstellar.2014.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1'
  os.listdir(path)
  files = organize_files(path)

  for hashkey in files:
    # save_subtitles(files[hashkey], directory=path)
    print(files[hashkey], path)


if __name__ == '__main__':
	main()