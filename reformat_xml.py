# This script parses the iTunes XML file (that is output by MusicBee) to be compatible
# with Traktor. It also adds track info for playlist folders.
import argparse
from lxml import etree

def main():
  parser = argparse.ArgumentParser(description='Parse iTunes XML file output by MusicBee for use in Traktor')
  parser.add_argument('dir', nargs='?', default='C:/Users/mowgli/Music/MusicBee/')
  args = parser.parse_args()
  parseFile(args.dir + 'iTunes Music Library.xml', args.dir + 'iTunes Music Library.reformatted.xml')

# Reads and parses XML file from inputPath and writes re-formatted XML to outputPath
def parseFile(inputPath, outputPath):
  print('Reading file... ' + inputPath)
  with open(inputPath, mode='r', encoding='UTF-8') as xmlFile:
    tree = etree.parse(xmlFile)
  root = tree.getroot()

  main = root.find('dict')
  playlistsKey = next(c for c in main.findall('key') if c.text == 'Playlists')
  playlists = playlistsKey.getnext()


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

    # Move the "Name" key-value elements to be the first child
    # e.g. <key>Name</key><string>trap</string>
    nameKey = next(k for k in keys if k.text == 'Name')
    nameKeyIndex = playlist.index(nameKey)
    playlist.insert(0, playlist[nameKeyIndex + 1]) # Move value element
    playlist.insert(0, playlist[nameKeyIndex + 1]) # Move key element

    # Determine what playlists are playlist folders (check if there are no tracks)
    playlistItems = playlist[-1]
    if len(playlistItems.findall('dict')) == 0:
      numPlaylistFolders += 1

      # Find playlist folder ID
      idKey = next(k for k in keys if k.text == 'Playlist Persistent ID')
      id = idKey.getnext().text

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
    f.write(etree.tostring(tree, encoding='UTF-8', pretty_print=True))
  print('Finished! Formatted %d playlist folders and %d playlists' % (numPlaylistFolders, len(playlists)))

if __name__ == '__main__':
  main()
