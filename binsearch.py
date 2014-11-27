"""Spell checker.
Derived from faster0.py; tuned for faster startup but slower per-word time.

>>> from binsearch import Speller
>>> import urllib, os
>>> s = Speller()
>>> s.cached_load('bigdict',
...   lambda: (open('big.txt') if os.path.exists('big.txt')
...            else urllib.urlopen('http://norvig.com/big.txt')).read())
>>> list(s.proofread('gort'))[0].suggestions
['got', 'sort', 'port']

"""

import bisect, collections, cPickle, heapq, operator, re

## s = Speller()
## s.train('the apple is the curse of god')
## for x in s.proofread('i am the devil'): print x
#. (at 0: i -> is)
#. (at 2: am -> of/is)
#. (at 9: devil -> )

class Speller:
    def __init__(self):
        self._words, self._counts = [], []
    def cached_load(self, filename, get_corpus): # XXX too-fancy interface
        try:
            self.load(open(filename))
        except IOError:
            self.train(get_corpus())
            self.save(open(filename, 'w'))
    def train(self, text):
        # TODO: make incremental training efficient
        old = dict(zip(self._words, self._counts))
        counter = collections.Counter(word for pos, word in words(text))
        self._words.extend(counter.keys())
        self._words.sort()
        self._counts = [old.get(w, 0) + counter[w] for w in self._words]
    def save(self, file):
        cPickle.dump((self._words, self._counts), file)
    def load(self, file):
        self._words, self._counts = cPickle.load(file)
    def proofread(self, text):
        for pos, word in words(text):
            i = bisect.bisect_left(self._words, word)
            if 0 <= i < len(self._words) and self._words[i] == word: continue
            edits = self._edits('', word, 1) or self._edits('', word, 2)
            suggestions = heapq.nlargest(3, edits, key=self._get_count)
            yield Mistake(self, pos, word, suggestions)
    def _get_count(self, word):
        i = bisect.bisect_left(self._words, word)
        if i < len(self._words) and self._words[i] == word:
            return self._counts[i]
        else:
            return 0
    def _has_prefix(self, head):
        i = bisect.bisect_left(self._words, head)
        return i < len(self._words) and self._words[i].startswith(head)
    def _edits(self, head, tail, distance):
        # Return a set of the words in self._words that are at the
        # given edit distance from head+tail (with edits restricted to
        # the tail and to deletions on the right of the head).
        # Precondition: head is '' or a prefix of a word in self._words
        if 0 == distance:
            return [head+tail] if self._get_count(head+tail) else []
        exts = [head + c for c in alphabet if self._has_prefix(head + c)]
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
    return reduce(operator.or_, map(set, xss), set())

class Mistake:
    def __init__(self, corrector, position, word, suggestions):
        self.corrector   = corrector
        self.position    = position
        self.word        = word
        self.suggestions = suggestions
    def should_have_been(self, word):
        if word not in self.suggestions:
            self.corrector.train(word)
    def __repr__(self):
        return ("(at %d: %s -> %s)" 
                % (self.position, self.word,
                   '/'.join(self.suggestions)))

def words(text):
    return ((m.start(), m.group(0))
            for m in re.finditer(r'[a-z]+', text.lower()))
