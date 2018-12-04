from lxml import etree
from lxml.html.soupparser import fromstring
from bs4 import BeautifulSoup

with open('polypodiales_download_2018-11-03fresh.xml', 'r') as fin:
    text = fin.read()
    
# print(len(text))
# tree = etree.fromstring(text)

chunks = ['<INSDSeq>' + t.strip() for t in text.split('<INSDSeq>')]

elements = []
for c in chunks:
    tree = etree.fromstring(BeautifulSoup(c, 'lxml').prettify())
    elements.append(tree)

node = etree.fromstring('<genestuff></genestuff>')

for i, e in enumerate(elements):
    node.insert(i, e)

with open('sequencepleasework.xml', 'wb') as fout:
    fout.write(etree.tostring(node, pretty_print=True))