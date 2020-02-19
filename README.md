# seaonedParser
seasoned Parser is python based parser that indexes a given directory for media files and identifies if it is a movie or show file and renames + moves it to a the correct place in library.

[![codecov](https://codecov.io/gh/KevinMidboe/seasonedParser/branch/master/graph/badge.svg)](https://codecov.io/gh/KevinMidboe/seasonedParser)
[![Build Status](https://drone.kevinmidboe.com/api/badges/KevinMidboe/seasonedParser/status.svg)](https://drone.kevinmidboe.com/KevinMidboe/seasonedParser)

## Table of Conents
- [Config](#config)
- [Setup for automation](#setup-for-automation)
	* [Download directory](#download-directory)

## Config <a name='config'></a>
We need to know few things about your library. This is so we know what folders to look at for new media items.


## Setup for automation <a name='setup'></a>
There are some settings that need to be set for seasonedParser to be able to find and rename new files. 

### Download directory <a name='download-directory'></a>
In your download client set a incomplete folder and a complete directory. This will allow seasonedParser to only parse items that have been completely downloaded.

*TODO:* Monitor multiple folders at the same time.  

## Run  
There are many run commands for this, but here is a list of the current working run commands for this project.

```bash
 user@host:$ ~/seasonedParser/./seasonedMover.py move 'The.Big.Bang.Theory.S11E(7..14).720p.x264.mkv' '/mnt/mainframe/shows/The Big Bang Theory/The Big Bang Theory S11E'
```

Here the first parameter is our move command, which in turn calls motherMover. The second parameter is what we want the filenames to be called. Notice the (num1..num2), this is to create a range for all the episodes we want to move. The last parameter is the path we want to move our content.
 > This will be done automatically by the parser based on the info in the media items name, but it is nice to have a manual command.


## Cli

Arguments
* Dry run with --dry
* Path variable
* daemon with -d option
  * Still need the path variable
  * Daemon sends confirmation and on missing asks tweetf or correction

Functions
* Should ask for input when missing info, always when cli


