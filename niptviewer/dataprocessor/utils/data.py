from ..models import Flowcell, BatchRun, SamplesRunData, Index, Flowcell, SampleType, BatchRun
from decimal import Decimal
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from numpy import isnan
from pandas import read_csv, to_numeric
from scipy import stats
import datetime
import os
import re

nnc_per_samplesheet = ['Library_nM']
c_sample_data = ['SampleID', 'Index', 'IndexID', 'Well', 'QCFailure', 'QCWarning', 'Description', 'SampleProject', 'SampleType']
nnc_per_sample = ['Ratio_13', 'Ratio_18', 'Ratio_21', 'Ratio_X', 'Ratio_Y',
                  'NCV_13', 'NCV_18', 'NCV_21', 'NCV_X', 'NCV_Y', 'FF_Formatted']
nnc_per_sample_qc = ['QCFlag', 'Clusters', 'TotalReads2Clusters',
                     'MaxMisindexedReads2Clusters', 'IndexedReads',
                     'TotalIndexedReads2Clusters', 'Tags', 'NonExcludedSites',
                     'NonExcludedSites2Tags', 'Tags2IndexedReads',
                     'PerfectMatchTags2Tags', 'GCBias', 'GCR2',
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

current_version = "v2"

csv_header_flowcell = {current_version: [
    "UserID", "UserName", "SoftwareVersion",
    "SampleID", "SampleType", "Flowcell", "Created", "RunDate", "Description",
    "SampleProject", "IndexID", "Index", "Well",
    "Library_nM", "QCFlag", "QCFailure", "QCWarning",
    "NCV_13", "NCV_18", "NCV_21", "NCV_X", "NCV_Y",
    "Ratio_13", "Ratio_18", "Ratio_21", "Ratio_X", "Ratio_Y",
    "Clusters", "TotalReads2Clusters", "MaxMisindexedReads2Clusters", "IndexedReads",
    "TotalIndexedReads2Clusters", "Tags", "NonExcludedSites", "NonExcludedSites2Tags", "Tags2IndexedReads",
    "PerfectMatchTags2Tags", "GCBias", "GCR2",
    "NCD_13", "NCD_18", "NCD_21", "NCD_X", "NCD_Y",
    "Chr1_Coverage", "Chr2_Coverage", "Chr3_Coverage", "Chr4_Coverage", "Chr5_Coverage",
    "Chr6_Coverage", "Chr7_Coverage", "Chr8_Coverage", "Chr9_Coverage", "Chr10_Coverage",
    "Chr11_Coverage", "Chr12_Coverage", "Chr13_Coverage", "Chr14_Coverage", "Chr15_Coverage",
    "Chr16_Coverage", "Chr17_Coverage", "Chr18_Coverage", "Chr19_Coverage", "Chr20_Coverage",
    "Chr21_Coverage", "Chr22_Coverage", "ChrX_Coverage", "ChrY_Coverage",
    "Chr1", "Chr2", "Chr3", "Chr4", "Chr5", "Chr6", "Chr7", "Chr8", "Chr9", "Chr10",
    "Chr11", "Chr12", "Chr13", "Chr14", "Chr15", "Chr16", "Chr17", "Chr18", "Chr19", "Chr20",
    "Chr21", "Chr22", "ChrX", "ChrY",
    "Median_13", "Median_18", "Median_21", "Median_X", "Median_Y",
    "Stdev_13", "Stdev_18", "Stdev_21", "Stdev_X", "Stdev_Y", "FF_Formatted"]}


def decimal_from_value(value):
    if len(value) == 0:
        return None
    elif value == 'None':
        return None
    else:
        return Decimal(value)


def parse_niptool_csv(file=None, sep=","):
    run_date = re.search('^([0-9]+)_', os.path.basename(file.name))
    if run_date:
        run_date = datetime.datetime.strptime(run_date[1], "%y%m%d")
    data = read_csv(file, sep=sep, comment='#', decimal=".", float_precision='high',
                    converters={'Library_nM': decimal_from_value})
    data.set_index('SampleID', drop=False)
    for sample in data['SampleID']:
        if "#" in sample and "version" in sample:
            version = re.search('Software[ ]version:[ ]([0-9.]+);', sample)[1]
    data = data[["#" not in sample for sample in data['SampleID']]]
    data['Description'] = data['Description'].fillna("")
    data['QCFailure'] = data['QCFailure'].fillna("")
    data['QCWarning'] = data['QCWarning'].fillna("")
    data['SampleProject'] = data['SampleProject'].fillna("")
    data['FF_Formatted'] = data['FF_Formatted'].apply(
        lambda x: int(x.replace('%', '').replace('<', '')) / 100 if isinstance(x, str) else x)
    columns_to_process = nnc_per_samplesheet + \
        nnc_per_sample + \
        nnc_per_sample_qc + \
        nnc_per_sample_scoring_metrics + \
        nnc_per_batch_scoring_metrics
    data[columns_to_process] = data[columns_to_process].apply(to_numeric)
    return version, run_date, data


def import_data_into_database(user, file, skip_samples=False):
    version, run_date, data = parse_niptool_csv(file)
    num_imported_samples = 0
    try:
        with transaction.atomic():
            rundata = data.loc[:, ['Flowcell'] + nnc_per_batch_scoring_metrics]
            flowcell_barcode = set([row['Flowcell'] for index, row in rundata.iterrows()])
            if len(flowcell_barcode) > 1:
                raise Exception(
                    "Multiple flowcell barcodes specified in the provided file: " + ", ".join(sorted(flowcell_barcode)))
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
            for sample, row in data.loc[:, nnc_per_sample_scoring_metrics +
                                        nnc_per_sample_qc + nnc_per_sample +
                                        c_sample_data + nnc_per_samplesheet].iterrows():
                sample_type = SampleType.get_sample_type(name=row['SampleType'])
                index = Index.get_index(row['IndexID'], row['Index'])
                if isnan(row['QCFlag']) and skip_samples:
                    continue
                try:
                    entry = SamplesRunData.create_sample_data(flowcell_id_entry=flowcell, sample_type_entry=sample_type,
                                                              sample_id=row['SampleID'], sample_project=row["SampleProject"],
                                                              index=index,
                                                              well=row['Well'], description=row['Description'],
                                                              library_nm=row['Library_nM'], qc_flag=row['QCFlag'],
                                                              qc_failure=row['QCFailure'], qc_warning=row['QCWarning'],
                                                              ncv_13=row['NCV_13'], ncv_18=row['NCV_18'], ncv_21=row['NCV_21'],
                                                              ncv_x=row['NCV_X'], ncv_y=row['NCV_Y'],
                                                              ratio_13=row['Ratio_13'], ratio_18=row['Ratio_18'],
                                                              ratio_21=row['Ratio_21'], ratio_X=row['Ratio_X'],
                                                              ratio_y=row['Ratio_Y'],
                                                              clusters=row['Clusters'],
                                                              total_reads_2_clusters=row['TotalReads2Clusters'],
                                                              max_misindexed_reads_2_clusters=row['MaxMisindexedReads2Clusters'],
                                                              indexed_reads=row['IndexedReads'],
                                                              total_indexed_reads_2_clusters=row['TotalIndexedReads2Clusters'],
                                                              tags=row['Tags'],
                                                              non_excluded_sites=row['NonExcludedSites'],
                                                              non_excluded_sites_2_tags=row['NonExcludedSites2Tags'],
                                                              tags_2_indexed_reads=row['Tags2IndexedReads'],
                                                              perfect_match_tags_2_tags=row['PerfectMatchTags2Tags'],
                                                              gc_bias=row['GCBias'], gcr2=row['GCR2'], ncd_13=row['NCD_13'],
                                                              ncd_18=row['NCD_18'], ncd_21=row['NCD_21'],
                                                              ncd_x=row['NCD_X'], ncd_y=row['NCD_Y'],
                                                              chr1_coverage=row['Chr1_Coverage'],
                                                              chr2_coverage=row['Chr2_Coverage'],
                                                              chr3_coverage=row['Chr3_Coverage'],
                                                              chr4_coverage=row['Chr4_Coverage'],
                                                              chr5_coverage=row['Chr5_Coverage'],
                                                              chr6_coverage=row['Chr6_Coverage'],
                                                              chr7_coverage=row['Chr7_Coverage'],
                                                              chr8_coverage=row['Chr8_Coverage'],
                                                              chr9_coverage=row['Chr9_Coverage'],
                                                              chr10_coverage=row['Chr10_Coverage'],
                                                              chr11_coverage=row['Chr11_Coverage'],
                                                              chr12_coverage=row['Chr12_Coverage'],
                                                              chr13_coverage=row['Chr13_Coverage'],
                                                              chr14_coverage=row['Chr14_Coverage'],
                                                              chr15_coverage=row['Chr15_Coverage'],
                                                              chr16_coverage=row['Chr16_Coverage'],
                                                              chr17_coverage=row['Chr17_Coverage'],
                                                              chr18_coverage=row['Chr18_Coverage'],
                                                              chr19_coverage=row['Chr19_Coverage'],
                                                              chr20_coverage=row['Chr20_Coverage'],
                                                              chr21_coverage=row['Chr21_Coverage'],
                                                              chr22_coverage=row['Chr22_Coverage'],
                                                              chrx_coverage=row['ChrX_Coverage'],
                                                              chry_coverage=row['ChrY_Coverage'],
                                                              chr1=row['Chr1'], chr2=row['Chr2'],
                                                              chr3=row['Chr3'], chr4=row['Chr4'],
                                                              chr5=row['Chr5'], chr6=row['Chr6'],
                                                              chr7=row['Chr7'], chr8=row['Chr8'],
                                                              chr9=row['Chr9'],
                                                              chr10=row['Chr10'], chr11=row['Chr11'], chr12=row['Chr12'],
                                                              chr13=row['Chr13'], chr14=row['Chr14'],
                                                              chr15=row['Chr15'], chr16=row['Chr16'], chr17=row['Chr17'],
                                                              chr18=row['Chr18'], chr19=row['Chr19'],
                                                              chr20=row['Chr20'], chr21=row['Chr21'], chr22=row['Chr22'],
                                                              chrx=row['ChrX'], chry=row['ChrY'],
                                                              ff_formatted=row['FF_Formatted'])
                    num_imported_samples += 1
                except ValueError as err:
                    if skip_samples:
                        pass
                    else:
                        raise ValueError(row['SampleID'] + ": " + str(err))
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
            if num_imported_samples == 0:
                raise ValueError("No samples imported")
            create_trendlines()
    except IntegrityError as e:
        raise e
    return flowcell.flowcell_barcode


def export_flowcell_data():
    yield("##User export")
    yield(",".join(['#id', "username", "first_name", "last_name", "email"]))
    for user in User.objects.all():
        yield(",".join([
            str(user.id),
            user.username,
            user.first_name,
            user.last_name,
            user.email
        ]))
    flowcells = Flowcell.objects.all().order_by('-run_date')
    yield("##Flowcell data export: " + current_version)
    yield("#" + ",".join(csv_header_flowcell[current_version]))
    for flowcell in flowcells:
        batch = BatchRun.objects.filter(flowcell_id=flowcell.pk)
        if len(batch) != 1:
            raise Exception("Incorrect size of batch")
        batch = batch[0]
        samples = SamplesRunData.objects.filter(flowcell_id=flowcell.pk)
        for sample in samples:
            yield(",".join([
                str(flowcell.uploading_user.id),
                flowcell.uploading_user.username,
                batch.software_version,
                sample.sample_id,
                sample.sample_type.name,
                flowcell.flowcell_barcode,
                str(flowcell.created),
                str(flowcell.run_date),
                sample.description,
                sample.sample_project,
                sample.index.index_id,
                sample.index.index,
                sample.well,
                str(sample.library_nm),
                str(sample.qc_flag),
                sample.qc_failure,
                sample.qc_warning,
                str(sample.ncv_13),
                str(sample.ncv_18),
                str(sample.ncv_21),
                str(sample.ncv_X),
                str(sample.ncv_Y),
                str(sample.ratio_13),
                str(sample.ratio_18),
                str(sample.ratio_21),
                str(sample.ratio_X),
                str(sample.ratio_y),
                str(sample.clusters),
                str(sample.total_reads_2_clusters),
                str(sample.max_misindexed_reads_2_clusters),
                str(sample.indexed_reads),
                str(sample.total_indexed_reads_2_clusters),
                str(sample.tags),
                str(sample.non_excluded_sites),
                str(sample.non_excluded_sites_2_tags),
                str(sample.tags_2_indexed_reads),
                str(sample.perfect_match_tags_2_tags),
                str(sample.gc_bias),
                str(sample.gcr2),
                str(sample.ncd_13),
                str(sample.ncd_18),
                str(sample.ncd_21),
                str(sample.ncd_x),
                str(sample.ncd_y),
                str(sample.chr1_coverage),
                str(sample.chr2_coverage),
                str(sample.chr3_coverage),
                str(sample.chr4_coverage),
                str(sample.chr5_coverage),
                str(sample.chr6_coverage),
                str(sample.chr7_coverage),
                str(sample.chr8_coverage),
                str(sample.chr9_coverage),
                str(sample.chr10_coverage),
                str(sample.chr11_coverage),
                str(sample.chr12_coverage),
                str(sample.chr13_coverage),
                str(sample.chr14_coverage),
                str(sample.chr15_coverage),
                str(sample.chr16_coverage),
                str(sample.chr17_coverage),
                str(sample.chr18_coverage),
                str(sample.chr19_coverage),
                str(sample.chr20_coverage),
                str(sample.chr21_coverage),
                str(sample.chr22_coverage),
                str(sample.chrx_coverage),
                str(sample.chry_coverage),
                str(sample.chr1),
                str(sample.chr2),
                str(sample.chr3),
                str(sample.chr4),
                str(sample.chr5),
                str(sample.chr6),
                str(sample.chr7),
                str(sample.chr8),
                str(sample.chr9),
                str(sample.chr10),
                str(sample.chr11),
                str(sample.chr12),
                str(sample.chr13),
                str(sample.chr14),
                str(sample.chr15),
                str(sample.chr16),
                str(sample.chr17),
                str(sample.chr18),
                str(sample.chr19),
                str(sample.chr20),
                str(sample.chr21),
                str(sample.chr22),
                str(sample.Chrx),
                str(sample.chry),
                str(batch.median_13),
                str(batch.median_18),
                str(batch.median_21),
                str(batch.median_x),
                str(batch.median_y),
                str(batch.stdev_13),
                str(batch.stdev_18),
                str(batch.stdev_21),
                str(batch.stdev_X),
                str(batch.stdev_Y),
                str(sample.ff_formatted)
            ]))


def import_flowcell_export(file_handle):
    def compare_flowcell(flowcell, columns, header_map, user_information):
        if flowcell.uploading_user.username == user_information[columns[header_map["UserName"]]].username and \
           flowcell.flowcell_barcode == columns[header_map["Flowcell"]] and \
           flowcell.run_date.strftime('%Y-%m-%d') == \
           datetime.datetime.strptime(columns[header_map["RunDate"]], '%Y-%m-%d %H:%M:%S+00:00').strftime('%Y-%m-%d') and \
           flowcell.created.strftime('%Y-%m-%d') == \
           datetime.datetime.strptime(columns[header_map["Created"]], '%Y-%m-%d %H:%M:%S.%f+00:00').strftime('%Y-%m-%d'):
            pass
        else:
            raise Exception("flowcell information inconsistent for flowcell: " + columns[header_map['Flowcell']] +
                            "\n" +
                            str([(flowcell.uploading_user.username, user_information[columns[header_map["UserName"]]]),
                                (flowcell.flowcell_barcode, columns[header_map["Flowcell"]]),
                                str(flowcell.run_date),
                                columns[header_map["RunDate"]],
                                str(flowcell.created),
                                columns[header_map["Created"]]
                                 ]
                                )
                            )

    def compare_batch(batch, columns, header_map):
        if (abs(float(batch.median_13) - float(columns[header_map["Median_13"]] if columns[header_map["Median_13"]] not in ["nan", "NaN"] else 0)) < 0.00000001 and  # noqa
           abs(float(batch.median_18) - float(columns[header_map["Median_18"]] if columns[header_map["Median_18"]] not in ["nan", "NaN"] else 0)) < 0.00000001 and  # noqa
           abs(float(batch.median_21) - float(columns[header_map["Median_21"]] if columns[header_map["Median_21"]] not in ["nan", "NaN"] else 0)) < 0.00000001 and  # noqa
           abs(float(batch.median_x) - float(columns[header_map["Median_X"]] if columns[header_map["Median_X"]] not in ["nan", "NaN"] else 0)) < 0.00000001 and  # noqa
           abs(float(batch.median_y) - float(columns[header_map["Median_Y"]] if columns[header_map["Median_Y"]] not in ["nan", "NaN"] else 0)) < 0.00000001 and  # noqa
           abs(float(batch.stdev_13) - float(columns[header_map["Stdev_13"]] if columns[header_map["Stdev_13"]] not in ["nan", "NaN"] else 0)) < 0.00000001 and  # noqa
           abs(float(batch.stdev_18) - float(columns[header_map["Stdev_18"]] if columns[header_map["Stdev_18"]] not in ["nan", "NaN"] else 0)) < 0.00000001 and  # noqa
           abs(float(batch.stdev_21) - float(columns[header_map["Stdev_21"]] if columns[header_map["Stdev_21"]] not in ["nan", "NaN"] else 0)) < 0.00000001 and  # noqa
           abs(float(batch.stdev_X) - float(columns[header_map["Stdev_X"]] if columns[header_map["Stdev_X"]] not in ["nan", "NaN"] else 0)) < 0.00000001 and  # noqa
           abs(float(batch.stdev_Y) - float(columns[header_map["Stdev_Y"]] if columns[header_map["Stdev_Y"]] not in ["nan", "NaN"] else 0)) < 0.00000001 and  # noqa
           batch.software_version == columns[header_map["SoftwareVersion"]]):
            pass
        else:
            raise Exception("batch information inconsistent for flowcell: " +
                            columns[header_map['Flowcell']] + "\n" +
                            str([(batch.median_13, columns[header_map["Median_13"]]),
                                 (batch.median_18, columns[header_map["Median_18"]]),
                                 (batch.median_21, columns[header_map["Median_21"]]),
                                 (batch.median_x, columns[header_map["Median_X"]]),
                                 (batch.median_y, columns[header_map["Median_Y"]]),
                                 (batch.stdev_13, columns[header_map["Stdev_13"]]),
                                 (batch.stdev_18, columns[header_map["Stdev_18"]]),
                                 (batch.stdev_21, columns[header_map["Stdev_21"]]),
                                 (batch.stdev_X, columns[header_map["Stdev_X"]]),
                                 (batch.stdev_Y, columns[header_map["Stdev_Y"]]),
                                 (batch.software_version, columns[header_map["SoftwareVersion"]])])
                            )

    def create_sample(columns, flowcell):
        type = SampleType.get_sample_type(columns[header_map["SampleType"]])
        index = Index.get_index(columns[header_map["IndexID"]], columns[header_map["Index"]])

        SamplesRunData.create_sample_data(
            flowcell_id_entry=flowcell,
            sample_type_entry=type,
            sample_id=columns[header_map["SampleID"]],
            sample_project=columns[header_map["SampleProject"]],
            index=index,
            well=columns[header_map["Well"]],
            description=columns[header_map["Description"]],
            library_nm=decimal_from_value(columns[header_map["Library_nM"]]),
            qc_flag=columns[header_map["QCFlag"]],
            qc_failure=columns[header_map["QCFailure"]],
            qc_warning=columns[header_map["QCWarning"]],
            ncv_13=decimal_from_value(columns[header_map["NCV_13"]]),
            ncv_18=decimal_from_value(columns[header_map["NCV_18"]]),
            ncv_21=decimal_from_value(columns[header_map["NCV_21"]]),
            ncv_x=decimal_from_value(columns[header_map["NCV_X"]]),
            ncv_y=decimal_from_value(columns[header_map["NCV_Y"]]),
            ratio_13=decimal_from_value(columns[header_map["Ratio_13"]]),
            ratio_18=decimal_from_value(columns[header_map["Ratio_18"]]),
            ratio_21=decimal_from_value(columns[header_map["Ratio_21"]]),
            ratio_X=decimal_from_value(columns[header_map["Ratio_X"]]),
            ratio_y=decimal_from_value(columns[header_map["Ratio_Y"]]),
            clusters=decimal_from_value(columns[header_map["Clusters"]]),
            total_reads_2_clusters=decimal_from_value(columns[header_map["TotalReads2Clusters"]]),
            max_misindexed_reads_2_clusters=decimal_from_value(columns[header_map["MaxMisindexedReads2Clusters"]]),
            indexed_reads=columns[header_map["IndexedReads"]],
            total_indexed_reads_2_clusters=decimal_from_value(columns[header_map["TotalIndexedReads2Clusters"]]),
            tags=columns[header_map["Tags"]],
            non_excluded_sites=columns[header_map["NonExcludedSites"]],
            non_excluded_sites_2_tags=decimal_from_value(columns[header_map["NonExcludedSites2Tags"]]),
            tags_2_indexed_reads=decimal_from_value(columns[header_map["Tags2IndexedReads"]]),
            perfect_match_tags_2_tags=decimal_from_value(columns[header_map["PerfectMatchTags2Tags"]]),
            gc_bias=decimal_from_value(columns[header_map["GCBias"]]),
            gcr2=decimal_from_value(columns[header_map["GCR2"]]),
            ncd_13=decimal_from_value(columns[header_map["NCD_13"]]),
            ncd_18=decimal_from_value(columns[header_map["NCD_18"]]),
            ncd_21=decimal_from_value(columns[header_map["NCD_21"]]),
            ncd_x=decimal_from_value(columns[header_map["NCD_X"]]),
            ncd_y=decimal_from_value(columns[header_map["NCD_Y"]]),
            chr1_coverage=decimal_from_value(columns[header_map["Chr1_Coverage"]]),
            chr2_coverage=decimal_from_value(columns[header_map["Chr2_Coverage"]]),
            chr3_coverage=decimal_from_value(columns[header_map["Chr3_Coverage"]]),
            chr4_coverage=decimal_from_value(columns[header_map["Chr4_Coverage"]]),
            chr5_coverage=decimal_from_value(columns[header_map["Chr5_Coverage"]]),
            chr6_coverage=decimal_from_value(columns[header_map["Chr6_Coverage"]]),
            chr7_coverage=decimal_from_value(columns[header_map["Chr7_Coverage"]]),
            chr8_coverage=decimal_from_value(columns[header_map["Chr8_Coverage"]]),
            chr9_coverage=decimal_from_value(columns[header_map["Chr9_Coverage"]]),
            chr10_coverage=decimal_from_value(columns[header_map["Chr10_Coverage"]]),
            chr11_coverage=decimal_from_value(columns[header_map["Chr11_Coverage"]]),
            chr12_coverage=decimal_from_value(columns[header_map["Chr12_Coverage"]]),
            chr13_coverage=decimal_from_value(columns[header_map["Chr13_Coverage"]]),
            chr14_coverage=decimal_from_value(columns[header_map["Chr14_Coverage"]]),
            chr15_coverage=decimal_from_value(columns[header_map["Chr15_Coverage"]]),
            chr16_coverage=decimal_from_value(columns[header_map["Chr16_Coverage"]]),
            chr17_coverage=decimal_from_value(columns[header_map["Chr17_Coverage"]]),
            chr18_coverage=decimal_from_value(columns[header_map["Chr18_Coverage"]]),
            chr19_coverage=decimal_from_value(columns[header_map["Chr19_Coverage"]]),
            chr20_coverage=decimal_from_value(columns[header_map["Chr20_Coverage"]]),
            chr21_coverage=decimal_from_value(columns[header_map["Chr21_Coverage"]]),
            chr22_coverage=decimal_from_value(columns[header_map["Chr22_Coverage"]]),
            chrx_coverage=decimal_from_value(columns[header_map["ChrX_Coverage"]]),
            chry_coverage=decimal_from_value(columns[header_map["ChrY_Coverage"]]),
            chr1=columns[header_map["Chr1"]],
            chr2=columns[header_map["Chr2"]],
            chr3=columns[header_map["Chr3"]],
            chr4=columns[header_map["Chr4"]],
            chr5=columns[header_map["Chr5"]],
            chr6=columns[header_map["Chr6"]],
            chr7=columns[header_map["Chr7"]],
            chr8=columns[header_map["Chr8"]],
            chr9=columns[header_map["Chr9"]],
            chr10=columns[header_map["Chr10"]],
            chr11=columns[header_map["Chr11"]],
            chr12=columns[header_map["Chr12"]],
            chr13=columns[header_map["Chr13"]],
            chr14=columns[header_map["Chr14"]],
            chr15=columns[header_map["Chr15"]],
            chr16=columns[header_map["Chr16"]],
            chr17=columns[header_map["Chr17"]],
            chr18=columns[header_map["Chr18"]],
            chr19=columns[header_map["Chr19"]],
            chr20=columns[header_map["Chr20"]],
            chr21=columns[header_map["Chr21"]],
            chr22=columns[header_map["Chr22"]],
            chrx=columns[header_map["ChrX"]],
            chry=columns[header_map["ChrY"]],
            ff_formatted=decimal_from_value(columns[header_map["FF_Formatted"]])
        )
    first_line = next(file_handle)
    if not first_line.startswith("##User export"):
        raise Exception("Missing user information at start of file")
    user_information = {}
    version = None
    for line in file_handle:
        line = line.rstrip("\n")
        line = line.lstrip("\"").rstrip('"')
        if line.startswith("#id"):
            continue
        if line.startswith("##Flowcell data export"):
            try:
                version = re.search('Flowcell data export: (v[0-9]+)', line).group(1)
            except AttributeError:
                raise Exception("Could not extract version from line: " + line)
            break
        columns = line.rstrip().split(",")
        user = User.objects.filter(id=int(columns[0]))
        if len(user) > 0:
            user = user[0]
            if user.username != columns[1]:
                raise Exception("Inconsistent user information:, found user " +
                                user.username + " with id " + columns[0] +
                                ", trying to import user with username " + columns[1] + " with id " + columns[0])
        else:
            user = User.objects.create(id=int(columns[0]), username=columns[1], first_name=columns[2], last_name=columns[3])
        user_information[user.username] = user

    flowcell = None

    header_line = next(file_handle)
    header_line = header_line.rstrip().strip('"')
    if not header_line.rstrip() == "#" + ",".join(csv_header_flowcell[version]):
        raise Exception("Flowcell columns mismatch, found\n" +
                        header_line +
                        "\nExpected: \n" +
                        "#" + ",".join(csv_header_flowcell[version]))
    header_map = {key: value for key, value in zip(csv_header_flowcell[version], range(0, len(csv_header_flowcell[version])))}

    for line in file_handle:
        line = line.rstrip("\n")
        line = line.lstrip("\"").rstrip('"')
        if line.startswith("#UserID"):
            continue
        columns = line.rstrip().split(",")
        if len(columns) == 0:
            return
        flowcell = Flowcell.objects.filter(flowcell_barcode=columns[header_map["Flowcell"]]).first()
        if flowcell is None:
            flowcell = Flowcell.create_flowcell(
                user=user_information[columns[header_map["UserName"]]],
                flowcell_barcode=columns[header_map["Flowcell"]],
                run_date=columns[header_map["RunDate"]],
                upload_date=columns[header_map["Created"]]
            )
            batch = BatchRun.create_batch_run(
                flowcell_entry=flowcell,
                median_13=columns[header_map["Median_13"]] if columns[header_map["Median_13"]] not in ["nan", "NaN"] else 0,
                median_18=columns[header_map["Median_18"]] if columns[header_map["Median_18"]] not in ["nan", "NaN"] else 0,
                median_21=columns[header_map["Median_21"]] if columns[header_map["Median_21"]] not in ["nan", "NaN"] else 0,
                median_x=columns[header_map["Median_X"]] if columns[header_map["Median_X"]] not in ["nan", "NaN"] else 0,
                median_y=columns[header_map["Median_Y"]] if columns[header_map["Median_Y"]] not in ["nan", "NaN"] else 0,
                stdev_13=columns[header_map["Stdev_13"]] if columns[header_map["Stdev_13"]] not in ["nan", "NaN"] else 0,
                stdev_18=columns[header_map["Stdev_18"]] if columns[header_map["Stdev_18"]] not in ["nan", "NaN"] else 0,
                stdev_21=columns[header_map["Stdev_21"]] if columns[header_map["Stdev_21"]] not in ["nan", "NaN"] else 0,
                stdev_X=columns[header_map["Stdev_X"]] if columns[header_map["Stdev_X"]] not in ["nan", "NaN"] else 0,
                stdev_Y=columns[header_map["Stdev_Y"]] if columns[header_map["Stdev_Y"]] not in ["nan", "NaN"] else 0,
                software_version=columns[header_map["SoftwareVersion"]]
            )
            create_sample(columns, flowcell)
        else:
            compare_flowcell(flowcell, columns, header_map, user_information)
            batch = BatchRun.objects.get(flowcell_id=flowcell)
            compare_batch(batch, columns, header_map)
            create_sample(columns, flowcell)
    create_trendlines()


def generate_regression_line_from_sample_data(samples,
                                              x_value=lambda v: getattr(v, 'ncv_X'),
                                              y_value=lambda v: getattr(v, 'ncv_Y'),
                                              filter=lambda v: getattr(v, 'ncv_Y') is not None and
                                              getattr(v, 'ncv_Y') > 3.0 and
                                              getattr(v, 'ncv_X') is not None and
                                              getattr(v, 'ncv_X') > -25.0):
    x_value_list = list()
    y_value_list = list()
    for sample in samples:
        if filter(sample):
            x_value_list.append(float(x_value(sample)))
            y_value_list.append(float(y_value(sample)))
    return stats.linregress(x_value_list, y_value_list)


def create_trendlines():
    from ..models import Line
    import math
    all_samples = SamplesRunData.objects.all()
    slope, intercept, r_value, p_value, std_err = generate_regression_line_from_sample_data(all_samples)
    stdev = math.sqrt(len(all_samples))*std_err
    Line.create_or_update_line(type="x_vs_y",
                               slope=slope,
                               intercept=intercept,
                               stderr=std_err,
                               stdev=stdev,
                               p_value=p_value,
                               r_value=r_value)
