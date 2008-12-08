import collections, cPickle, heapq, re

## s = Speller()
## s.train(open('big.txt').read())
## list(s.proofread('gort'))[0].suggestions
#. ['got', 'sort', 'port']

class Speller:
    def __init__(self):   self.d = collections.defaultdict(int)
    def load(self, file): self.d = cPickle.load(file)
    def save(self, file): cPickle.dump(self.d, file)
    def train(self, text):
        for pos, word in words(text):
            self.d[word] += 1
    def proofread(self, text):
        for pos, word in words(text):
            if word in self.d: continue
            cs = self._known(edits1(word)) or self._known_edits2(word)
            suggestions = heapq.nlargest(3, cs, key=self.d.get)
            yield Mistake(self, pos, word, suggestions)
    def _known_edits2(self, word):
        return set(e2 for e1 in edits1(word) for e2 in edits1(e1)
                   if e2 in self.d)
    def _known(self, words):
        return set(w for w in words if w in self.d)

class Mistake:
    def __init__(self, corrector, position, word, suggestions):
        self.corrector   = corrector
        self.position    = position
        self.word        = word
        self.suggestions = suggestions
    def should_have_been(self, word):
        if word not in self.suggestions:
            self.corrector.train(word)
    
def edits1(word):
    s = [(word[:i], word[i:]) for i in range(len(word) + 1)] ## splits
    return set([a + b[1:] for a, b in s] + ## deletes
               [a + b[1] + b[0] + b[2:] for a, b in s[:-2]] + ## transposes
               [a + c + b[1:] for a, b in s for c in alphabet] + ## replaces
               [a + c + b for a, b in s for c in alphabet]) ## inserts

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def words(text):
    return [(m.start(), m.group(0))
            for m in re.finditer(r'[a-z]+', text.lower())]
