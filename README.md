# MusicBee iTunes XML Parser
Tool to re-format the iTunes XML file that MusicBee outputs to be compatible with Traktor

## Why?
I strongly dislike iTunes. I think MusicBee is a great alternative. Unforuntately, as a DJ, using MusicBee is difficult because most modern DJ software only support iTunes when it comes to dynamically importing songs and playlists.

MusicBee produces an XML file that purposely replicates the "iTunes Music Library.xml" file that iTunes produces. However, it is not perfect and when importing this with Traktor, it fails for various reasons. This tool fixes this file to be compatible with Traktor.

## What exactly is being changed in the XML?
The modifications being made to the XML are actually very simple:
- Remove the XML prolog line (the first line of the file)
- Re-order the "Name" key-value element to be the first child of the playlist element
- For playlist folders, add the "Folder" element
- For playlist folders, add the list of tracks that are included in all child playlists

## Other notes
alec.tron from the MusicBee forum already made an iTunes XML parser like this, but it did not support viewing all songs of a parent folder. So this tool reverse engineers that solution and adds to it.
