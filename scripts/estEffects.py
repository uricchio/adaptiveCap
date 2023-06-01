from genVul import GenVul
import sys

myTest = GenVul.EstimateEffects(inFile=sys.argv[1],trFile=sys.argv[2])

myTest.readVCF()

myTest.readTraits()

myTest.linMod()
