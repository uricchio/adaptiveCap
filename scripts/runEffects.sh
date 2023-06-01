#!/bin/bash	
#SBATCH -N 1 # nodes requested
#SBATCH -n 1 # tasks requested
#SBATCH -c 4 # cores requested
#SBATCH --mem=8000 # memory in Mb
#SBATCH --array=1-5 
#SBATCH -t 10:00:00 # time
#SBATCH -o outfile # send stdout to outfile
#SBATCH -e errfile # send stderr to errfile

module load anaconda/2021.11

if [[ -v SLURM_ARRAY_TASK_ID ]];
then
    echo $SLURM_ARRAY_TASK_ID; simID=$SLURM_ARRAY_TASK_ID
else
    simID=1
fi

S=$1
i=$simID

python estEffects.py ../simOut/vcfs/geno.S.${S}.${i}.vcf ../simOut/traits/trait.S.${S}.${i}.txt > ../simOut/estEffects/estEffects.S.${S}.${i}.txt
