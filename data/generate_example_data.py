import click
import string
import pandas as pd
import numpy as np
import os
from scipy.stats import skewnorm
from scipy.stats import norm

from datetime import datetime, timedelta

index_data = [('A002', 'CGATGT'),
              ('A005', 'ACAGTG'),
              ('A007', 'CAGATC'),
              ('A012', 'CTTGTA'),
              ('A013', 'AGTCAA'),
              ('A014', 'AGTTCC'),
              ('A018', 'GTCCGC'),
              ('A019', 'GTGAAA'),
              ('A001', 'ATCACG'),
              ('A003', 'TTAGGC'),
              ('A008', 'ACTTGA'),
              ('A010', 'TAGCTT'),
              ('A020', 'GTGGCC'),
              ('A022', 'CGTACG'),
              ('A025', 'ACTGAT')]

header = ['SampleID',
          'SampleType',
          'Flowcell',
          'Description',
          'SampleProject',
          'IndexID',
          'Index',
          'Well',
          'Library_nM',
          'QCFlag',
          'QCFailure',
          'QCWarning',
          'NCV_13',
          'NCV_18',
          'NCV_21',
          'NCV_X',
          'NCV_Y',
          'Ratio_13',
          'Ratio_18',
          'Ratio_21',
          'Ratio_X',
          'Ratio_Y',
          'Clusters',
          'TotalReads2Clusters',
          'MaxMisindexedReads2Clusters',
          'IndexedReads',
          'TotalIndexedReads2Clusters',
          'Tags',
          'NonExcludedSites',
          'NonExcludedSites2Tags',
          'Tags2IndexedReads',
          'PerfectMatchTags2Tags',
          'GCBias',
          'GCR2',
          'NCD_13',
          'NCD_18',
          'NCD_21',
          'NCD_X',
          'NCD_Y',
          'Chr1_Coverage',
          'Chr2_Coverage',
          'Chr3_Coverage',
          'Chr4_Coverage',
          'Chr5_Coverage',
          'Chr6_Coverage',
          'Chr7_Coverage',
          'Chr8_Coverage',
          'Chr9_Coverage',
          'Chr10_Coverage',
          'Chr11_Coverage',
          'Chr12_Coverage',
          'Chr13_Coverage',
          'Chr14_Coverage',
          'Chr15_Coverage',
          'Chr16_Coverage',
          'Chr17_Coverage',
          'Chr18_Coverage',
          'Chr19_Coverage',
          'Chr20_Coverage',
          'Chr21_Coverage',
          'Chr22_Coverage',
          'ChrX_Coverage',
          'ChrY_Coverage',
          'Chr1',
          'Chr2',
          'Chr3',
          'Chr4',
          'Chr5',
          'Chr6',
          'Chr7',
          'Chr8',
          'Chr9',
          'Chr10',
          'Chr11',
          'Chr12',
          'Chr13',
          'Chr14',
          'Chr15',
          'Chr16',
          'Chr17',
          'Chr18',
          'Chr19',
          'Chr20',
          'Chr21',
          'Chr22',
          'ChrX',
          'ChrY',
          'Median_13',
          'Median_18',
          'Median_21',
          'Median_X',
          'Median_Y',
          'Stdev_13',
          'Stdev_18',
          'Stdev_21',
          'Stdev_X',
          'Stdev_Y',
          'FF_Formatted']


@click.group(help="CLI tool to used to generate dummy data for NIPTViewer")
def cli():
    pass


