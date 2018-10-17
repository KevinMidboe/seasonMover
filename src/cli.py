#!usr/bin/env python3.6

from core import scan_folder, moveHome 
from video import Video
from guessit import guessit

videos, insufficient_info = scan_folder('Spider.Man')
print('Sweet lemonade: {} {}'.format(videos, insufficient_info))

for video in videos:
    moveHome(video)

for file in insufficient_info:
    supplementary_info = input("Insufficient info for match file: '{}'\nSupplementary info: ".format(file)) 
    print(supplementary_info)
    video = Video.fromguess(file, guessit(supplementary_info))
    moveHome(video)
