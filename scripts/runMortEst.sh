#!/bin/bash     
#SBATCH -N 1 # nodes requested
#SBATCH -n 1 # tasks requested
#SBATCH -c 4 # cores requested
#SBATCH --mem=8000 # memory in Mb
#SBATCH --array=1-5
#SBATCH -t 48:00:00 # time
#SBATCH -o outfile # send stdout to outfile
#SBATCH -e errfile # send stderr to errfile

if [[ -v SLURM_ARRAY_TASK_ID ]];
then
   echo $SLURM_ARRAY_TASK_ID; simID=$SLURM_ARRAY_TASK_ID
else
   simID=1
fi

S=$1

/cluster/tufts/uricchiolab/software/build/slim -d simID=$simID -d S=$S simMort.slim

python simMort.py ../simOut/BtoA/vcfs/geno.S.${S}.${simID}.vcf > ../simOut/BtoA/out/freqs.S.${S}.${simID}.txt

python calcCov.py ../simOut/BtoA/out/freqs.S.${S}.${simID}.txt > ../simOut/BtoA/out/cov.S.${S}.${simID}.txt

#python postProcFreqs.py ../simOut/BtoA/Before.${simID}.S.${S}.txt ../simOut/BtoA/After.${simID}.S.${S}.txt ../simOut/BtoA/Pop.${simID}.S.${S}.txt  > ../simOut/BtoA/freqComp.${simID}.S.${S}.txt

#python calcCov.py ../simOut/BtoA/Before.${simID}.S.${S}.txt ../simOut/BtoA/After.${simID}.S.${S}.txt ../simOut/BtoA/Pop.${simID}.S.${S}.txt  > ../simOut/BtoA/cov.${simID}.S.${S}.txt

