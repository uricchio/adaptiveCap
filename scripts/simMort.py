from genVul import GenVul
import sys
import numpy as np

numSims = 5

myTest = GenVul.EstimateEffects(inFile=sys.argv[1],recRate = 1e-4, chromBreaks=50000)

myTest.readVCFMort()

pars = np.random.choice(500,2*numSims,replace=False)

for i in range(numSims):
    myTest.makeOffspring(i,pars[2*i],pars[2*i+1])

