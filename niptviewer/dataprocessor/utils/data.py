from pandas import read_csv, to_numeric
from django.db import IntegrityError, transaction
from decimal import Decimal
from ..models import Flowcell, BatchRun, SamplesRunData, Index, Flowcell, SampleType
import re
from io import StringIO
import datetime
import os

nnc_per_samplesheet = ['Library_nM']
c_sample_data = ['SampleID', 'Index','IndexID','Well','QCFailure','QCWarning', 'Description', 'SampleProject', 'SampleType']
nnc_per_sample = ['Ratio_13', 'Ratio_18', 'Ratio_21', 'Ratio_X', 'Ratio_Y',
                  'NCV_13', 'NCV_18', 'NCV_21', 'NCV_X', 'NCV_Y', 'FF_Formatted']
nnc_per_sample_qc = ['QCFlag', 'Clusters', 'TotalReads2Clusters',
                     'MaxMisindexedReads2Clusters','IndexedReads',
                     'TotalIndexedReads2Clusters', 'Tags', 'NonExcludedSites',
                     'NonExcludedSites2Tags', 'Tags2IndexedReads',
                     'PerfectMatchTags2Tags','GCBias', 'GCR2',
                     'NCD_13', 'NCD_18', 'NCD_21', 'NCD_X', 'NCD_Y',
                     ]
nnc_per_sample_scoring_metrics = ['Chr1', 'Chr2', 'Chr3', 'Chr4', 'Chr5',
                                  'Chr6', 'Chr7', 'Chr8', 'Chr9', 'Chr10',
                                  'Chr11', 'Chr12', 'Chr13', 'Chr14',
                                  'Chr15', 'Chr16', 'Chr17', 'Chr18',
                                  'Chr19', 'Chr20', 'Chr21', 'Chr22',
                                  'ChrX', 'ChrY',
                                  'Chr1_Coverage', 'Chr2_Coverage',
                                  'Chr3_Coverage', 'Chr4_Coverage',
                                  'Chr5_Coverage', 'Chr6_Coverage',
                                  'Chr7_Coverage', 'Chr8_Coverage',
                                  'Chr9_Coverage', 'Chr10_Coverage',
                                  'Chr11_Coverage', 'Chr12_Coverage',
                                  'Chr13_Coverage', 'Chr14_Coverage',
                                  'Chr15_Coverage', 'Chr16_Coverage',
                                  'Chr17_Coverage', 'Chr18_Coverage',
                                  'Chr19_Coverage', 'Chr20_Coverage',
                                  'Chr21_Coverage', 'Chr22_Coverage',
                                  'ChrX_Coverage', 'ChrY_Coverage']
nnc_per_batch_scoring_metrics = ['Median_13', 'Median_18', 'Median_21',
                                 'Median_X', 'Median_Y',
                                 'Stdev_13', 'Stdev_18', 'Stdev_21',
                                 'Stdev_X', 'Stdev_Y']
def decimal_from_value(value):
    if len(value) == 0:
        return None
    else:
        return Decimal(value)

def parse_niptool_csv(file=None, sep=","):
    run_date = re.search('^([0-9]+)_',os.path.basename(file.name))
    if run_date:
        run_date = datetime.datetime.strptime(run_date[1],"%y%m%d")
    data = read_csv(file,sep=sep, comment='#', decimal=".", float_precision='high', converters={'Library_nM': decimal_from_value})
    data.set_index('SampleID', drop=False)
    for sample in data['SampleID']:
        if "#" in sample and "version" in sample:
            version = re.search('Software[ ]version:[ ]([0-9.]+);', sample)[1]
    data = data[[not "#" in sample for sample in data['SampleID']]]
    data['Description'] = data['Description'].fillna("")
    data['QCFailure'] = data['QCFailure'].fillna("")
    data['QCWarning'] = data['QCWarning'].fillna("")
    data['SampleProject'] = data['SampleProject'].fillna("")
    data['FF_Formatted']=data['FF_Formatted'].apply(lambda x: int(x.replace('%','').replace('<',''))/100 if isinstance(x, str) else x)
    columns_to_process = nnc_per_samplesheet + nnc_per_sample + nnc_per_sample_qc +nnc_per_sample_scoring_metrics + nnc_per_batch_scoring_metrics
    data[columns_to_process]=data[columns_to_process].apply(to_numeric)
    return version, run_date, data

