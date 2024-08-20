#!/bin/bash

#SBATCH --partition=batch
#SBATCH --job-name=$EXAMPLE_JOB
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --time=96:00:00
#SBATCH --mem=8gb

#Replace this with your UGA email to get notified on completion
#SBATCH --mail-user="$YOUREMAIL@uga.edu"
#SBATCH --mail-type=BEGIN,END,FAIL

SUBDIR=$(pwd)

# THIS SCRIPT WILL NOT RUN AS-IS, IT IS INTENDED TO BE A STARTING POINT. ANY VARIABLE (STARTING WITH "$") MUST BE REPLACED WITH A PROPER FILEPATH.

#OUTDIR="/work/$YOUR-OUTPUT-DIRECTORY"

singularity run docker://lorentzb/figaro:1.2 python3 figaro-find.py -s $LOCATION-OF-SEQUENCES -a 400 -f 20 -r 20 -o figaro_result -p $PROJECTDIR/ampliseq-param.yaml

if [[ ! -d $SCRATCHDIR ]]; then
    mkdir -p  $SCRATCHDIR
fi

cd $SCRATCHDIR

module load Nextflow/22.04.5
nextflow run nf-core/ampliseq \
        -r 2.9.0 \
        -c $PROJECTDIR/gacrc.config \
        -profile slurm,singularity \
        -params-file $PROJECTDIR/ampliseq-param.yaml \
        -resume
        
#This command copies the output of nf-core/ampliseq from the /work directory from the ampliseq-param.yaml file to the /scratch directory for visualise-ampliseq pipeline
if [[ ! -d $SCRATCH-OUTDIR ]]; then
    cp -rf $WORK-OUTDIR $SCRATCH-OUTDIR
fi

#This command copies the metadata file from the $PROJECTDIR to the /scratch dir if it is not present
if [[ ! -f $SCRATCHDIR/metadata.tsv ]]; then 
    cp $PROJECTDIR/metadata.tsv $SCRATCHDIR/metadata.tsv
fi 

nextflow run lorentzben/visualize-ampliseq \
        -r main \
        -with-tower \
        -profile slurm,singularity \
        -params-file $PROJECTDIR/visualize-ampliseq-param.yaml \
        -latest \
        -resume 
        
if [[ ! -d $WORKDIR/figaro_result ]]; then
    cp -rf $SUBDIR/figaro_result $WORKDIR/
fi