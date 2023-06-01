# load correct anaconda env first 
module load anaconda/2021.11

# 
rm ../simOut/traits/*
rm ../simOut/vcfs/*
rm ../simOut/estEffects/*

# run slim -- get rid of the output trait files in ../simOut/traits if needed first
for i in {1..5};  do for S in {0.01,0.1,0.2,0.5,,0.5,1,2,5}; do /cluster/tufts/uricchiolab/software/build/slim -d simID=$i -d S=$S simAssoc.slim ; done; done

# run analysis
for i in {1..5}; do for S in {0.01,0.05,0.1,0.2,0.5,1,2,5}; do python estEffects.py ../simOut/vcfs/geno.S.${S}.${i}.vcf ../simOut/traits/trait.S.${S}.${i}.txt > ../simOut/estEffects/estEffects.S.${S}.${i}.txt; done; done


