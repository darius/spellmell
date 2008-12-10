"""Spell checker.

>>> import urllib
>>> s = Speller()
>>> s.train(urllib.urlopen('http://norvig.com/big.txt').read())
>>> list(s.proofread('gort'))[0].suggestions
['got', 'sort', 'port']

"""

import collections, cPickle, heapq, re

class Speller:
    def __init__(self):
        # _freqs gives the frequencies of all words we've trained on.
        # _prefixes holds all prefixes of all words we've trained on.
        self._freqs, self._prefixes = collections.defaultdict(int), set()
    def train(self, text):
        for pos, word in words(text):
            if word not in self._prefixes: self._note_prefixes(word)
            self._freqs[word] += 1
    def _note_prefixes(self, word):
        self._prefixes.update(set(word[:i] for i in range(len(word) + 1)))
    def save(self, file):
        cPickle.dump(self._freqs, file)
    def load(self, file):
        self._freqs, self._prefixes = cPickle.load(file), set()
        for word in self._freqs.keys(): 
            self._note_prefixes(word)
    def proofread(self, text):
        for pos, word in words(text):
            if word in self._freqs: continue
            edits = self._edits('', word, 1) or self._edits('', word, 2)
            suggestions = heapq.nlargest(3, edits, key=self._freqs.get)
            yield Mistake(self, pos, word, suggestions)
    def _edits(self, head, tail, distance):
        # Return a set of the words in self._freqs that are at the
        # given edit distance from head+tail (with edits restricted to
        # the tail and to deletions on the right of the head).
        # Precondition: head in self._prefixes
        if 0 == distance:
            return [head+tail] if head+tail in self._freqs else []
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
    return [(m.start(), m.group(0))
            for m in re.finditer(r'[a-z]+', text.lower())]
