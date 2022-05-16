from django.db import models
from django.contrib.auth.models import User
import pandas
import datetime


class Flowcell(models.Model):
    flowcell_barcode = models.CharField(max_length=9, help_text="Flowcell identification.", blank=False, unique=True)
    uploading_user = models.ForeignKey(User, on_delete=models.RESTRICT, null=False, blank=False, default=1,
                                       help_text="User that uploaded the flowcell identification.",)
    qc_status = models.CharField(help_text="QC summary for samples", max_length=200, blank=False, default="PASS")
    created = models.DateTimeField(auto_now_add=True)
    run_date = models.DateTimeField(blank=False)

    def __str__(self):
        return "{} {}".format(self.flowcell_barcode, self.run_date.strftime("%Y-%m-%d %H:%M"))

    def create_flowcell(user, flowcell_barcode, run_date=None, upload_date=None):
        if upload_date is None:
            return Flowcell.objects.create(uploading_user=user, flowcell_barcode=flowcell_barcode, run_date=run_date)
        else:
            flowcell = Flowcell.objects.create(uploading_user=user, flowcell_barcode=flowcell_barcode, run_date=run_date)
            flowcell.created = datetime.datetime.strptime(upload_date, '%Y-%m-%d %H:%M:%S.%f+00:00')
            flowcell.save(update_fields=['created'])
            return flowcell

    def get_flowcell(flowcell_barcode):
        return Flowcell.objects.get(flowcell_barcode=flowcell_barcode)

    def save(self, *args, **kwargs):
        if not self.id and not self.run_date:
            self.run_date = timezone.now()
        return super(Flowcell, self).save(*args, **kwargs)


class SampleType(models.Model):
    name = models.CharField(max_length=9, help_text="Sample type.", blank=False, unique=True)

    def __str__(self):
        return self.name

    def create_sample_type(name):
        return SampleType.objects.create(name=name)

    def get_sample_type(name):
        return SampleType.objects.filter(name=name)[0]


class Index(models.Model):
    index_id = models.CharField(max_length=6, help_text="Index id.", blank=False, unique=True)
    index = models.CharField(max_length=6, help_text="Index sequence.", blank=False, unique=True)

    def __str__(self):
        return self.index

    def create_index(index_id, index):
        return Index.objects.create(index_id=index_id, index=index)

    def get_index(index_id, index):
        return Index.objects.get(index_id=index_id, index=index)


class BatchRun(models.Model):
    __help_text_median = "Batch median of chromosomal ratios for putative diploid samples. ChrX and chrY are based on " + \
                         "putative female samples only."
    __help_text_stdev = "Batch standard deviation of chromosomal ratios for putative diploid samples. ChrX and chrY based on " +\
                        "putative female samples only"
    flowcell_id = models.ForeignKey(Flowcell, on_delete=models.CASCADE, help_text="Flowcell ID")
    median_13 = models.DecimalField(blank=False, help_text=__help_text_median, max_digits=25, decimal_places=20)
    median_18 = models.DecimalField(blank=False, help_text=__help_text_median, max_digits=25, decimal_places=20)
    median_21 = models.DecimalField(blank=False, help_text=__help_text_median, max_digits=25, decimal_places=20)
    median_x = models.DecimalField(blank=False, help_text=__help_text_median, max_digits=25, decimal_places=20)
    median_y = models.DecimalField(blank=False, help_text=__help_text_median, max_digits=25, decimal_places=20)
    stdev_13 = models.FloatField(blank=False, help_text=__help_text_stdev)
    stdev_18 = models.FloatField(blank=False, help_text=__help_text_stdev)
    stdev_21 = models.FloatField(blank=False, help_text=__help_text_stdev)
    stdev_X = models.FloatField(blank=False, help_text=__help_text_stdev)
    stdev_Y = models.FloatField(blank=False, help_text=__help_text_stdev)
    software_version = models.CharField(help_text="Illumina analysis software version", max_length=10, blank=False)

    def __str__(self):
        return self.software_version + ";" + str(self.flowcell_id)

    def create_batch_run(flowcell_entry, median_13, median_18, median_21,
                         median_x, median_y, stdev_13, stdev_18, stdev_21,
                         stdev_X, stdev_Y, software_version):
        return BatchRun.objects.create(flowcell_id=flowcell_entry,
                                       median_13=median_13,
                                       median_18=median_18,
                                       median_21=median_21,
                                       median_x=median_x,
                                       median_y=median_y,
                                       stdev_13=stdev_13,
                                       stdev_18=stdev_18,
                                       stdev_21=stdev_21,
                                       stdev_X=stdev_X,
                                       stdev_Y=stdev_Y,
                                       software_version=software_version)


