#!/usr/bin/env python3
import os
import yaml
import json
import subprocess
import argparse

def call_figaro(seqdir, amplen, fprlen, rprlen, figout):
    
    figaro_command="python3 /opt/figaro/figaro/figaro.py \
        -i " +seqdir+ " \
        -a " +amplen+ " \
        -f " +fprlen+ " \
        -r " +rprlen+ " \
        -o " +figout

    result = subprocess.run([figaro_command], shell=True)

    return result

def parse_figaro(figout):

    fig_to_parse = figout+"/trimParameters.json"

    with open(fig_to_parse) as json_data:
        data = json.load(json_data)

    best_result = data[0]
    forward = best_result['trimPosition'][0]
    reverse = best_result['trimPosition'][1]

    return(forward,reverse)

def modify_param(paramfile, fcutoff, rcutoff):

    with open(paramfile, 'r') as file:
        params = yaml.safe_load(file)

    params["trunclenf"] = fcutoff
    params["trunclenr"] = rcutoff
    params["trunc_qmin"] = 25

    with open(paramfile, 'w') as outfile:
        outputs = yaml.dump(params, outfile, sort_keys=False, default_flow_style=False)

def main(arg):
    call_figaro(arg.seqdir, arg.ampliconlen, arg.fprimerlen, arg.rprimerlen, arg.figaro_out)

    cutoffs = parse_figaro(arg.figaro_out)

    modify_param(arg.paramfile, cutoffs[0], cutoffs[1])




if __name__ == "__main__":
    # Build Argument Parser in order to facilitate ease of use for user
    parser = argparse.ArgumentParser(
        description="Calls figaro and updates the paramfile for nf-core/ampliseq with suggested DADA2 cutoff params")
    parser.add_argument('-s', '--seq_dir', action='store', required=True,
                        help="name of the directory with fastq files", dest='seqdir')
    parser.add_argument('-a', '--amplicon_len', action='store', required=True,
                        help="length of expeced amplicon length ", dest='ampliconlen')
    parser.add_argument('-f', '--forward_primer', action='store', required=True,
                        help="length of forward primer", dest='fprimerlen')
    parser.add_argument('-r', '--reverse_primer', action='store', required=True,
                        help="length of reverse primer", dest='rprimerlen')
    parser.add_argument('-o', '--out', action='store', required=True,
                        help="name of figaro outdir name", dest='figaro_out')
    parser.add_argument('-p', '--params', action='store', required=False,
                        help="name of paramfile to add suggested cutoffs to", dest='paramfile')
    args = parser.parse_args()
    main(args)