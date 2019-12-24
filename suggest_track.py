# This script suggests a track based on the track name
import argparse
import sys
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from lxml import etree

def main():
  parser = argparse.ArgumentParser(description='Parse iTunes XML file output by MusicBee for use in Traktor')
  parser.add_argument('searchValue', help="the song name and optionally the artist")
  parser.add_argument('-dir', nargs='?', default='C:/Users/mowgli/Music/MusicBee/')
  args = parser.parse_args()

  inputPath = args.dir + 'iTunes Music Library.xml'
  print('\nReading file... ' + inputPath)
  collection = getCollection(inputPath)

  track = getTrack(collection, args.searchValue)
  print('Looking for matches for:')
  print(getTrackDisplayValue(track))

  suggestedTracks = getSuggestedTracks(collection, track)
  for index, track in enumerate(suggestedTracks[:10]):
    print('%d. %s' % (index + 1, getTrackDisplayValue(track)))


# Reads XML file from inputPath
def getCollection(inputPath):
  with open(inputPath, mode='r', encoding='UTF-8') as xmlFile:
    tree = etree.parse(xmlFile)
  root = tree.getroot()
  main = root.find('dict')
  return getValueOfKey(main, 'Tracks')

# Gets the value given the key
# e.g. <key>Track ID</key><value>5</value> will return 5 if passed in 'Track ID'
def getValueOfKey(dictElement, keyText):
  keys = [k for k in dictElement.findall('key') if k.text == keyText]
  if len(keys) == 0:
    return None
  return keys[0].getnext()

def getTextValueOfKey(dictElement, keyText):
  value = getValueOfKey(dictElement, keyText)
  if (value == None):
    return None
  return value.text

# Get the track details based on the track name given
def getTrack(collection, searchValue):
  tracks = collection.findall('dict')
  trackValues = [getValueOfKey(t, 'Name').text for t in tracks]
  result = process.extractOne(searchValue, trackValues, scorer=fuzz.token_sort_ratio)
  return next(t for t in tracks if getValueOfKey(t, 'Name').text == result[0])

# Returns "Artist - Song"
def getTrackDisplayValue(track):
  return getTextValueOfKey(track, 'Artist') + ' - ' + getTextValueOfKey(track, 'Name')

# Returns if key is similar
def isSimilarKey(keyOne, keyTwo):
  # TODO
  return True

# Returns tracks that have the same BPM and Key of the track searched
def getSuggestedTracks(collection, track):
  suggestedTracks = []
  trackId = getTextValueOfKey(track, 'Track ID')
  trackKey = getTextValueOfKey(track, 'Key')
  trackBpm = getTextValueOfKey(track, 'BPM')
  for t in collection.findall('dict'):
    # Don't include the same track
    if (getTextValueOfKey(t, 'Track ID') == trackId):
      continue

    score = 0
    if trackKey is not None:
      if getTextValueOfKey(t, 'Key') == trackKey:
        score += 1
    if trackBpm is not None and getTextValueOfKey(t, 'BPM') == trackBpm:
      score += 1
    if (score == 2):
      suggestedTracks.append(t)
  return suggestedTracks

if __name__ == '__main__':
  main()