class SamplesRunData(models.Model):
    __help_text_chr = "Total number of NonExcludedSites used for analysis of a corresponding chromosome (integer value)"
    __help_text_chr_coverage = "Normalized coverage of each chromosome used in evaluation of chromosomal ratios"
    flowcell_id = models.ForeignKey(Flowcell, on_delete=models.CASCADE, help_text="Flowcell ID")
    sample_type = models.ForeignKey(SampleType, on_delete=models.CASCADE, help_text="Flowcell ID")
    sample_id = models.CharField(help_text="SampleID", max_length=20)
    sample_project = models.CharField(help_text="SampleID", max_length=20, default="")
    index = models.ForeignKey(Index, on_delete=models.CASCADE, help_text="Index used")
    well = models.CharField(help_text="Well id", max_length=10)
    description = models.TextField(help_text="Description.", blank=False, unique=False, default="")
    library_nm = models.DecimalField(blank=False, max_digits=25, decimal_places=20)
    qc_flag = models.IntegerField(choices=((0, 'Pass'), (1, 'Warning'), (2, 'Failure')), blank=False, unique=False)
    qc_failure = models.TextField(help_text="Description.", blank=False, unique=False, default="")
    qc_warning = models.TextField(help_text="Description.", blank=False, unique=False, default="")
    ncv_13 = models.DecimalField(blank=True, null=True,
                                 help_text="Normalized Chromosomal Value (z-score) 13", max_digits=25, decimal_places=20)
    ncv_18 = models.DecimalField(blank=True, null=True,
                                 help_text="Normalized Chromosomal Value (z-score) 18", max_digits=25, decimal_places=20)
    ncv_21 = models.DecimalField(blank=True, null=True,
                                 help_text="Normalized Chromosomal Value (z-score) 21", max_digits=25, decimal_places=20)
    ncv_X = models.DecimalField(blank=True, null=True,
                                help_text="Normalized Chromosomal Value (z-score) X", max_digits=25, decimal_places=20)
    ncv_Y = models.DecimalField(blank=True, null=True,
                                help_text="Normalized Chromosomal Value (z-score) Y", max_digits=25, decimal_places=20)
    ratio_13 = models.DecimalField(blank=True, null=True, help_text="Chromosomal Ratio 13", max_digits=25, decimal_places=20)
    ratio_18 = models.DecimalField(blank=True, null=True, help_text="Chromosomal Ratio 18", max_digits=25, decimal_places=20)
    ratio_21 = models.DecimalField(blank=True, null=True, help_text="Chromosomal Ratio 21", max_digits=25, decimal_places=20)
    ratio_X = models.DecimalField(blank=True, null=True, help_text="Chromosomal Ratio X", max_digits=25, decimal_places=20)
    ratio_y = models.DecimalField(blank=True, null=True, help_text="Chromosomal Ratio Y", max_digits=25, decimal_places=20)
    clusters = models.IntegerField(blank=False, help_text="Total number of clusters across lanes (Reported per flow cell)")
    total_reads_2_clusters = models.DecimalField(blank=False,
                                                 help_text="Ratio of recovered reads to number of clusters across lanes " +
                                                           "(Reported per flow cell)", max_digits=25, decimal_places=20)
    max_misindexed_reads_2_clusters = models.FloatField(blank=False,
                                                        help_text="Ratio of misindexed reads across lanes to clusters in a " +
                                                                  "virtual lane (Reported per flow cell)")
    indexed_reads = models.IntegerField(blank=False, help_text="Total number of indexed reads per sample across lanes")
    total_indexed_reads_2_clusters = models.DecimalField(blank=False, max_digits=25, decimal_places=20,
                                                         help_text="Ratio of indexed reads to clusters (Reported per flow cell)")
    tags = models.IntegerField(blank=False, help_text="Number of reads mapped to a unique place in the genome")
    non_excluded_sites = models.IntegerField(blank=False,
                                             help_text="Number of tags excluding filtered genome regions and duplicate reads " +
                                                       "mapping to the same location")
    non_excluded_sites_2_tags = models.DecimalField(blank=False, max_digits=25, decimal_places=20,
                                                    help_text="Ratio of NonExcludedSites to tags")
    tags_2_indexed_reads = models.DecimalField(blank=False, max_digits=25, decimal_places=20,
                                               help_text="Ratio of tags to indexed reads")
    perfect_match_tags_2_tags = models.DecimalField(blank=False, max_digits=25, decimal_places=20,
                                                    help_text="Ratio of perfectly mapped tags to all tags")
    gc_bias = models.DecimalField(blank=False, max_digits=25, decimal_places=20,
                                  help_text="Residual GC bias in the read distribution after correction")
    gcr2 = models.DecimalField(blank=False, max_digits=25, decimal_places=20,
                               help_text="R2 of the GC correction (percentage of variance explained by GC correction)")
    ncd_13 = models.DecimalField(blank=False, max_digits=25, decimal_places=20,
                                 help_text="Likelihood score for chromosome 13 denominators")
    ncd_18 = models.DecimalField(blank=False, max_digits=25, decimal_places=20,
                                 help_text="Likelihood score for chromosome 18 denominators")
    ncd_21 = models.DecimalField(blank=False, max_digits=25, decimal_places=20,
                                 help_text="Likelihood score for chromosome 21 denominators")
    ncd_x = models.DecimalField(blank=False, max_digits=25, decimal_places=20,
                                help_text="Likelihood score for chromosome X denominators")
    ncd_y = models.DecimalField(blank=False, max_digits=25, decimal_places=20,
                                help_text="Likelihood score for chromosome Y denominators")
    chr1_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chr2_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chr3_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chr4_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chr5_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chr6_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chr7_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chr8_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chr9_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chr10_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chr11_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chr12_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chr13_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chr14_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chr15_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chr16_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chr17_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chr18_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chr19_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chr20_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chr21_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chr22_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chrx_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chry_coverage = models.DecimalField(blank=False, help_text=__help_text_chr_coverage, max_digits=25, decimal_places=20)
    chr1 = models.IntegerField(blank=False, help_text=__help_text_chr)
    chr2 = models.IntegerField(blank=False, help_text=__help_text_chr)
    chr3 = models.IntegerField(blank=False, help_text=__help_text_chr)
    chr4 = models.IntegerField(blank=False, help_text=__help_text_chr)
    chr5 = models.IntegerField(blank=False, help_text=__help_text_chr)
    chr6 = models.IntegerField(blank=False, help_text=__help_text_chr)
    chr7 = models.IntegerField(blank=False, help_text=__help_text_chr)
    chr8 = models.IntegerField(blank=False, help_text=__help_text_chr)
    chr9 = models.IntegerField(blank=False, help_text=__help_text_chr)
    chr10 = models.IntegerField(blank=False, help_text=__help_text_chr)
    chr11 = models.IntegerField(blank=False, help_text=__help_text_chr)
    chr12 = models.IntegerField(blank=False, help_text=__help_text_chr)
    chr13 = models.IntegerField(blank=False, help_text=__help_text_chr)
    chr14 = models.IntegerField(blank=False, help_text=__help_text_chr)
    chr15 = models.IntegerField(blank=False, help_text=__help_text_chr)
    chr16 = models.IntegerField(blank=False, help_text=__help_text_chr)
    chr17 = models.IntegerField(blank=False, help_text=__help_text_chr)
    chr18 = models.IntegerField(blank=False, help_text=__help_text_chr)
    chr19 = models.IntegerField(blank=False, help_text=__help_text_chr)
    chr20 = models.IntegerField(blank=False, help_text=__help_text_chr)
    chr21 = models.IntegerField(blank=False, help_text=__help_text_chr)
    chr22 = models.IntegerField(blank=False, help_text=__help_text_chr)
    Chrx = models.IntegerField(blank=False, help_text=__help_text_chr)
    chry = models.IntegerField(blank=False, help_text=__help_text_chr)
    ff_formatted = models.DecimalField(blank=True, null=True, max_digits=25, decimal_places=20,
                                       help_text="Estimated fetal component of cfDNA recovered by the assay. Reported as a " +
                                                 "discreet, rounded percentage that provides additional information for each " +
                                                 "sample.")

    def __str__(self):
        return self.sample_id + ";  " + str(self.sample_type) + "; " + str(self.index)

    def create_sample_data(flowcell_id_entry, sample_type_entry, sample_id, sample_project, index, well, description, library_nm,
                           qc_flag, qc_failure, qc_warning,
                           ncv_13, ncv_18, ncv_21, ncv_x, ncv_y, ratio_13, ratio_18, ratio_21, ratio_X, ratio_y,
                           clusters, total_reads_2_clusters, max_misindexed_reads_2_clusters, indexed_reads,
                           total_indexed_reads_2_clusters, tags, non_excluded_sites, non_excluded_sites_2_tags,
                           tags_2_indexed_reads, perfect_match_tags_2_tags, gc_bias, gcr2, ncd_13, ncd_18, ncd_21, ncd_x, ncd_y,
                           chr1_coverage, chr2_coverage, chr3_coverage, chr4_coverage, chr5_coverage, chr6_coverage,
                           chr7_coverage, chr8_coverage, chr9_coverage, chr10_coverage, chr11_coverage, chr12_coverage,
                           chr13_coverage, chr14_coverage, chr15_coverage, chr16_coverage, chr17_coverage, chr18_coverage,
                           chr19_coverage, chr20_coverage, chr21_coverage, chr22_coverage, chrx_coverage, chry_coverage,
                           chr1, chr2, chr3, chr4, chr5, chr6, chr7, chr8, chr9,
                           chr10, chr11, chr12, chr13, chr14, chr15, chr16, chr17,
                           chr18, chr19, chr20, chr21, chr22, chrx, chry, ff_formatted):
        return SamplesRunData.objects.create(
                flowcell_id=flowcell_id_entry,
                sample_type=sample_type_entry,
                sample_id=sample_id,
                sample_project=sample_project,
                index=index,
                well=well,
                description=description,
                library_nm=library_nm,
                qc_flag=qc_flag,
                qc_failure=qc_failure,
                qc_warning=qc_warning,
                ncv_13=ncv_13 if not pandas.isna(ncv_13) else None,
                ncv_18=ncv_18 if not pandas.isna(ncv_18) else None,
                ncv_21=ncv_21 if not pandas.isna(ncv_21) else None,
                ncv_X=ncv_x if not pandas.isna(ncv_x) else None,
                ncv_Y=ncv_y if not pandas.isna(ncv_y) else None,
                ratio_13=ratio_13 if not pandas.isna(ratio_13) else None,
                ratio_18=ratio_18 if not pandas.isna(ratio_18) else None,
                ratio_21=ratio_21 if not pandas.isna(ratio_21) else None,
                ratio_X=ratio_X if not pandas.isna(ratio_X) else None,
                ratio_y=ratio_y if not pandas.isna(ratio_y) else None,
                clusters=clusters,
                total_reads_2_clusters=total_reads_2_clusters,
                max_misindexed_reads_2_clusters=max_misindexed_reads_2_clusters,
                indexed_reads=indexed_reads,
                total_indexed_reads_2_clusters=total_indexed_reads_2_clusters,
                tags=tags,
                non_excluded_sites=non_excluded_sites,
                non_excluded_sites_2_tags=non_excluded_sites_2_tags,
                tags_2_indexed_reads=tags_2_indexed_reads,
                perfect_match_tags_2_tags=perfect_match_tags_2_tags,
                gc_bias=gc_bias,
                gcr2=gcr2,
                ncd_13=ncd_13 if not ncd_13 == "NA" else None,
                ncd_18=ncd_18 if not ncd_18 == "NA" else None,
                ncd_21=ncd_21 if not ncd_21 == "NA" else None,
                ncd_x=ncd_x if not ncd_x == "NA" else None,
                ncd_y=ncd_y if not ncd_y == "NA" else None,
                chr1_coverage=chr1_coverage,
                chr2_coverage=chr2_coverage,
                chr3_coverage=chr3_coverage,
                chr4_coverage=chr4_coverage,
                chr5_coverage=chr5_coverage,
                chr6_coverage=chr6_coverage,
                chr7_coverage=chr7_coverage,
                chr8_coverage=chr8_coverage,
                chr9_coverage=chr9_coverage,
                chr10_coverage=chr10_coverage,
                chr11_coverage=chr11_coverage,
                chr12_coverage=chr12_coverage,
                chr13_coverage=chr13_coverage,
                chr14_coverage=chr14_coverage,
                chr15_coverage=chr15_coverage,
                chr16_coverage=chr16_coverage,
                chr17_coverage=chr17_coverage,
                chr18_coverage=chr18_coverage,
                chr19_coverage=chr19_coverage,
                chr20_coverage=chr20_coverage,
                chr21_coverage=chr21_coverage,
                chr22_coverage=chr22_coverage,
                chrx_coverage=chrx_coverage,
                chry_coverage=chry_coverage,
                chr1=chr1,
                chr2=chr2,
                chr3=chr3,
                chr4=chr4,
                chr5=chr5,
                chr6=chr6,
                chr7=chr7,
                chr8=chr8,
                chr9=chr9,
                chr10=chr10,
                chr11=chr11,
                chr12=chr12,
                chr13=chr13,
                chr14=chr14,
                chr15=chr15,
                chr16=chr16,
                chr17=chr17,
                chr18=chr18,
                chr19=chr19,
                chr20=chr20,
                chr21=chr21,
                chr22=chr22,
                Chrx=chrx,
                chry=chry,
                ff_formatted=ff_formatted if not pandas.isna(ff_formatted) else None)

    def get_samples(flowcell, sample=None):
        if sample is None:
            return SamplesRunData.objects.filter(flowcell_id=flowcell). \
                select_related().values('ff_formatted', 'flowcell_id__run_date', 'flowcell_id__flowcell_barcode', 'sample_id',
                                        'sample_type__name', 'ncv_13', 'ncv_18', 'ncv_21', 'ncv_X', 'ncv_Y', 'chr1_coverage',
                                        'chr2_coverage', 'chr3_coverage', 'chr4_coverage', 'chr5_coverage', 'chr6_coverage',
                                        'chr7_coverage', 'chr8_coverage', 'chr9_coverage', 'chr10_coverage', 'chr11_coverage',
                                        'chr12_coverage', 'chr13_coverage', 'chr14_coverage', 'chr15_coverage', 'chr16_coverage',
                                        'chr17_coverage', 'chr18_coverage', 'chr19_coverage', 'chr20_coverage', 'chr21_coverage',
                                        'chr22_coverage', 'chrx_coverage', 'chry_coverage', 'qc_flag', 'qc_failure',
                                        'qc_warning',  'chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9',
                                        'chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19',
                                        'chr20', 'chr21', 'chr22', 'Chrx', 'chry')
        else:
            return SamplesRunData.objects.filter(flowcell_id=flowcell, sample_id=sample). \
                select_related().values('ff_formatted', 'flowcell_id__run_date', 'flowcell_id__flowcell_barcode', 'sample_id',
                                        'sample_type__name', 'ncv_13', 'ncv_18', 'ncv_21', 'ncv_X', 'ncv_Y', 'chr1_coverage',
                                        'chr2_coverage', 'chr3_coverage', 'chr4_coverage', 'chr5_coverage', 'chr6_coverage',
                                        'chr7_coverage', 'chr8_coverage', 'chr9_coverage', 'chr10_coverage', 'chr11_coverage',
                                        'chr12_coverage', 'chr13_coverage', 'chr14_coverage', 'chr15_coverage', 'chr16_coverage',
                                        'chr17_coverage', 'chr18_coverage', 'chr19_coverage', 'chr20_coverage', 'chr21_coverage',
                                        'chr22_coverage', 'chrx_coverage', 'chry_coverage', 'qc_flag', 'qc_failure',
                                        'qc_warning',  'chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9',
                                        'chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19',
                                        'chr20', 'chr21', 'chr22', 'Chrx', 'chry')

    def get_samples_not_included(flowcell, start_time=None, stop_time=None, sample=None):
        if start_time is not None or stop_time is not None:
            flowcells = Flowcell.objects.filter(run_date__lte=stop_time, run_date__gte=start_time)
            if sample is None:
                return SamplesRunData.objects.filter(flowcell_id__in=flowcells).exclude(flowcell_id=flowcell). \
                    select_related().values('ff_formatted', 'flowcell_id__run_date', 'flowcell_id__flowcell_barcode',
                                            'sample_id', 'sample_type__name', 'ncv_13', 'ncv_18', 'ncv_21', 'ncv_X', 'ncv_Y')
            else:
                return SamplesRunData.objects.filter(flowcell_id__in=flowcells). \
                       exclude(flowcell_id=flowcell, sample_id=sample). \
                       select_related().values('ff_formatted', 'flowcell_id__run_date', 'flowcell_id__flowcell_barcode',
                                               'sample_id', 'sample_type__name', 'ncv_13', 'ncv_18', 'ncv_21', 'ncv_X', 'ncv_Y')
        else:
            if sample is None:
                return SamplesRunData.objects.all().exclude(flowcell_id=flowcell). \
                    select_related().values('ff_formatted', 'flowcell_id__run_date', 'flowcell_id__flowcell_barcode',
                                            'sample_id', 'sample_type__name', 'ncv_13', 'ncv_18', 'ncv_21', 'ncv_X', 'ncv_Y')
            else:
                return SamplesRunData.objects.all().exclude(flowcell_id=flowcell, sample_id=sample). \
                    select_related().values('ff_formatted', 'flowcell_id__run_date', 'flowcell_id__flowcell_barcode',
                                            'sample_id', 'sample_type__name', 'ncv_13', 'ncv_18', 'ncv_21', 'ncv_X', 'ncv_Y')


