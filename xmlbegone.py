"""
Quick-and-dirty conversion from XML to plaintext. There must be a 
better way.
"""

import xml.parsers.expat

ugh = []

def start_element(name, attrs):
    pass
def end_element(name):
    pass
def char_data(data):
    ugh.append(data)

for line in open(sys.stdin):
    if line.startswith('<message'): # XXX adapt to wikipedia's xml
        p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = start_element
        p.EndElementHandler = end_element
        p.CharacterDataHandler = char_data
        p.Parse(line, 1)
        print ''.join(ugh).encode('utf8')
        ugh = []
