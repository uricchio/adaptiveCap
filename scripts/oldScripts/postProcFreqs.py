
import sys
from collections import defaultdict

bef = defaultdict(dict)
aft =  defaultdict(dict)
frq =  defaultdict(dict)

fh = open(sys.argv[1],'r') # before file
for line in fh:
    data = line.strip().split()
    if data[4] == "p1":
        continue    
    bef[data[4]][data[7]] = [float(data[8]),float(data[12])/4.]
fh.close()

fh = open(sys.argv[2],'r') # after file
for line in fh:
    data = line.strip().split()
    aft[data[4]][data[7]] = [float(data[8]),float(data[12])/200.]
fh.close()

fh = open(sys.argv[3],'r') # pop file
for line in fh:
    data = line.strip().split()
    frq[data[4]][data[7]] = [float(data[8]),float(data[12])/1000.]
fh.close()

for pop in aft:
    if pop == "p1":
        continue
    for pos in aft[pop]:
        if pos in bef[pop] and pos in frq["p1"]:
            if bef[pop][pos][1] == 1.:
                continue
            if bef[pop][pos][0] != aft[pop][pos][0]:
                continue
            print(pos, aft[pop][pos][0], bef[pop][pos][1],aft[pop][pos][1],frq["p1"][pos][1], pop)

