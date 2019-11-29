from io import BytesIO
from lxml import etree

tree = etree.parse('iTunes Music Library.xml')

with open('./output.xml', 'wb+') as f:
	f.write(etree.tostring(tree, pretty_print=True))