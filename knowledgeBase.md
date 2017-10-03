# seasonedParser
The following is a description of the optimal flow for discovering mediafiles in a directory. 

## Table of Contents
  * [Detect changes in a directory <a name="user-content-detect-changes-in-a-directory"></a>](#detect-changes-in-a-directory-)
  * [Find the files](#find-the-files)
  * [Analyze the files](#analyze-the-files)
  * [What to do with this information](#what-to-do-with-this-information)
     * [Different ways we can say a file is interesting](#different-ways-we-can-say-a-file-is-interesting)
  * [The different ways we want to accept data](#the-different-ways-we-want-to-accept-data)
     * [Movies](#movies)
     * [Show w/ complete season folder](#show-w-complete-season-folder)
     * [Show with single episode](#show-with-single-episode)
  * [Scan vs Convert](#scan-vs-convert)
  * [Plex Local Media Assets <a name="user-content-plex-local-media-assets"></a>](#plex-local-media-assets-)
     * [Enable "Local Media Assets"](#enable-local-media-assets)
     * [Extra Subtitle Files](#extra-subtitle-files)
     * [Local Trailers and Extras](#local-trailers-and-extras)
        * [Organized in Subdirectories](#organized-in-subdirectories)
  * [Alternatives to Run-Options](#alternatives-to-run-options)
  * [Monitor End-to-End Movement of Files](#monitor-end-to-end-movement-of-files)

## Detect changes in a directory <a name='detect-changes-in-a-directory'></a>
There should be a daemon running to check for changes in the hash for a directory. 

## Find the files <a name='find-the-files'></a>
```python 
# dir = somedir
os.list(dir)
```
What information do we want:

 - Name of the files
 - Hierarchy of the files

Runtime of `os.list()` is the real problem with the system. When collecting from network drive the speed is super slow. Need a better way to get the directory contents. 

## Analyze the files <a name='analyze-the-files'></a>
Step through every file.
What information do we want:

 - What the name of the file is
 - Can use guessit (speed issue)
 - We want to know what category of file it is
 	* Movie
 	* Episode
 	* Season folder
 	* Directory
 	* Subtitles
 	* Trash files

## What to do with this information <a name='what-to-do-with-this-information'></a>
When we know it is a movie, subtitles or episode, create a object for the type.  
If it is a directory, subtitles

### Different ways we can say a file is interesting <a name='different-ways-we-can-say-a-file-is-interesting'></a>
1. If it is in a directory that has enough information
2. If it has enough information in itself to know what it is and where it belongs. 

The reason we need to check this is because if a directory:

```
Twin Peaks Season 1 1080p WEB-DL DD5.1/
├── Twin Peaks S01E01
│   ├── Twin Peaks S01E01 Pilot.en.srt
│   └── Twin Peaks S01E01 Pilot.mkv
├── Twin Peaks S01E02
│   ├── Twin Peaks S01E02 Traces to Nowhere.en.srt
│   └── Twin Peaks S01E02 Traces to Nowhere.mkv
```

What do we do here? 

 - Do we disregard the folder name and look at the files and say that we have one mediafile [.mkv] and one subtitles file [.srt] and therefore we say we have everything we need for a element.
 - Or do we look at the folder name and say say that the files inside are most likely correct and without looking at the information within the name of each  element, just rename the files based on the name of the parent folder.

If we save the parent directory file name and the information within, then if the file does not have enough information we can check with the parent folder if we can extract more information about the item. 

> Sidenote, this can be depremental if the file we are looking at is a sample or someother trash. Then we can accidentaly select a file that is unusefull to us. 

## The different ways we want to accept data <a name='the-different-ways-we-want-to-accept-data'></a>
### Movies <a name='movies'></a>
A movie that is within a folder of the same name:

```
Interstellar.2014.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1/
├── Interstellar.2014.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1.eng.srt
└── Interstellar.2014.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1.mkv
```

A movie that is standalone: 

```
Interstellar.2014.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1.mkv
```

A movie with extras: 

```
Swiss.Army.Man.2016.Bluray.1080p.TrueHD-7.1.Atmos.x264-Grym/
├── Swiss.Army.Man.2016.Bluray.1080p.TrueHD-7.1.Atmos.x264-Grym.mkv
├── Swiss.Army.Man.Extras-Grym
│   ├── Behind.the.Scenes-Grym.mkv
│   ├── Deleted.Scenes-Grym.mkv
│   ├── Making.Manny-Grym.mkv
│   └── Q.and.A.Session.with.the.Filmmakers-Grym.mkv
├── Torrent downloaded from demonoid.ph.txt
└── Torrent downloaded from......txt
```

### Show w/ complete season folder <a name='show-w-complete-season-folder'></a>
A shows complete season folder with separate folder:

```
Community.720p.1080p.WEB-DL.DD5.1.H.264/S03/
├── Community S03E01
│   └── Community S03E01 Biology 101.mkv
├── Community S03E02
│   ├── Community S03E02 Geography of Global Conflict.en.srt
│   └── Community S03E02 Geography of Global Conflict.mkv
├── Community S03E03
│   ├── Community S03E03 Competitive Ecology.en.srt
│   └── Community S03E03 Competitive Ecology.mkv
```

A shows complete season folder without separate folders:

```
Penn and Teller Fool Us S01 WEB-DL x264-FUM[ettv]
├── Penn.and.Teller.Fool.Us.S01E01.WEB-DL.x264-FUM.mp4
├── Penn.and.Teller.Fool.Us.S01E02.WEB-DL.x264-FUM.mp4
├── Penn.and.Teller.Fool.Us.S01E03.WEB-DL.x264-FUM.mp4
├── Penn.and.Teller.Fool.Us.S01E04.WEB-DL.x264-FUM.mp4
├── Penn.and.Teller.Fool.Us.S01E05.WEB-DL.x264-FUM.mp4
├── Penn.and.Teller.Fool.Us.S01E06.WEB-DL.x264-FUM.mp4
├── Penn.and.Teller.Fool.Us.S01E07.WEB-DL.x264-FUM.mp4
├── Penn.and.Teller.Fool.Us.S01E08.WEB-DL.x264-FUM.mp4
├── Penn.and.Teller.Fool.Us.S01.Special.WEB-DL.x264-FUM.mp4
└── Torrent-Downloaded-From-extratorrent.cc.txt
```

### Show with single episode <a name='show-with-single-episode'></a>
A shows episode in a separate folder:

```
Twin.Peaks.S03E17.1080p.WEB.H264-STRiFE[rarbg]/
├── RARBG.txt
├── twin.peaks.s03e17.1080p.web.h264-strife.mkv
└── twin.peaks.s03e17.1080p.web.h264-strife.nfo
```

### Other example outputs that need to be handled
```
...
Baby Driver (2017)
Room (2015)
Sample
Proof
the.house.2017.1080p.bluray.x264-geckos.sfv
the.house.2017.1080p.bluray.x264-geckos.nfo
the.house.2017.1080p.bluray.x264-geckos.jpg
Subs
The.House.2017.1080p.BluRay.x264-GECKOS[EtHD].mkv
To keep us going please read.txt
the.book.of.henry.2017.1080p.bluray.x264-geckos.sfv
the.book.of.henry.2017.1080p.bluray.x264-geckos.nfo
the.book.of.henry.2017.1080p.bluray.x264-geckos.jpg
The.Book.Of.Henry.2017.1080p.BluRay.x264-GECKOS[EtHD].mkv
```



## Plex Local Media Assets <a name='plex-local-media-assets'></a>
### Enable "Local Media Assets"
*Because I use plex and it is per date the leading platfor for multimedia library hosting we have decided to follow its naming scheme.*  
"Local Media Assets" is an Agent source that loads local media files or embedded metadata for a media item. To do this, ensure the Agent source is enabled and topmost in the list:

 * Launch the Plex Web App
 * Choose Settings from the top right of the Home screen
 * Select your Plex Media Server from the horizontal list
 * Choose Agents
 * Choose the Library Type and Agent you want to change
 * Ensure Local Media Assets is checked
 * Ensure Local Media Assets is topmost in the list

 
### Extra Subtitle Files
Several formats of subtitle files are supported and can be picked up by the Local Media Assets scanner:

* .srt
* .smi
* .ssa (or .ass)

Other formats such as VOBSUB, PGS, etc. may work on some Plex Apps but not all. If you use the Universal Transcoder, both VOBSUBS and PGS subtitles will be "burned in" during the transcoding process and shown.

Subtitle files need to be named as follows:

 * `MovieName (Release Date).[Language_Code].ext`
 * `Movies/MovieName (Release Date).[Language_Code].ext`
 * `Movies/MovieName (Release Date).[Language_Code].forced.ext`
 
### Local Trailers and Extras
If you have trailers, interviews, behind the scenes videos, or other "extras" type content for your movies, you can add those.

#### Organized in Subdirectories
You can organize your local extras into specific subdirectories inside the main directory named for the movie. Extras will be detected and used if named and stored as follows:

* `Movie/MovieName (Release Date)/Extra_Directory_Type/Descriptive_name.ext`

Where `Extra_Directory_Type` is one of:

* Behind The Scenes
* Deleted Scenes
* Featurettes
* Interviews
* Scenes
* Shorts
* Trailers

It is recommended that you provide some sort of descriptive name for the extras filenames.

```
Swiss Army Man (2016)/
├── Behind The Scenes
│   └── Behind the Scenes (Local).mkv
├── Deleted Scenes
│   └── Deleted Scenes (Local).mkv
├── Featurettes
│   ├── Making Of (Local).mkv
│   └── Q and A Session with the Filmmakers (Local).mkv
└── Swiss.Army.Man.2016.Bluray.1080p.TrueHD-7.1.Atmos.x264.mkv
```


## How to group together items
Hashes are our friend! We want to take the minimal amount of separatly identifying information and hash it to a index value. This will in effect become a hash table.  

**Movies:** Movie name and release year.  
**Shows:** Series name, season number and episode number.

```
user@hostname:/$ echo 'interstellar.2017' | sha1sum
4ecc56e9bb3d0ef4b0b48cbe14f78974ea24ab35
```

```
user@hostname:/$ echo 'new girl.2.17' | sha1sum
bb1c1339fa4211f65013f3ce36004253cc89fe04
```

> Separate items with '.'.  
> That is; '.'.join([series_name, season, episode])

> ```python
> >>> series_name='new girl'
  >>>> season=2
  >>>> episode=17
  >>>> '.'.join([series_name, str(season), str(episode)])
    'new girl.2.17'
> ```

> NB: Episode and season number should NOT have a leading 0 here!

### Hashing episode in python

```python
show = 'Rick and morty'.lower()
season = 3
for ep in range(1,10):
	itemConcat = '.'.join([show, str(season), str(ep)])
	hash_object = hashlib.sha1(str.encode(itemConcat))
	hex_dig = hash_object.hexdigest()
	print('%s : %s' % (hex_dig, itemConcat))
```

## What information should a hash index contain?
For a show item, we would hash the name of the show, season number and episode number. What information do we want to keep about a item?

#### Show episode
 - The full name of the file.
 - What show
 - Season
 - Episode
 - [Name of episode]

#### Movie
 - The full name of the file
 - Movie name
 - Year
 - Extra?

#### Subtitles
 - The full name of the file
 - Language
 - SDH?

To move the item we just need the hash, and append all the other information. 

### What we also can do with the hash/information problem
Ok, so the problem is that we really just want one class per folder. That means that having a separate subtitles goes againts this. Me reasoning for having a class pr folder type is that then everything within a hash index could have the same structure. Having everything in a single class means that we only need to do one uniform pass over our tree to execute all the operations needed (move and rename).


## Scan vs Convert <a name='scan-vs-convert'></a>
We are thinking there should be two main blobs. There should be one for the run cycle, when the new information is found, and one for the elements that have been handled. 

Wait! This would mean that we need to move the information.


## Looking up names for episodes
The tmdb api [link](https://github.com/dbr/tvdb_api) can get extended information about a episode number. 

```python
import tvdb_api
t = tvdb_api.Tvdb()
episode = t['Rick and morty'][3][4] # get season 1, episode 3 of show
print(episode['episodename']) # Print episode name
```

A large stall in the system would be to do a http call to the tvdb api to get the episode name every time we run seasoned. What we could do is when we find a episode from a series we can look for and cache all episode names that are that season for the series. 

This can be saved in the blob in the hash location for the episode. This means we can make a hash table insertion without having the episode yet. 

## How to save our information
So we have decided that to increase the search time we save each node in our library with a hash key index. Within this index we want to save the values for the node and a list of objects. These objects are all the media items that are to be present in the directory. 

### Concept: 
```bash
.
├── 1c133
└── f3ce3
    ├── this.name: New Girl
    ├── this.season: 2
    ├── this.episode: 17
    ├── [this.name of the episode]
    └── this.objects
    │   ├── episode:
    │   │   ├── full name of path
    │   └── subtitle:
    │       ├── full name of path
    │       ├── language
    │       └── SDH?
```

These database will be structured such that:  

 1. The leaf nodes will be the physcial files. 
 -  Their parents will a type object (movie | episode | subtitle)

 
A thing to notice is that choosing the structure of the database has much effect on how this parser will work. If we choose a django backend we get a lot of features, but everything will be accessed in a structure that will not be totally transparent. I hope that this will be a barebones application that will be fast and easy to run. I would be helpfull to save everything as json objects, because then we could have one key hash and all the information behind in a format that could easily be translated to objects in python. I think the simplest way to do this and still follow the original guidelines of this project we will need a sqlite3 database that has a (movie/show)_content table where we have all items' key be the hash that we want to use. Then it's variables would be it's hash values as well as other information that is the same for all elements of it's children. It would have a field that refers to a the different leaf node types *movie/show/subtitle*. How this will be saved I am not yet sure. 


## Going all inn on django!
After much consideration I think we want to go with django as our db manager. This is because we will be doing a lot of the operations from python and it is the easiest way I know of to work with databases from python. Since django lets us decide what database format we want to use, we can use sqlite3 so that our node api also easily can retrieve information from our database if needed. 

### Structure of our django app

 * ShowsItem:  
	* hash_index: char(max=200, PRIMARY KEY)
	* show_name: char(max=200)
	* season: int(2)
	* episode: int(2)
	* episode_name: char(max=200) null=True
 
* Episode:
 * path: char(max=200) 

* Subtitle:
 * path: char(max=200)
 * language: char(2)
 * sdh: boolean()



## The main parts of seasonedParse

### Parser
We need a parser that indexes a given directory and in some way finds the identifying features of a element and selects a type for the item to be.

### Inserter
When all the items have been looked at and added to a list, we want to insert all the items into our database on the hash key.

### Mover
After all the items have been added we want to commit our decisions and move the files to their correct location. 

Need to do more thinking about how it is decided when a item is in the correct location and when it has been moved. Can check that the file location matches the thing we want. But then because we haven't saved anything about the structure of the parent folders, we need to construct the wanted path every time we want to verify a item.


## Alternatives to Run-Options <a name='alternatives-to-run-options'></a>

seasoned **parse** : Looks through the saved directory and looks for mediafiles to match

 - --dry : should not commit any of the changes, just print them out.
 - --type : options *movie* | *show* for looking for a specific type of content.
 - Something to do with subtitles.
 - Something to do with looking up the name of the episode on tmdb. 

seasoned **add** : This would be how you say you want to look at a folder. 
 > This could be a interesting feature, the database does not care what the folder is, beacuse it is looking only at the leaf files. That means if we give it a single season folder or a complete root shows directory it will look for all the leafs add to database based on the names. 

seasoned **discover** : 



## Monitor End-to-End Movement of Files <a name='monitor-end-to-end-movement-of-files'></a>
Using watchdog can give us verification that something we wanted to happen acctually has happened. 

`watchdog.events.DirMovedEvent` 

If this is to be used we need a way to check the output of watchdog eventHandler very fast after we have done a action. Such actions may be, but not limited to, renaming a file, creating a directory or moving files from old dir to new.

#### Event queues and emitters
Event queue can be what we are looking at to verify that an event has happened. [link](https://pythonhosted.org/watchdog/api.html#collections) 


```
class watchdog.observers.api.EventQueue(maxsize=0)
```

Thread-safe event queue based on a special queue that skips adding the same event (FileSystemEvent) multiple times consecutively. Thus avoiding dispatching multiple event handling calls when multiple identical events are produced quicker than an observer can consume them.

```
watchdog.observers.api.EventEmitter(event_queue, watch, timeout=1)
```

Producer thread base class subclassed by event emitters that generate events and populate a queue with them. 


## As is today
### Core
```
organize_files(path):
	mediafiles = scan_files(path)
	
scan_files(path):
	checks that it is a directory and that it exsists.
	for dirpath, dirnames, filenames in os.walk(path):
		for dirname in list(dirnames):
			if dirname.startswith('.'):
				SKIP

		for filename in filenames:
			checks that it is a valid extension and doesn't start with '.'
			filepath = os.path.join(dirpath, filename)
			
			skips links and old files
			
			if filename.endswith(VIDEO_EXTENSION):
				video = scan_video(filepath)
				mediafiles.append(video)
			...
			
	return mediafiles
	
scan_video(path):
	check if it is a actual path
	dirpath, filename = os.path.split(path)
	parent_path = path.strip(path)
	# Where sanitize strips and lowers the file so it is easier to guess.
	return Video.fromguess(filename, parent_path, guessit(sanitize(path)))
	

> Now we have a list with objects, either episode, subtitle or movie. 

|-> organize_files(path):
 		for file in mediafiles:
 			hashList.setdefault(file.__hash__(),[]).append(file)

```

## Video


## Runtimes
At commit #30 we are walking through the directory with the function shown in core above. A run through The Office US of 201 episodes gives us a total runtime of 17.716. Ideas of what is slowing down the runtime:

 - Walking through the entire directory tree.
 - Checking that it is a folder that exists.
 - Guessing the episode name, number and info with the guessit library.
 - Langdetect of a subtitle file. 

```
Only scan: real    0m0.745s
Only subs: real    0m4.273s
Only videos: real    0m13.280s
```

Clearly something happening in video that takes time. 
> Also more video objects that subs

## Moving away from guessit
I wanted to check how accurate hits we could get with regex. The test is to compare the results from a simple reqex function with the output of guessit. Our code is the following:

```
def removeLeadingZero(number):
    stringedNumber = str(number)
    if (len(stringedNumber) > 1 and stringedNumber[0] == '0'):
        return int(stringedNumber[1:])
    return int(number)
    
class episode(object):
    def __init__(self, path):
        self.path = path
        self.season = self.getSeasonNumber()
        self.episode = self.getEpisodeNumber()

    def getSeasonNumber(self):
        m = re.search('[sS][0-9]{1,2}', self.path)
        if m:
            seasonNumber = re.sub('[sS]', '', m.group(0))
            return removeLeadingZero(seasonNumber)

    def getEpisodeNumber(self):
        m = re.search('[eE][0-9]{1,2}', self.path)
        if m:
            episodeNumber = re.sub('[eE]', '', m.group(0))
            return removeLeadingZero(episodeNumber)
```

With this we got: 

```
seasonedParser:$ time ./scandir.py '/mnt/mainframe/shows/'
Total: 5926, missed was: 33

real    2m3.560s
user    1m43.832s
sys     0m0.840s
```

Our main misses where episodes with multiple episodes within. Examples follow:

| Resolved | Filename | Manual guess | Reason for mismatch |
| --- | --- | --- | --- |
|[ ]| The.Office S03E24&25 - The Job [720p].mkv | 3 : 24 | Double episode |
|[ ]| Seinfeld.S07E21E22.The.Bottle.Deposit.720p.WEBrip.AAC.EN-SUB.x264-[MULVAcoded].mkv | 7 : 21 | Double episode |
|[ ]| Friends S10E17 E18.mkv | 10 : 17 | Double episode with spacing |
|[x]| S00E121.The.Seinfeld.Story.mkv | 0 : 12 | Special episode |
|[ ]| Brooklyn.Nine-Nine.S04E11-E12.The.Fugitive.Pt.1-2.1080p.WEB-DL.DD5.1.H264.mkv | 4 : 11 | Double episode |
|[ ]| Greys.Anatomy.S06E01.E02.720p.HDTV.x264.srt | 6 : 1 | Double episode |
|[ ]| Its.Always.Sunny.In.Philadelphia.S04E05E06.DSR.XviD-NoTV.avi | 4 : 5 | Multiple episode |
|[ ]| Chicago.PD.S02E20.Law.and.Order.SVU.S16E20.720p.HDTV.X264-DIMENSION[rarbg].mkv | 2 : 20 | Guessed wrong part |
|[ ]| 03x16 - The Excelsior Acquisition.avi | None | Separated by x |
|[ ]| new.girl.421.hdtv-lol.mp4 | None | No s or ep id chars


#### Excepts longer episode number 
Except longer episode number, see *S00E121*.

```
def getEpisodeNumber(self):
        m = re.search('[eE][0-9]{1,3}', self.path)
        if m:
            episodeNumber = re.sub('[eE]', '', m.group(0))
            return removeLeadingZero(episodeNumber)
```

Now we got 4 less misses

```
seasonedParser:$ time ./scandir.py '/mnt/mainframe/shows/'
Total: 5926, missed was: 29

real    2m0.766s
user    1m41.482s
sys     0m0.851s
```