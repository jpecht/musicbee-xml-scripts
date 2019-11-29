from io import BytesIO
from lxml import etree

tree = etree.parse('samples/iTunes Music Library.xml')
root = tree.getroot()

main = root.find('dict')
playlistsKey = next(c for c in main.findall('key') if c.text == 'Playlists')
playlists = playlistsKey.getnext()

for playlist in playlists:
	keys = playlist.findall('key')

	# Move the "Name" key-value elements to be the first child
	# e.g. <key>Name</key><string>trap</string>
	nameKey = next(k for k in keys if k.text == 'Name')
	nameKeyIndex = playlist.index(nameKey)
	playlist.insert(0, playlist[nameKeyIndex + 1]) # Move value element
	playlist.insert(0, playlist[nameKeyIndex + 1]) # Move key element

	# Determine what playlists are playlist folders
	if len([k for k in keys if k.text == 'Playlist Items']) == 0:
		# Remove empty <array></array> element
		# NOTE: This is assumed to be the last child element
		del playlist[-1]

		# Add "Folder" key-value element
		# e.g. <key>Folder</key><true/>
		folderKey = etree.SubElement(playlist, 'key')
		folderKey.text = 'Folder'
		etree.SubElement(playlist, 'true')

		# Add "Playlist Items"
		playlistItemsKey = etree.SubElement(playlist, 'key')
		playlistItemsKey.text = 'Playlist Items'
		playlistItems = etree.SubElement(playlist, 'array')

		# TODO: Add track references to playlist items element

with open('./samples/output.xml', 'wb+') as f:
	f.write(etree.tostring(tree, pretty_print=True))
