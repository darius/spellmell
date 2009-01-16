import re
import sys

def words(text):
    return map(stripquote, re.findall("""[a-z']+""", text.lower()))

def stripquote(s):
    #return s.replace("'", "")
    return s.strip("'")

for line in sys.stdin:
    for word in words(line):
        print word
