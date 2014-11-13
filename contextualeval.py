#import norvig as spelling
#import faster0 as spelling
#import faster1 as spelling
import bigrammer as spelling
import time
import ansi

def red(s):   return color(ansi.red, s)
def blue(s):  return color(ansi.blue, s)
def green(s): return color(ansi.green, s)
def color(c, s):
    return ansi.set_foreground(c) + s + ansi.set_foreground(ansi.default_color)

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
        corrected, before, after = correct(badline, speller)
        n += 1
        if goodline.lower() != corrected.lower(): # TODO: expect correct case as well
            nwrong += 1
            print 'From:     ' + before.rstrip()
            print 'Expected: ' + goodline.rstrip()
            print 'Got:      ' + after.rstrip()
            print ''
    return dict(n=n, nwrong=nwrong, 
                pct=percent(n - nwrong, n),
                secs=(time.clock()-start))

def percent(n, total):
    return int(100. * n / total)

def correct(text, speller):
    fixed = before = after = ''
    p = 0
    for mistake in speller.proofread(text):
        word = (mistake.suggestions[0] if mistake.suggestions
                else '#' * len(mistake.word))
        fixed  += text[p:mistake.position] + word
        before += text[p:mistake.position] + red(mistake.word)
        after  += text[p:mistake.position] + blue(word)
        p = mistake.position + len(mistake.word)
    fixed  += text[p:]
    before += text[p:]
    after  += text[p:]
    return fixed, before, after

if __name__ == '__main__':
    import sys
    main(sys.argv)