@cli.command(short_help="generate dummy data")
def generate_dummy_data():
    date = datetime.now()

    def print_file(file, barcode, data, iter, c_index):
        def _print_row(indexid, c_iter, out, index_counter):
            index = ''.join(np.random.choice(list("ACGT"), size=6))
            sample_type = "Test"
            if data["sample_id"][c_iter].startswith("XY-XX"):
                sample_type = "Control"
            if data["ff_formatted"][c_iter] == "None":
                ff_formatted = "NA"
            else:
                ff_formatted = "{:.0f}%".format(float(data["ff_formatted"][c_iter]) * 100)
            out.write(f'\n"{data["sample_id"][c_iter]}"'
                      f',"{sample_type}"'
                      f',"{barcode}"'
                      ',""'
                      ',""'
                      f',"{index_data[index_counter][0]}"'
                      f',"{index_data[index_counter][1]}"'
                      f',"A{indexid}"'
                      f',"{data["library_nm"][c_iter]}"'
                      ',"0"'
                      ',""'
                      f',""'
                      f',"{data["ncv_13"][c_iter]}"'
                      f',"{data["ncv_18"][c_iter]}"'
                      f',"{data["ncv_21"][c_iter]}"'
                      f',"{data["ncv_X"][c_iter]}"'
                      f',"{data["ncv_Y"][c_iter]}"'
                      f',"{data["ratio_13"][c_iter]}"'
                      f',"{data["ratio_18"][c_iter]}"'
                      f',"{data["ratio_21"][c_iter]}"'
                      f',"{data["ratio_y"][c_iter]}"'
                      f',"{data["ratio_X"][c_iter]}"'
                      f',"{data["clusters"][c_iter]}"'
                      f',"{data["total_reads_2_clusters"][c_iter]}"'
                      f',"{data["max_misindexed_reads_2_clusters"][c_iter]}"'
                      f',"{data["indexed_reads"][c_iter]}"'
                      f',"{data["total_indexed_reads_2_clusters"][c_iter]}"'
                      f',"{data["tags"][c_iter]}"'
                      f',"{data["non_excluded_sites"][c_iter]}"'
                      f',"{data["non_excluded_sites_2_tags"][c_iter]}"'
                      f',"{data["tags_2_indexed_reads"][c_iter]}"'
                      f',"{data["perfect_match_tags_2_tags"][c_iter]}"'
                      f',"{data["gc_bias"][c_iter]}"'
                      f',"{data["gcr2"][c_iter]}"'
                      f',"{data["ncd_13"][c_iter]}"'
                      f',"{data["ncd_18"][c_iter]}"'
                      f',"{data["ncd_21"][c_iter]}"'
                      f',"{data["ncd_x"][c_iter]}"'
                      f',"{data["ncd_y"][c_iter]}"'
                      f',"{data["chr1_coverage"][c_iter]}"'
                      f',"{data["chr2_coverage"][c_iter]}"'
                      f',"{data["chr3_coverage"][c_iter]}"'
                      f',"{data["chr4_coverage"][c_iter]}"'
                      f',"{data["chr5_coverage"][c_iter]}"'
                      f',"{data["chr6_coverage"][c_iter]}"'
                      f',"{data["chr7_coverage"][c_iter]}"'
                      f',"{data["chr8_coverage"][c_iter]}"'
                      f',"{data["chr9_coverage"][c_iter]}"'
                      f',"{data["chr10_coverage"][c_iter]}"'
                      f',"{data["chr11_coverage"][c_iter]}"'
                      f',"{data["chr12_coverage"][c_iter]}"'
                      f',"{data["chr13_coverage"][c_iter]}"'
                      f',"{data["chr14_coverage"][c_iter]}"'
                      f',"{data["chr15_coverage"][c_iter]}"'
                      f',"{data["chr16_coverage"][c_iter]}"'
                      f',"{data["chr17_coverage"][c_iter]}"'
                      f',"{data["chr18_coverage"][c_iter]}"'
                      f',"{data["chr19_coverage"][c_iter]}"'
                      f',"{data["chr20_coverage"][c_iter]}"'
                      f',"{data["chr21_coverage"][c_iter]}"'
                      f',"{data["chr22_coverage"][c_iter]}"'
                      f',"{data["chrx_coverage"][c_iter]}"'
                      f',"{data["chry_coverage"][c_iter]}"'
                      f',"{data["chr1"][c_iter]}"'
                      f',"{data["chr2"][c_iter]}"'
                      f',"{data["chr3"][c_iter]}"'
                      f',"{data["chr4"][c_iter]}"'
                      f',"{data["chr5"][c_iter]}"'
                      f',"{data["chr6"][c_iter]}"'
                      f',"{data["chr7"][c_iter]}"'
                      f',"{data["chr8"][c_iter]}"'
                      f',"{data["chr9"][c_iter]}"'
                      f',"{data["chr10"][c_iter]}"'
                      f',"{data["chr11"][c_iter]}"'
                      f',"{data["chr12"][c_iter]}"'
                      f',"{data["chr13"][c_iter]}"'
                      f',"{data["chr14"][c_iter]}"'
                      f',"{data["chr15"][c_iter]}"'
                      f',"{data["chr16"][c_iter]}"'
                      f',"{data["chr17"][c_iter]}"'
                      f',"{data["chr18"][c_iter]}"'
                      f',"{data["chr19"][c_iter]}"'
                      f',"{data["chr20"][c_iter]}"'
                      f',"{data["chr21"][c_iter]}"'
                      f',"{data["chr22"][c_iter]}"'
                      f',"{data["Chrx"][c_iter]}"'
                      f',"{data["chry"][c_iter]}"'
                      f',"{data["median_13"][c_iter]}"'
                      f',"{data["median_18"][c_iter]}"'
                      f',"{data["median_21"][c_iter]}"'
                      f',"{data["median_x"][c_iter]}"'
                      f',"{data["median_y"][c_iter]}"'
                      f',"{data["stdev_13"][c_iter]}"'
                      f',"{data["stdev_18"][c_iter]}"'
                      f',"{data["stdev_21"][c_iter]}"'
                      f',"{data["stdev_X"][c_iter]}"'
                      f',"{data["stdev_Y"][c_iter]}"'
                      f',"{ff_formatted}"')

        with open(file, 'w') as out:
            out.write('"' + '","'.join(header) + '"')
            indexid = 1
            index_counter = 0
            _print_row(indexid, c_index, out, index_counter)
            index_counter = 1
            for i in iter:
                indexid = indexid + 1
                next_barcode = data['flowcell_barcode'][i]
                if next_barcode != barcode:
                    out.write('\n"# Software version: 1.4.0; Configuration file version: VeriSeq NIPT Analysis Software (16 Samples)",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,')  # noqa
                    out.write('\n"# Disclosure: For Research Use Only. Not for use in diagnostic procedures.",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,')  # noqa
                    return i, next_barcode
                else:
                    _print_row(indexid, i, out, index_counter)
                    index_counter = index_counter + 1
            else:
                out.write('\n"# Software version: 1.4.0; Configuration file version: VeriSeq NIPT Analysis Software (16 Samples)",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,')  # noqa
                out.write('\n"# Disclosure: For Research Use Only. Not for use in diagnostic procedures.",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,')  # noqa
                return None, None

    marchine_name = "NDX" + "".join(map(str, np.random.randint(0, 5, 8)))
    if os.path.isfile("./test_data.csv"):
        data = pd.read_csv("./test_data.csv")
    elif os.path.isfile("./data/test_data.csv"):
        data = pd.read_csv("./data/test_data.csv")
    else:
        raise Exception("Could not find test_data.csv in current dir or data dir!")
    iterator = iter(data.index)
    run_counter = 1
    c_iter = next(iterator)
    barcode = data['flowcell_barcode'][c_iter]
    while barcode:
        filename = f"{date:%y%m%d}_{marchine_name}_{run_counter:04d}_{barcode}_NIPT_RESULT.csv"
        c_iter, barcode = print_file(filename, barcode, data, iterator, c_iter)
        date = date - timedelta(days=7)
        run_counter = run_counter + 1


if __name__ == "__main__":
    cli()
