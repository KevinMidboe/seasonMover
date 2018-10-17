#/usr/local/bin/python3
import click
import os
import logging

import env_variables as env

logging.basicConfig(filename=env.logfile, level=logging.INFO)
logger = logging.getLogger('seasonedParser')
fh = logging.FileHandler(env.logfile)
fh.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)

def listPath(path):
    if (os.path.isdir(path)):
        print('Contents of path:')
        print(os.listdir(path))

    elif os.path.isfile(path):
        print('File to parse:')
        print(path)
   
    else:
        print('Path does not exists')

def guessFromInput(video):
    print('Insufficient info for {}'.format(video.name))
    video_name = input('Input 

@click.command()
@click.argument('path')
@click.option('--greeting', '-g')
def main(path, greeting):
    logger.info('Received cli variables: \n\t path: {}'.format(path))
    listPath(path)


if __name__ == '__main__':
    main()
