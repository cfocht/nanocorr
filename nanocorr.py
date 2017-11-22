#!/usr/bin/env python

"""
nanocorr.py

Usage:
    nanocorr.py <raw_reads> <correction_reads> [--ref <reference_fasta>]
Arguments:

"""

import sys
import os
from docopt import docopt


def runfail(cmd):
    print "Running : %s" % cmd
    if not 0 == os.system(cmd):
        sys.exit("Failed : %s " % cmd)


def main(args):

    query_file = args['<correction_reads>']
    ref_file = args['<reference_fasta>']
    start_file = args['<raw_reads>']

    start_path = os.getcwd()
    if not os.path.isabs(query_file):
        query_file = os.path.join(start_path, query_file)
    if ref_file and not os.path.isabs(ref_file):
        ref_file = os.path.join(start_path, ref_file)

    tmp_dir = os.environ["TMPDIR"]
    os.chdir(tmp_dir)

    runfail("cp {} . ".format(os.path.join(start_path, start_file)))

    runfail("makeblastdb -dbtype nucl -in {}".format(start_file))

    blast6_out = start_file + ".blast6"
    runfail("blastn -db {db} -query {query} -outfmt \"6 std qlen slen qseq sseq\" -dust no -task blastn -reward 5 -penalty -4 -gapopen 8 -gapextend 6 -evalue 1e-15 | sort -k 2,2 -k 9,9n > {outfile}".format(db=start_file, query=query_file, outfile=blast6_out))

    runfail("cp {} {} ".format(blast6_out, start_path))

    blast6_filter_out = start_file +".blast6.r"
    runfail("blast6Filter r_experimental {} > {}".format(blast6_out, blast6_filter_out))

    runfail("cp {} {} ".format(blast6_filter_out, start_path))

    correct_fa = start_file + ".blast6.r.fa"
    correct_log = start_file + ".blast6.r.log"

    cor_params = {"raw_reads": start_file,
              "filter_out": blast6_filter_out,
              "cor_fa" : correct_fa,
              "cor_log" : correct_log}

    runfail("correctOxford {raw_reads} {filter_out} > {cor_fa} 2> {cor_log}".format(**cor_params))
    runfail("cp {} {} {}".format(correct_fa,correct_log,start_path))

    if ref_file:

        refblast_out = start_file + ".blast6.r.refblast6"
        ref_blast_params = {"reference": ref_file,
                        "cor_query": correct_fa,
                        "ref_blast_out": refblast_out}

        runfail("blastn -db {reference} -query {cor_query} -outfmt \"6 std qlen slen\" -evalue 1e-10 -reward 5 -penalty -4 -gapopen 8 -gapextend 6 -dust no -task blastn -out {ref_blast_out}".format(**ref_blast_params))


        refblast_filter_out = start_file + ".blast6.r.refblast6.q"
        runfail("blast6Filter q {} > {}".format(refblast_out, refblast_filter_out))

        runfail("cp {} {} ".format(refblast_filter_out, start_path))


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Nanocorr  0.1')
    print arguments
    main(arguments)