class Line(models.Model):
    slope = models.DecimalField(blank=False, help_text="Slope of line", decimal_places=5, max_digits=15)
    intercept = models.DecimalField(blank=False, help_text="Intercept point", decimal_places=5, max_digits=15)
    stderr = models.DecimalField(blank=False, help_text="Stderr", decimal_places=5, max_digits=15)
    stdev = models.DecimalField(blank=False, help_text="Stderr", decimal_places=5, max_digits=15)
    p_value = models.DecimalField(blank=False, help_text="P value", decimal_places=5, max_digits=15)
    r_value = models.DecimalField(blank=False, help_text="R value", decimal_places=5, max_digits=15)
    plot_type = models.CharField(max_length=20, help_text="Comparison type", blank=False, unique=True)

    def create_or_update_line(type, slope, intercept, stderr, stdev, p_value, r_value):
        line = Line.objects.filter(plot_type=type)
        if line and len(line) == 1:
            line[0].slope = slope
            line[0].intercept = intercept
            line[0].stderr = stderr
            line[0].stdev = stdev
            line[0].p_value = p_value
            line[0].r_value = r_value
            line[0].save()
        else:
            return Line.objects.create(plot_type=type,
                                       slope=slope,
                                       intercept=intercept,
                                       stderr=stderr,
                                       stdev=stdev,
                                       p_value=p_value,
                                       r_value=r_value)

    def get_line(type):
        return Line.objects.filter(plot_type=type)

    def __str__(self):
        return "y={}*x + {}, stderr: {}, stdev: {}, P: {}, R: {}".format(self.slope,
                                                                         self.intercept,
                                                                         self.stderr,
                                                                         self.stdev,
                                                                         self.p_value,
                                                                         self.r_value)
