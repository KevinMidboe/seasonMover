#!usr/bin/env python3.6
import click
from guessit import guessit

from core import scan_folder, moveHome 
from video import Video
from exceptions import InsufficientNameError

def moveHome(video):
    print('Would have moved: {}'.format(video))

def tweet(video):
    pass

def prompt(name):
    manual_name = input("Insufficient name: '{}'\nInput name manually: ".format(name)) 

    if manual_name == 'q':
        raise  KeyboardInterrupt
    if manual_name == 's':
        return None


    return manual_name

@click.command()
@click.argument('path')
@click.option('--daemon', '-d', daemon)
def main(path, daemon):
    videos, insufficient_name = scan_folder(path)

    for video in videos:
        moveHome(video)

    while len(insufficient_name) >= 1:
        for file in insufficient_name:
            try:
                manual_name = prompt(file)
                
                if manual_name is None:
                    insufficient_name.pop()
                    continue
                
                try:
                    video = Video.fromguess(file, guessit(manual_name))
                    moveHome(video)
                    insufficient_name.pop()

                except InsufficientNameError:
                    continue 
                    
            except KeyboardInterrupt:
                # Logger: Received interrupt, exiting parser.
                # should the class objects be deleted ?
                print('Interrupt detected. Exiting')
                exit(0)
           
if __name__ == '__main__':
    main()
