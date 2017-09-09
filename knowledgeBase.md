# seasonedGuesser
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

## Detect changes in a directory <a name='detect-changes-in-a-directory'></a>
There should be a daemon running to check for changes in the hash for a directory. 

## Find the files <a name='find-the-files'></a>
```python 
dir = somedir  
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

#### Subtitles
 - The full name of the file
 - Language
 - SDH?

To move the item we just need the hash, and append all the other information. 

## Scan vs Convert <a name='scan-vs-convert'></a>
We are thinking there should be two main blobs. There should be one for the run cycle, when the new information is found, and one for the elements that have been handled. 

Wait! This would mean that we need to move the information.


## Plex Local Media Assets <a name='plex-local-media-assets'></a>
### Enable "Local Media Assets"
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

## Alternatives to Run-Options <a name='alternatives-to-run-options'></a>

seasoned **parse** : Looks through the saved directory and looks for mediafiles to match

 - --dry : should not commit any of the changes, just print them out.
 - --type : options *movie* | *show* for looking for a specific type of content.
 - Something to do with subtitles.
 - Something to do with looking up the name of the episode on tmdb. 

seasoned **discover** : 