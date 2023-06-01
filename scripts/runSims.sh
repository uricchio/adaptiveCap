#!/bin/bash	
#SBATCH -N 1 # nodes requested
#SBATCH -n 1 # tasks requested
#SBATCH -c 4 # cores requested
#SBATCH --mem=8000 # memory in Mb
#SBATCH --array=1-5 # memory in Mb
#SBATCH -t 10:00:00 # time
#SBATCH -o outfile # send stdout to outfile
#SBATCH -e errfile # send stderr to errfile

#module load anaconda/2021.11

if [[ -v SLURM_ARRAY_TASK_ID ]];
then 
    echo $SLURM_ARRAY_TASK_ID; simID=$SLURM_ARRAY_TASK_ID
else
    simID=1
fi 

/cluster/tufts/uricchiolab/software/build/slim -d simID=$simID -d S=$1 simAssoc.slim

#for i in {1..3}; do for shape in {0.01,0.05,0.1,0.2,0.5,1,2,5}; do python estEffects.py ../simOut/vcfs/geno.shape.${shape}.${i}.vcf ../simOut/traits/trait.shape.${shape}.${i}.txt > ../simOut/estEffects/estEffects.shape.${shape}.${i}.txt; done; done
