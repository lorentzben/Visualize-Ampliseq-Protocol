# Visualize-Ampliseq-Protocol

## Ben Lorentz

# Introduction

This pair of pipelines was constructed to simplify microbiome analysis of 16s rRNA amplicons. The first pipeline nf-core/ampliseq was built by the organization nf core which is composed of a group of scientists and programmers. This pipeline simplifies the amplicon analysis, however lacks a suite of polished figures. The solution is a custom pipeline I constructed called lorentzben/visualize-ampliseq. This pipeline takes the results directory from a nf-core/ampliseq run and re-computes some diversity measurements and generates figures that ampliseq does not.  
Installation
Required:
-	Linux System (preferably sapleo2)
-	Docker/Singularity 
-	Nextflow installed (version 24.04.2)
-	Sequence files in FASTQ format

# Usage

To enhance reproducibility and as a requirement for nf-core/ampliseq a sample sheet must be constructed in .csv format with the sample-id as well as path as columns. A metadata sheet must additionally be constructed with a column of interest (usually control/treatment or day of study). The sample-id columns must match between sheets. Additionally, a params file should be provided to handle input and output paths of files. Example files can be found in this repository.

# Parameters

The major parameters that must be provided in the “parameters.yaml” for nf-core/ampliseq are as follows:

input: Points to the manifest file that contains “sample-id and reads (possibly forward and reverse)”
-	A good location is on the “home” partition
metadata: Points to the metadata file that contains “sample-id and treatment column”
outdir: Points to where the output files should be saved
-	A good location is usually on the “work” partition

For further clarification see: https://nf-co.re/ampliseq/2.11.0/docs/usage/

The major parameters that must be provided in the “parameters.yaml” for visualize-ampliseq are as follows:
input: A directory containing the output from nf-core/ampliseq
ioi: Which column in the metadata that contains the treatment  
metadata: Location of a metadata file with a column titled with the same value provided in “ioi” 
outdir: Location of the output from this pipeline to be saved. 
controls: OPTIONAL If positive control samples were used, tsv file that contains sample IDs of positive controls
ordioi: OPTIONAL, if the user wants to order the levels of the “ioi” column this tsv lists the order if alphabetic is not desired
rare: rarefaction depth (default is the lowest richness value of one sample)
srs: is srs curve plot desired?
negative: OPTIONAL, if negative control samples are provided, name in “ioi”
mock: OPTIONAL, if mock community samples are provided, name in “ioi”
report: Generate a report?
refSeq: OPTIONAL, reference sequences in qza format for mock community
refTab: OPTIONAL, reference taxonomy in qza format for mock community

# Output

From visualize-ampliseq: 
The following directories hold results from visualize-ampliseq. The primary directory of interest will be html which contains the html reports with figures embedded. 
barrnap
clean-qza-table
clean-tsv-table
control-removed
dada2
fastqc
figaro_result
filtered-mock-table
filtered-nc-table
html
input
multiqc
ordered-ioi
pdf
pipeline_info
qiime2
scratch
srs_curve
srs_normalize
