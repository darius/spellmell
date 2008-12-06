import math
import sys

threshold = int(sys.argv[1])

freqs = {}
for line in sys.stdin:
    try:
        freq, word = line.split()
    except ValueError:
        continue
    if int(freq) < threshold:
        continue
    freqs[word] = int(freq)

n = float(sum(freqs.values()))

for word, count in freqs.items():
    cost = -math.log(count / n)
    #cost -= 3.78896 - 2.46093
    print '%g\t%s' % (cost, word)
