import re
import time
import sys

#import norvig as speller
import faster0 as speller

def main(argv):
    input = words(open('chatlogs/chatlogs.text').read())
    start = time.clock()
    ncorrections = 0
    for word in input:
        w = speller.correct(word)
        if w != word:
            ncorrections += 1
            print word, w
    sys.stderr.write('%d corrections, %d words, %g secs\n'
                     % (ncorrections, len(input), time.clock() - start))

def words(text):
    return re.findall('[a-z]+', text.lower()) 

if __name__ == '__main__':
    main(sys.argv)
