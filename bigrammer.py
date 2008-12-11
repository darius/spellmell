"""Spell checker.

>>> import urllib, os
>>> s = Speller()
>>> s.train((file('big.txt') if os.path.exists('big.txt')
...          else urllib.urlopen('http://norvig.com/big.txt')).read())
>>> list(s.proofread('gort'))[0].suggestions
['got', 'sort', 'port']

"""

import collections, cPickle, heapq, re

class Speller:
    def __init__(self):
        # _counts[w1] counts unigrams we've trained on.
        # _succs[w1][w2] counts bigrams we've trained on.
        # _prefixes holds all prefixes of all words we've trained on.
        self._counts = collections.defaultdict(int)
        self._succs = {}
        self._prefixes = set()
    def train(self, text):
        previous = '#'
        for pos, word in words(text):
            self._note_ngram(previous, word)
            if word not in self._prefixes: self._note_prefixes(word)
            previous = word
        self._note_ngram(previous, '#')
    def _note_ngram(self, prev, word):
        self._counts[prev] += 1
        if prev not in self._succs:
            self._succs[prev] = collections.defaultdict(int)
        self._succs[prev][word] += 1
    def _note_prefixes(self, word):
        self._prefixes.update(set(word[:i] for i in range(len(word) + 1)))
    def save(self, file):
        cPickle.dump(self._succs, file)
    def load(self, file):
        self._succs = cPickle.load(file)
        self._counts = dict((word, len(succs))
                            for word, succs in self._succs.items())
        self._prefixes = set()
        for word in self._counts.keys(): 
            self._note_prefixes(word)
    def proofread(self, text):
        # XXX use _succs
        for pos, word in words(text):
            if word in self._counts: continue
            edits = self._edits('', word, 1) or self._edits('', word, 2)
            suggestions = heapq.nlargest(3, edits, key=self._counts.get)
            yield Mistake(self, pos, word, suggestions)
    def _edits(self, head, tail, distance):
        # Return a set of the words in self._counts that are at the
        # given edit distance from head+tail (with edits restricted to
        # the tail and to deletions on the right of the head).
        # Precondition: head in self._prefixes
        if 0 == distance:
            return [head+tail] if head+tail in self._counts else []
        exts = [head + c for c in alphabet if head + c in self._prefixes]
        deletes = ([] if not head else
                   [self._edits(head[:-1], tail, distance - 1)])
        inserts = [self._edits(p, tail, distance - 1) for p in exts]
        if not tail:
            return flatten(deletes + inserts)
        transposes = ([self._edits(head, tail[1]+tail[0]+tail[2:], distance-1)]
                      if 2 <= len(tail) and tail[0] != tail[1]
                      else [])
        replaces = [self._edits(p, tail[1:],
                                distance if p[-1] == tail[0] else distance-1)
                    for p in exts]
        return flatten(deletes + transposes + replaces + inserts)

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def flatten(xss):
    result = []
    for xs in xss:
        result.extend(xs)
    return set(result)

class Mistake:
    def __init__(self, corrector, position, word, suggestions):
        self.corrector   = corrector
        self.position    = position
        self.word        = word
        self.suggestions = suggestions
    def should_have_been(self, word):
        if word not in self.suggestions:
            self.corrector.train(word)

def words(text):
    return ((m.start(), m.group(0))
            for m in re.finditer(r'[a-z]+', text.lower()))
