# This scripts attempts to convert the iTunes.xml file into a TSV file
# TODO: THis isn't functional at all yet.
import argparse
from lxml import etree

def main():
  parser = argparse.ArgumentParser(description='Parse iTunes XML file output by MusicBee for use in Traktor')
  parser.add_argument('dir', nargs='?', default='C:/Users/mowgli/Music/MusicBee/')
  args = parser.parse_args()
  parseFile(args.dir + 'iTunes Music Library.xml', './output/playlists.tsv')

# Gets the value given the key
# e.g. <key>Track ID</key><value>5</value> will return 5 if passed in 'Track ID'
def getValueOfKey(dictElement, keyText):
  keys = [k for k in dictElement.findall('key') if k.text == keyText]
  if len(keys) == 0:
    return None
  return keys[0].getNext()


# Reads and parses XML file from inputPath and writes re-formatted XML to outputPath
def parseFile(inputPath, outputPath):
  print('Reading file... ' + inputPath)
  with open(inputPath, mode='r', encoding='UTF-8') as xmlFile:
    tree = etree.parse(xmlFile)
  root = tree.getroot()

  main = root.find('dict')
  tracks = getValueOfKey(main, 'Tracks')
  playlists = getValueOfKey(main, 'Playlists')

  # Gets the tag values for a track given its ID
  def getTrackInfo(id):
    d = dict()
    d.track = getValueOfKey(tracks, 'Track ID')
    d.name = getValueOfKey(track, 'Name')
    d.artist = getValueOfKey(track, 'Artist')
    d.bpm = getValueOfKey(track, 'BPM')
    d.comments = getValueOfKey(track, 'Comments')
    d.dateAdded = getValueOfKey(track, 'Date Added')
    return d


  # Returns an array of child track ids that are associated with the playlist folder
  def getChildTracks(id):
    # Find playlists that have a parent ID that matches
    trackIds = []
    for p in playlists:
      keys = p.findall('key')
      parentIdKeys = [k for k in keys if k.text == 'Parent Persistent ID']
      if (len(parentIdKeys) and parentIdKeys[0].getnext().text == id):
        playlistItemsKeys = [k for k in keys if k.text == 'Playlist Items']
        if (len(playlistItemsKeys) == 0):
          break
        valueElements = playlistItemsKeys[0].getnext().iter('integer')
        trackIds = trackIds + list(map(lambda elem: elem.text, valueElements))

    # Remove duplicates
    trackIds = list(set(trackIds))
    return trackIds


  # Loop through playlists and start
  numPlaylistFolders = 0
  for playlist in playlists:
    keys = playlist.findall('key')

    # Determine what playlists are playlist folders
    if len([k for k in keys if k.text == 'Playlist Items']) == 0:
      numPlaylistFolders += 1

      # Find playlist folder ID
      id = getValueOfKey(keys, 'Playlist Persistent ID').text

      # Add child tracks to "Playlist Items" element
      childTrackIds = getChildTracks(id)
      for trackId in childTrackIds:
        trackElement = etree.SubElement(playlistItems, 'dict')
        trackIdKey = etree.SubElement(trackElement, 'key')
        trackIdKey.text = 'Track ID'
        trackIdValue = etree.SubElement(trackElement, 'integer')
        trackIdValue.text = trackId

  # Write new XML to file
  print('Writing file... ' + outputPath)
  with open(outputPath, 'wb+') as f:
    # TODO
    f.write('hi')
  print('Finished! Output tracks for %d playlist folders' % (numPlaylistFolders, len(playlists)))

if __name__ == '__main__':
  main()
