
# have to complete the first line first

#for S in {0.02,0.05,0.1,0.2,0.5,1,2,5,10}; do sbatch runSims.sh $S; done
for S in {0.02,0.05,0.1,0.2,0.5,1,2,5,10}; do sbatch runEffects.sh $S; done
