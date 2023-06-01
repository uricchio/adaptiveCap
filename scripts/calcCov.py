
import sys
from collections import defaultdict
from scipy.stats import binom_test

freq = defaultdict(dict)

fh = open(sys.argv[1],'r')


for line in fh:
    data = line.strip().split()
    freq[data[0]][data[2]] = [float(x) for x in data[3:]]


for pop in freq:
    for pop2 in freq:
        if pop2 <= pop:
            continue
        for pos in freq[pop]:
            if pos in freq[pop2]:
                print(pop, pop2, pos, freq[pop][pos][1], freq[pop][pos][2], freq[pop][pos][3], freq[pop2][pos][3], freq[pop2][pos][3],freq[pop][pos][4],freq[pop2][pos][4])
            else:
                print(pop, pop2, pos, freq[pop][pos][1], freq[pop][pos][2], freq[pop][pos][3], -1, -1 ,freq[pop][pos][4],-1)
