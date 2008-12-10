"""
Let's see how big and spacey a dict of 1-edits of all words would be.
"""

import norvig as speller

s = speller.Speller()
s.load(open('bigdict'))

edits = set()
for i, word in enumerate(s.d):
    #if i % 1000: print '.',
    edits |= set(speller.edits1(word))
print ''

print len(edits), sum(map(len, edits)), len(s.d)