def import_data_into_database(user, file):
    version, run_date, data = parse_niptool_csv(file)
    try:
        with transaction.atomic():
            rundata =  data.loc[:, ['Flowcell'] + nnc_per_batch_scoring_metrics]

            flowcell_barcode = set([row['Flowcell'] for index, row in rundata.iterrows()])
            if len(flowcell_barcode) > 1:
                raise Exception("Multiple flowcell barcodes specified in the provided file: " + ", ".join(sorted(flowcell_barcode)))
            flowcell_barcode = flowcell_barcode.pop()

            if len(flowcell_barcode) != 9:
                raise Exception("Invalid Flowcell bardcode length, should be 9 chars, found: " + str(len(flowcell_barcode)))
            batch_data_error = []

            for column in nnc_per_batch_scoring_metrics:
                if len(set(rundata[column])) > 1:
                    batch_data_error.append(column)

            first_row = rundata.head(1)

            flowcell = Flowcell.create_flowcell(user=user, flowcell_barcode=flowcell_barcode, run_date=run_date)

            BatchRun.create_batch_run(flowcell_entry=flowcell,
                                        median_13=first_row['Median_13'].item(),
                                        median_18=first_row['Median_18'].item(),
                                        median_21=first_row['Median_21'].item(),
                                        median_x=first_row['Median_X'].item(),
                                        median_y=first_row['Median_Y'].item(),
                                        stdev_13=first_row['Stdev_13'].item(),
                                        stdev_18=first_row['Stdev_18'].item(),
                                        stdev_21=first_row['Stdev_21'].item(),
                                        stdev_X=first_row['Stdev_X'].item(),
                                        stdev_Y=first_row['Stdev_Y'].item(),
                                        software_version=version)
            fail = []
            warn = []
            for sample, row in data.loc[:, nnc_per_sample_scoring_metrics + nnc_per_sample_qc + nnc_per_sample + c_sample_data + nnc_per_samplesheet].iterrows():
                sample_type = SampleType.get_sample_type(name=row['SampleType'])
                index = Index.get_index(row['IndexID'],row['Index'])

                entry = SamplesRunData.create_sample_data(flowcell_id_entry=flowcell, sample_type_entry=sample_type, sample_id=row['SampleID'], sample_project=row["SampleProject"], index=index,
                    well=row['Well'], description=row['Description'], library_nm=row['Library_nM'], qc_flag=row['QCFlag'],
                    qc_failure=row['QCFailure'], qc_warning=row['QCWarning'],
                    ncv_13=row['NCV_13'], ncv_18=row['NCV_18'], ncv_21=row['NCV_21'], ncv_x=row['NCV_X'], ncv_y=row['NCV_Y'],
                    ratio_13=row['Ratio_13'], ratio_18=row['Ratio_18'], ratio_21=row['Ratio_21'], ratio_X=row['Ratio_X'], ratio_y=row['Ratio_Y'],
                    clusters=row['Clusters'], total_reads_2_clusters=row['TotalReads2Clusters'],
                    max_misindexed_reads_2_clusters=row['MaxMisindexedReads2Clusters'], indexed_reads=row['IndexedReads'],
                    total_indexed_reads_2_clusters=row['TotalIndexedReads2Clusters'], tags=row['Tags'],
                    non_excluded_sites=row['NonExcludedSites'], non_excluded_sites_2_tags=row['NonExcludedSites2Tags'],
                    tags_2_indexed_reads=row['Tags2IndexedReads'], perfect_match_tags_2_tags=row['PerfectMatchTags2Tags'],
                    gc_bias=row['GCBias'], gcr2=row['GCR2'], ncd_13=row['NCD_13'], ncd_18=row['NCD_18'], ncd_21=row['NCD_21'],
                    ncd_x=row['NCD_X'], ncd_y=row['NCD_Y'], chr1_coverage=row['Chr1_Coverage'], chr2_coverage=row['Chr2_Coverage'],
                    chr3_coverage=row['Chr3_Coverage'], chr4_coverage=row['Chr4_Coverage'], chr5_coverage=row['Chr5_Coverage'],
                    chr6_coverage=row['Chr6_Coverage'], chr7_coverage=row['Chr7_Coverage'], chr8_coverage=row['Chr8_Coverage'],
                    chr9_coverage=row['Chr9_Coverage'], chr10_coverage=row['Chr10_Coverage'], chr11_coverage=row['Chr11_Coverage'],
                    chr12_coverage=row['Chr12_Coverage'], chr13_coverage=row['Chr13_Coverage'], chr14_coverage=row['Chr14_Coverage'],
                    chr15_coverage=row['Chr15_Coverage'], chr16_coverage=row['Chr16_Coverage'], chr17_coverage=row['Chr17_Coverage'],
                    chr18_coverage=row['Chr18_Coverage'], chr19_coverage=row['Chr19_Coverage'], chr20_coverage=row['Chr20_Coverage'],
                    chr21_coverage=row['Chr21_Coverage'], chr22_coverage=row['Chr22_Coverage'], chrx_coverage=row['ChrX_Coverage'],
                    chry_coverage=row['ChrY_Coverage'], chr1=row['Chr1'], chr2=row['Chr2'], chr3=row['Chr3'], chr4=row['Chr4'],
                    chr5=row['Chr5'], chr6=row['Chr6'], chr7=row['Chr7'], chr8=row['Chr8'], chr9=row['Chr9'],
                    chr10=row['Chr10'], chr11=row['Chr11'], chr12=row['Chr12'], chr13=row['Chr13'], chr14=row['Chr14'],
                    chr15=row['Chr15'], chr16=row['Chr16'], chr17=row['Chr17'], chr18=row['Chr18'], chr19=row['Chr19'],
                    chr20=row['Chr20'], chr21=row['Chr21'], chr22=row['Chr22'], chrx=row['ChrX'], chry=row['ChrY'],
                    ff_formatted=row['FF_Formatted'])
                if not entry.qc_flag == 0:
                    if not entry.qc_failure == "":
                        fail.append(entry.qc_failure)
                    if not entry.qc_warning == "":
                        warn.append(entry.qc_warning)
            if len(fail) or len(warn):
                qc_status = []
                if len(fail):
                    qc_status.append("Failures (" + str(len(fail)) + ")")
                if len(warn):
                    qc_status.append("Warnings (" + str(len(warn)) + ")")
                flowcell.qc_status = ", ".join(qc_status)
                flowcell.save()
    except IntegrityError:
        return Flowcell.get_flowcell(flowcell_barcode)
    return flowcell.flowcell_barcode
