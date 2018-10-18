#!usr/bin/env python3.6
from guessit import guessit
import click

from core import scan_folder, moveHome 
from video import Video
from exceptions import InsufficientInfoError

@click.command()
@click.argument('path')
def main(path):
    videos, insufficient_info = scan_folder(path)
    # print('Sweet lemonade: {} {}'.format(videos, insufficient_info))

    for video in videos:
        moveHome(video)

    while len(insufficient_info) >= 1:
        for file in insufficient_info:
            supplementary_info = input("Insufficient info for match file: '{}'\nSupplementary info: ".format(file)) 

            if supplementary_info is 'q':
                exit(0)
            if supplementary_info is 's':
                insufficient_info.pop()
                continue

            try:
                video = Video.fromguess(file, guessit(supplementary_info))
                print(video)
                moveHome(video)
                insufficient_info.pop()
            except InsufficientInfoError:
                pass
            
if __name__ == '__main__':
    main()
