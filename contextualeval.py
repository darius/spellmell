#import norvig as spelling
#import faster0 as spelling
#import faster1 as spelling
import bigrammer as spelling
import time

def main(argv):
    def train_it():
        trainer = spelling.Speller()
        trainer.train(open('big.txt').read())
        trainer.save(open('bigdict', 'w'))
    timed('training', train_it)
    speller = spelling.Speller()
    timed('loading', lambda: speller.load(open('bigdict')))
    print spelltest(speller, open('contextual-test-set'))

def timed(label, f):
    start = time.clock()
    result = f()
    print 'Time for %s: %g' % (label, time.clock() - start)
    return result

def spelltest(speller, f):
    start = time.clock()
    n, nwrong = 0, 0
    while True:
        badline = f.readline()
        if badline == '': break
        goodline = f.readline()
        blank = f.readline()
        assert blank.isspace()
        corrected = correct(badline, speller)
        n += 1
        nwrong += (goodline != corrected)
        if goodline != corrected:
            print 'From:     ' + badline
            print 'Expected: ' + goodline
            print 'Got:      ' + corrected
            print ''
    return dict(n=n, nwrong=nwrong, 
                pct=percent(n - nwrong, n),
                secs=(time.clock()-start))

def percent(n, total):
    return int(100. * n / total)

def correct(text, speller):
    fixed = ''
    p = 0
    for mistake in speller.proofread(text):
        word = mistake.suggestions[0] if mistake.suggestions else mistake.word
        fixed += text[p:mistake.position] + word
        p = mistake.position + len(mistake.word)
    fixed += text[p:]
    return fixed

if __name__ == '__main__':
    import sys
    main(sys.argv)
