import collections
import re
import string

def correct(word):
    candidates = (corrections('', word, 0)
                  or corrections('', word, 1)
                  or corrections('', word, 2))
    return max(candidates, key=NWORDS.get) if candidates else word

def corrections(head, tail, distance):
    # Return a set of the words in NWORDS that are at the given edit
    # distance from head+tail (with edits restricted to the tail and
    # to deletions on the right of the head).
    # Precondition: head in known_prefixes
    if 0 == distance:
        return [head+tail] if head+tail in NWORDS else []
    exts = [head + c for c in alphabet if head + c in known_prefixes]
    deletes = ([] if not head else
               [corrections(head[:-1], tail, distance - 1)])
    inserts = [corrections(p, tail, distance - 1) for p in exts]
    if not tail:
        return flatten(deletes + inserts)
    transposes = ([corrections(head, tail[1]+tail[0]+tail[2:], distance-1)]
                  if 2 <= len(tail) and tail[0] != tail[1]
                  else [])
    replaces = [corrections(p, tail[1:],
                            distance if p[-1] == tail[0] else distance-1)
                for p in exts]
    return flatten(deletes + transposes + replaces + inserts)

alphabet = string.ascii_lowercase

def flatten(xss):
    result = []
    for xs in xss:
        result.extend(xs)
    return set(result)

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return dict(model)

def words(text):
    return re.findall('[a-z]+', text.lower()) 

NWORDS = train(words(file('data/big.txt').read()))
known_prefixes = set(_w[:_i] for _w in NWORDS for _i in range(len(_w) + 1))
