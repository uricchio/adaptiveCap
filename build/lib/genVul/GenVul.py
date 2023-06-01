import sys
import numpy as np
from collections import defaultdict
import statsmodels.api as sm
import random
import math
from scipy.stats import binom_test

class EstimateEffects():

    def __init__(self,inFile='../simOut/vcfs/geno.1.vcf',genos=defaultdict(dict),traits=[],
                      trFile='../simOut/traits/trait.1.txt',inds = 500, nbases = 100000, 
                      nKids = 200, recRate = 1e-2,chromBreaks = 50):

        self.inFile = inFile
        self.trFile = trFile
        self.genos = genos
        self.traits = traits
        self.effects = defaultdict(dict)
        self.effVec = []
        self.freqs = defaultdict(dict)
        self.acVec = []
        self.pops = []
        self.inds = inds
        self.nKids = nKids
        self.recRate = recRate
        self.chromBreaks = chromBreaks

    def readVCF(self):

        fh = open(self.inFile, 'r')
        for line in fh:
            if(line[0] == "#"):
                continue

            data = line.strip().split()

            genos = []
            # get genotype data
            for ind in data[9:]:
                geno = ind.split('|')
                geno = np.sum([float(x) for x in geno])
                genos.append([geno,1])
        
            if data[1] not in self.genos[data[0]]:
                self.genos[data[0]][data[1]] = genos

                # get true effects of SNPs
            
                info = data[7].split(';')
                for thing in info:
                    if thing[:2] == 'S=':
                        eff = thing.split('=')
                        self.effects[data[0]][data[1]] = float(eff[1])         
                        self.effVec.append( float(eff[1]))         
                    if thing[:3] == 'AC=':
                        ac = thing.split('=')
                        self.freqs[data[0]][data[1]] = float(ac[1])/(2*self.inds)         
                        self.acVec.append( float(ac[1])/(2*self.inds))         
        fh.close()
    
    def readVCFMort(self):
        fh = open(self.inFile, 'r')
        for line in fh:
            if(line[0] == "#"):
                continue
            data = line.strip().split()
            chromNum =  str(int(math.ceil(int(data[1])/self.chromBreaks)))
            genos = []
            # get genotype data
            for ind in data[9:]:
                geno = ind.split('|')
                geno = [int(x) for x in geno]
                genos.append(geno)
            if data[1] not in self.genos[chromNum]:
                self.genos[chromNum][data[1]] = genos
            # get true effects of SNPs
                info = data[7].split(';')
                for thing in info:
                    if thing[:2] == 'S=':
                        eff = thing.split('=')
                        self.effects[chromNum][data[1]] = float(eff[1])
                        self.effVec.append( float(eff[1]))         
                    if thing[:3] == 'AC=':
                        ac = thing.split('=')
                        self.freqs[data[0]][data[1]] = float(ac[1])/(2*self.inds)
                        self.acVec.append( float(ac[1])/(2*self.inds))
        fh.close()

    def readTraits(self):

        fh = open(self.trFile, 'r')
        for line in fh:
            self.traits.append(float(line.strip()))
            self.pops.append(1)
        #self.traits = np.array(self.traits)

        fh.close() 

    def linMod(self):

        for chrom in self.genos:
            for pos in self.genos[chrom]:
                #print(np.sum(self.genos[chrom][pos])/(2*len(self.genos[chrom][pos])))
                #exit()
                #if np.sum(self.genos[chrom][pos]) < len(self.genos[chrom][pos])*2*0.05 or np.sum(self.genos[chrom][pos]) > len(self.genos[chrom][pos])*2*0.95 :
                #    continue
                result = sm.OLS(self.traits, self.genos[chrom][pos]) # np.column_stack((genos,np.ones(len(genos)))))
                res = result.fit()
                print(res.pvalues[0], res.params[0], self.effects[chrom][pos],-0.5+np.sum(self.genos[chrom][pos])/(len(self.genos[chrom][pos])*2))



    def makeOffspring(self,simNum, p1, p2):

        par1 = [[],[]]
        par2 = [[],[]]

        # get chromosomes
        for chrom in self.genos:
            #print(len(self.genos[chrom]))
            for pos in self.genos[chrom]:    
                par1[0].append(self.genos[chrom][pos][p1][0])          
                par1[1].append(self.genos[chrom][pos][p1][1])
                par2[0].append(self.genos[chrom][pos][p2][0])         
                par2[1].append(self.genos[chrom][pos][p2][1])

        parents = [par1,par2]

        # make recombined offspring
        kids = []
      
        while len(kids) < self.nKids:
            kid = [[],[]]
            for par in range(0,2):
                i = 0
                for chrom in self.genos:
                    pos0 = 0
                    chromNum = 0
                    if random.random() > 0.5:
                        chromNum = 1-chromNum
                    for pos in self.genos[chrom]:
                        nRec = np.random.poisson((int(pos)-pos0)*self.recRate)
                        if nRec % 2 == 1:
                            chromNum = 1-chromNum
                        kid[par].append(parents[par][chromNum][i])
                        i += 1
                        pos0 = int(pos)
                    
            kids.append(kid)        

        trs = []
        
        for kid in kids:
        
            
            tr1 = np.dot(kid[0],self.effVec)
            tr2 = np.dot(kid[1],self.effVec)
 
            tr = tr1+tr2
 
            trs.append(tr)

        # impose selection
        trs = np.subtract(trs,np.mean(trs))
        trs = np.divide(trs, np.std(trs))

        trs = np.add(trs,1)
        for i in range(len(trs)):
            if trs[i] < 0:
                trs[i] = 0 
        trs = np.divide(trs,np.sum(trs))
        
        inds = np.random.choice(len(trs),int(len(trs)/2), p=trs,replace=False)
        
        # now print previous and final allele freq of each allele
        
        i = 0
        for chrom in self.genos:
            for var in self.genos[chrom]:
                tot = 0
                for kid in inds:
                    tot += kids[kid][0][i]+kids[kid][1][i]
                tot /= (len(inds)*2)
 
                totBef = 0
                for kid in range(len(kids)):
                    totBef += kids[kid][0][i]+kids[kid][1][i]
                totBef /= (len(kids)*2)
  
                if (parents[0][0][i]+parents[0][1][i]+parents[1][0][i]+parents[0][1][i])/4. != 0. and (parents[0][0][i]+parents[0][1][i]+parents[1][0][i]+parents[0][1][i])/4. != 1.:
                    print(simNum, chrom, var, self.effVec[i], self.acVec[i], totBef, tot, binom_test(tot*len(inds)*2,len(inds)*2,totBef))
                i += 1      

         
