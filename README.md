# MusicBee "iTunes.XML" Parsing Scripts
This repository contains various tools that read the XML file that MusicBee produces.

## Re-formatter
The [re-formatter tool](https://github.com/jpecht/musicbee-xml-scripts/tree/master/reformat-xml) re-formats the "iTunes Music Library.xml" file that MusicBee outputs to be compatible with Traktor.

### Why?
I strongly dislike iTunes. I think MusicBee is a great alternative. Unfortunately, as a DJ, using MusicBee is difficult because most modern DJ software only support iTunes when it comes to dynamically importing songs and playlists.

MusicBee produces an XML file that purposely replicates the "iTunes Music Library.xml" file that iTunes produces. However, it is not perfect and when importing this with Traktor, it fails for various reasons. This tool fixes this file to be compatible with Traktor.

### How to use it
1. Download
2. Run `python reformatter.py --dir [path/to/MusicBee/]` to create new XML file
3. In Traktor settings, under File Management, set "iTunes/Music Library" to point to "iTunes Music Library.reformatted.xml"
4. Repeat step 2 when playlists are updated!

### Converting to exe file
You can convert to an exe file with the following command (assuming you have pyinstaller installed):
```
pyinstaller --onefile reformat_xml.py
```

### What exactly is being changed in the XML?
The modifications being made to the XML are actually very simple:
- Re-order the "Name" key-value element to be the first child of the playlist element
- For playlist folders, add the "Folder" element
- For playlist folders, add the list of tracks that are included in all child playlists

### Caveats
- This tool was tested to work with MusicBee 3.3 and Traktor 3.2.1.
- This has not been tested with nested folders 3+ levels deep

### Other notes
alec.tron from the MusicBee forum already made an [iTunes XML parser](https://getmusicbee.com/forum/index.php?topic=25608.0) like this, but it did not support viewing the songs of a playlist folder in Traktor. So, this tool reverse engineers that solution and adds to it.
