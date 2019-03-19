#!usr/bin/env python3.6
import click
from guessit import guessit

from core import scan_folder
from video import Video
from exceptions import InsufficientNameError

def tweet(video):
    pass

def prompt(name):
    manual_name = input("Insufficient name: '{}'\nInput name manually: ".format(name)) 

    if manual_name == 'q':
        raise  KeyboardInterrupt
    if manual_name == 's':
        return None


    return manual_name

def _moveHome(file):
    print('- - -\nMatch: \t\t {}. \nDestination:\t {}'.format(file, file.wantedFilePath()))

@click.command()
@click.argument('path')
@click.option('--daemon', '-d', is_flag=True)
@click.option('--dry', is_flag=True)
def main(path, daemon, dry):
    if dry:
        def moveHome(file): _moveHome(file)
    else:
        from core import moveHome


    videos, insufficient_name = scan_folder(path)

    for video in videos:
        moveHome(video)

    if daemon:
        print('Exiting! Daemon flag set. Insufficient name for: ', insufficient_name)
        exit(0)

    while len(insufficient_name) >= 1:
        for i, file in enumerate(insufficient_name):
            try:
                manual_name = prompt(file)
                
                if manual_name is None:
                    del insufficient_name[i]
                    continue
                
                video = Video.fromguess(file, guessit(manual_name))
                moveHome(video)
                del insufficient_name[i]

            except KeyboardInterrupt:
                # Logger: Received interrupt, exiting parser.
                # should the class objects be deleted ?
                print('Interrupt detected. Exiting')
                exit(0)
           
if __name__ == '__main__':
    main()
