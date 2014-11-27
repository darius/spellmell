import re
import sys
import time

#import norvig as spelling
import faster0 as spelling
#import binsearch as spelling

def main(argv):
    speller = spelling.Speller()
    speller.load(open('bigdict'))
    input = open(argv[1]).read()
    nwords = len(words(input))
    start = time.clock()
    ncorrections = 0
    for mistake in speller.proofread(input):
        ncorrections += 1
        print mistake.word, '/'.join(mistake.suggestions)
    sys.stderr.write('%d corrections, %d words, %g secs\n'
                     % (ncorrections, nwords, time.clock() - start))

def words(text):
    return re.findall('[a-z]+', text.lower()) 

if __name__ == '__main__':
    main(sys.argv)
