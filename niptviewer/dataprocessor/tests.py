from .models import SampleType, Index, Flowcell, BatchRun, SamplesRunData, Index
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
import datetime
import numpy as np

HEADER = ["SampleID", "SampleType", "Flowcell", "Description", "SampleProject", "IndexID", "Index", "Well",
          "Library_nM", "QCFlag", "QCFailure", "QCWarning", "NCV_13", "NCV_18", "NCV_21", "NCV_X", "NCV_Y", "Ratio_13",
          "Ratio_18", "Ratio_21", "Ratio_X", "Ratio_Y", "Clusters", "TotalReads2Clusters",
          "MaxMisindexedReads2Clusters", "IndexedReads", "TotalIndexedReads2Clusters", "Tags", "NonExcludedSites",
          "NonExcludedSites2Tags", "Tags2IndexedReads", "PerfectMatchTags2Tags", "GCBias", "GCR2", "NCD_13", "NCD_18",
          "NCD_21", "NCD_X", "NCD_Y", "Chr1_Coverage", "Chr2_Coverage", "Chr3_Coverage", "Chr4_Coverage",
          "Chr5_Coverage", "Chr6_Coverage", "Chr7_Coverage", "Chr8_Coverage", "Chr9_Coverage", "Chr10_Coverage",
          "Chr11_Coverage", "Chr12_Coverage", "Chr13_Coverage", "Chr14_Coverage", "Chr15_Coverage", "Chr16_Coverage",
          "Chr17_Coverage", "Chr18_Coverage", "Chr19_Coverage", "Chr20_Coverage", "Chr21_Coverage", "Chr22_Coverage",
          "ChrX_Coverage", "ChrY_Coverage", "Chr1", "Chr2", "Chr3", "Chr4", "Chr5", "Chr6", "Chr7", "Chr8", "Chr9",
          "Chr10", "Chr11", "Chr12", "Chr13", "Chr14", "Chr15", "Chr16", "Chr17", "Chr18", "Chr19", "Chr20", "Chr21",
          "Chr22", "ChrX", "ChrY", "Median_13", "Median_18", "Median_21", "Median_X", "Median_Y", "Stdev_13",
          "Stdev_18", "Stdev_21", "Stdev_X", "Stdev_Y", "FF_Formatted"]

TEST_DATA = [
    ["120AB-1", "Test", "ABCDEFGHI", "d1", "P1", "A002", "CGATGT", "A2", 43.9, 3, "NCC;", "ACB", -0.65537058,
     -0.26181607, 0.03433961, -3.46129478, 54.04707311, 0.1997250425013872, 0.2495247637744749, 0.2501577664130391,
     0.325867183420615, 7.022031713343147E-8, 559762153, 1.0, 1.0700080325009041E-4, 38828451, 0.9028202894596198,
     31398596, 29051311, 0.9252423579704009, 0.8086492041621748, 0.9363653075443246, 0.05035, 0.82417, 22.8842,
     17.66044, 17.82128, 15.27829, 89.98756, 0.999767156655, 0.996221044411, 1.00240419923, 0.998675017099,
     1.00029748755, 0.996906814503, 1.00082776713, 0.998424292775, 0.999498912425, 0.994719943037, 1.00110849673,
     0.999569333688, 0.995994623495, 0.998788650217, 0.994360417196, 1.00836543998, 0.997585308234, 0.996679189689,
     1.01607827032, 1.00249046855, 0.998684864799, 0.999147192931, 0.978871276368, 6.99549576735E-8, 2354053, 2486612,
     2055877, 1845160, 1823656, 1736871, 1547935, 1508355, 1172952, 1413907, 1401626, 1371579, 955609, 918492, 850503,
     822282, 802915, 795715, 533643, 687727, 369009, 362949, 1232818, 1066, 0.20000997720842884, 0.2496738366536334,
     0.2501301523467464, 0.3317407341447674, 7.979040558294557E-9, 3.0509929074924204E-4, 2.3989667228442092E-4,
     6.189684400650153E-4, 6.369169138443013E-4, 1.1323241868674808E-9, 8 / 100],
    ["130VY-2", "Test", "ABCDEFGHI", "d2", "", "A005", "ACAGTG", "B2", 44.1, 0, "", "", -0.85104066, -0.27928844,
     -0.72567932, -3.2939618, 55.3614837, 0.1996399712481648, 0.24951481535248005, 0.2495466000982289,
     0.3261511345993774, 7.173400858600674E-8, 559762153, 1.0, 1.070008032500904E-4, 35444004, 0.9028202894596198,
     28561479, 26393539, 0.9240956674547561, 0.8058197657352708, 0.9361645102482263, 0.03919, 0.86071, 23.67755,
     17.77966, 17.88423, 14.96602, 91.42685, 0.997651181433, 0.996182338212, 1.00127671888, 0.999628197481,
     1.0003626279, 0.997223433584, 0.998559132761, 1.00135340871, 1.00190440161, 0.994465583264, 1.00105943377,
     1.00058080961, 0.996579746622, 1.00025531579, 0.992899046942, 1.00916856964, 0.998225059697, 0.997833312888,
     1.01844729688, 1.00364725902, 0.996826495268, 0.994852107712, 0.98010676849, 7.14601524025E-8, 2141941, 2254052,
     1856963, 1657486, 1647483, 1570690, 1401373, 1370342, 1069424, 1289908, 1276737, 1246935, 860482, 835223, 776874,
     758248, 741550, 721958, 497907, 632968, 334830, 336248, 1112927, 990, 0.20000997720842884, 0.2496738366536334,
     0.2501301523467464, 0.3317407341447674, 7.979040558294557E-9, 3.0509929074924204E-4, 2.3989667228442092E-4,
     6.189684400650153E-4, 6.369169138443013E-4, 1.1323241868674808E-9, 7 / 100],
    ["XY012345", "Control", "ABCDEFGHI", "d3", "", "A025", "ACTGAT", "G4", 54.9, 0, "", "", -0.78114759, -0.68553864,
     -0.52671249, -8.0505785, 127.67442885, 0.1996703585758866, 0.24928350454948028, 0.24970659851165686,
     0.3180795223086526, 1.550104888862345E-7, 559762153, 1.6, 1.070008032500904E-4, 37543895, 0.9028202894596198,
     30748027, 28497583, 0.9268101332160271, 0.8189887330550013, 0.9378450201048673, 0.00695, 0.13847, 26.1829,
     20.43631, 20.49477, 15.34822, 97.83376, 1.00149329993, 1.00005899646, 1.00071032123, 1.00122760212, 0.999845101557,
     0.999594247835, 1.00015460739, 1.00107714859, 1.0013689022, 0.999746775752, 0.999034698484, 1.0010478566,
     0.998531878599, 0.998791392218, 0.998253202924, 1.00149627032, 0.999200819481, 0.997892598265, 1.00384951439,
     1.00099151511, 0.998723684614, 0.997762268947, 0.95419763491, 1.55019633957E-7, 2282891, 2463877, 2043949, 1899300,
     1820069, 1735136, 1528588, 1493903, 1141890, 1369602, 1357742, 1347096, 976612, 899946, 815806, 764324, 746437,
     790915, 481246, 641772, 363532, 327793, 1202844, 2313, 0.20000997720842884, 0.2496738366536334, 0.2501301523467464,
     0.3317407341447674, 7.979040558294557E-9, 3.0509929074924204E-4, 2.3989667228442092E-4, 6.189684400650153E-4,
     6.369169138443013E-4, 1.1323241868674808E-9, 10 / 100],
    ["MN20-1234-BM", "Test", "ABCDEFGHI", "", "", "A003", "TTAGGC", "B4", 43.9, 2, "NCD_21;NCD_18", "", np.nan, np.nan,
     np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 408619234, 1.0, 1.0563624129352658E-4, 22776432,
     0.927590662557994, 17972441, 16722713, 0.9304642034991241, 0.7890806163142673, 0.9353938621915632, 0.08938,
     0.81036, 13.15018, -59.89946, -75.72517, -47.77625, -90.1483, 0.997787570191, 0.993370110807, 1.00222816166,
     1.00148714309, 1.00238904966, 0.994059786989, 1.00410951749, 0.999882726324, 0.996999756351, 0.99719996531,
     0.999751505041, 1.00327138225, 0.997911936493, 0.995225512295, 0.994999526549, 1.01100101117, 1.00258251107,
     0.999604849356, 1.02610547408, 0.965150624458, 0.992689922444, 1.00203732591, 0.996733350503, 8.89324434289E-9,
     1359202, 1424941, 1176848, 1046405, 1044219, 990893, 890084, 867352, 675439, 823124, 807993, 790859, 543097,
     527251, 495880, 482936, 470399, 459740, 313281, 389084, 212090, 214202, 717316, 78, 0.2000566082419352,
     0.2499767601203153, 0.2503599840311732, 0.33252057913327576, 8.45872893801531E-9, 3.2796303697978817E-4,
     5.382952934550243E-4, 6.066146484622653E-4, 0.0027062531076787037, 1.1766580670770674E-9, np.nan],
    ["LK19-4321-C-BM", "Test", "ABCDEFGHI", "", "", "A010", "TAGCTT", "D4", 61.2, 0, "", "", 2.94861252, -0.12303047,
     -0.88540654, 2.05340098, -0.7353879, 0.2011177898424326, 0.24977289575241307, 0.24900286063298493,
     0.33674489337781505, 6.3083996515990304E-9, 477059374, 1.0, 1.165892612771508E-4, 25876409, 0.9186892782867736,
     20923248, 19495863, 0.9317799511815756, 0.8085839113147423, 0.9376390797451715, 0.0517, 0.6581, 16.75418, 17.09129,
     11.96289, 14.79218, 65.04944, 0.998184128404, 0.99441250147, 1.00122891271, 1.00322562984, 1.00060542301,
     0.995303956252, 1.0058501427, 1.00104966922, 1.00057124671, 0.994357680568, 0.997745131629, 1.00128531106,
     1.00330609959, 0.995603709857, 0.990864677651, 1.00445280196, 0.998282886014, 0.998627237515, 1.03343426291,
     0.999507949576, 0.99199797495, 1.00312572838, 1.00951354236, 6.27315147782E-9, 1572441, 1671071, 1383408, 1241807,
     1227919, 1166992, 1040444, 1021504, 785567, 950552, 932991, 919019, 647704, 613962, 571071, 544475, 525739, 539308,
     342031, 457425, 244288, 235981, 860100, 64, 0.19983582499641347, 0.249842946860313, 0.24971485691008202,
     0.33326043001521344, 7.155281440328387E-9, 2.4020934098400952E-4, 6.218465301768219E-4, 8.824610220556811E-4,
     0.0015387570636482906, 9.931177315545228E-10, 1 / 100]
]


class UtilTestTestsCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Testuser')
        self.admin_ser = User.objects.create(username='admin')

        call_command("loaddata", "index", app_label='dataprocessor')
        call_command("loaddata", "sample_types", app_label='dataprocessor')

    def test_csv_parsing(self):
        csv = open("./dataprocessor/tests/200809_NDX123456_RUO_0001_ABCDEFGHIJ_NIPT_RESULTS.csv")
        from .utils.data import parse_niptool_csv
        version, run_date, data = parse_niptool_csv(csv)

        self.assertEqual(version, "1.1.1")
        self.assertTrue(run_date == datetime.datetime.strptime("200809", "%y%m%d"))
        self.assertEqual(len(data), 5)
        iterator = iter(data.iterrows())
        row = next(iterator)

        def compare_row(row, counter):
            for i in range(len(HEADER)):
                if isinstance(row[1][HEADER[i]], float):
                    if np.isnan(row[1][HEADER[i]]):
                        self.assertTrue(np.isnan(TEST_DATA[counter][i]))
                    else:
                        self.assertTrue(abs(row[1][HEADER[i]] - TEST_DATA[counter][i]) < 0.000000001)
                elif isinstance(TEST_DATA[counter][i], str):
                    self.assertEqual(row[1][HEADER[i]], TEST_DATA[counter][i])
                else:
                    # Catch unhandled case
                    self.assertTrue(False)

        compare_row(row, 0)
        row = next(iterator)
        compare_row(row, 1)
        row = next(iterator)
        compare_row(row, 2)
        row = next(iterator)
        compare_row(row, 3)
        row = next(iterator)
        compare_row(row, 4)

    def test_flowcell_csv_into_database(self):
        csv = open("./dataprocessor/tests/200809_NDX123456_RUO_0001_ABCDEFGHIJ_NIPT_RESULTS.csv")
        from .utils.data import import_data_into_database
        import_data_into_database(self.user, csv)

        flowcell = Flowcell.objects.get(flowcell_barcode="ABCDEFGHI")

        self.assertEqual(flowcell.flowcell_barcode, "ABCDEFGHI")
        self.assertEqual(flowcell.uploading_user, self.user)
        self.assertEqual(flowcell.qc_status, "Failures (2), Warnings (1)")
        self.assertEqual(flowcell.created.strftime("%d/%m/%Y"), datetime.datetime.now().strftime("%d/%m/%Y"))
        self.assertEqual(flowcell.run_date.strftime("%d/%m/%Y"),
                         datetime.datetime.strptime("200809", "%y%m%d").strftime("%d/%m/%Y"))

    def test_batchrun_csv_into_database(self):
        csv = open("./dataprocessor/tests/200809_NDX123456_RUO_0001_ABCDEFGHIJ_NIPT_RESULTS.csv")
        from .utils.data import import_data_into_database
        import_data_into_database(self.user, csv)

        batch = BatchRun.objects.get(flowcell_id=Flowcell.objects.get(flowcell_barcode="ABCDEFGHI"))

        self.assertTrue(abs(batch.median_13 - Decimal("0.20000997720842884")) < 0.00000001)
        self.assertTrue(abs(batch.median_18 - Decimal("0.2496738366536334")) < 0.00000001)
        self.assertTrue(abs(batch.median_21 - Decimal("0.2501301523467464")) < 0.00000001)
        self.assertTrue(abs(batch.median_x - Decimal("0.3317407341447674")) < 0.00000001)
        self.assertTrue(abs(batch.median_y - Decimal("7.97904055829E-9")) < 0.00000001)
        self.assertTrue(abs(batch.stdev_13 - 0.00030509929074924204) < 0.00000001)
        self.assertTrue(abs(batch.stdev_18 - 0.00023989667228442092) < 0.00000001)
        self.assertTrue(abs(batch.stdev_21 - 0.0006189684400650153) < 0.00000001)
        self.assertTrue(abs(batch.stdev_X - 0.0006369169138443013) < 0.00000001)
        self.assertTrue(abs(batch.stdev_Y - 1.1323241868674808E-9) < 0.00000001)
        self.assertEqual(batch.software_version, "1.1.1")

    def test_samplerundata_csv_into_database(self):
        csv = open("./dataprocessor/tests/200809_NDX123456_RUO_0001_ABCDEFGHIJ_NIPT_RESULTS.csv")
        from .utils.data import import_data_into_database
        import_data_into_database(self.user, csv)

        samples = SamplesRunData.objects.filter(flowcell_id=Flowcell.objects.get(flowcell_barcode="ABCDEFGHI"))
        iSamples = iter(samples)
        sample = next(iSamples)

        self.assertEqual(sample.sample_type, SampleType.objects.get(name="Test"))
        self.assertEqual(sample.sample_id, "120AB-1")
        self.assertEqual(sample.sample_project, "P1")
        self.assertEqual(sample.index, Index.objects.get(index_id="A002"))
        self.assertEqual(sample.well, "A2")
        self.assertEqual(sample.description, "d1")
        self.assertTrue(abs(sample.library_nm - Decimal("43.9000000000000000000")) < 0.00000001)
        self.assertEqual(sample.qc_flag, 3)
        self.assertEqual(sample.qc_failure, "NCC;")
        self.assertEqual(sample.qc_warning, "ACB")
        self.assertTrue(abs(sample.ncv_13 - Decimal("-0.65537058")) < 0.00000001)
        self.assertTrue(abs(sample.ncv_18 - Decimal("-0.26181607")) < 0.00000001)
        self.assertTrue(abs(sample.ncv_21 - Decimal("0.03433961")) < 0.00000001)
        self.assertTrue(abs(sample.ncv_X - Decimal("-3.46129478")) < 0.00000001)
        self.assertTrue(abs(sample.ncv_Y - Decimal("54.04707311")) < 0.00000001)
        self.assertTrue(abs(sample.ratio_13 - Decimal("0.199725042501387")) < 0.00000001)
        self.assertTrue(abs(sample.ratio_18 - Decimal("0.249524763774475")) < 0.00000001)
        self.assertTrue(abs(sample.ratio_21 - Decimal("0.250157766413039")) < 0.00000001)
        self.assertTrue(abs(sample.ratio_X - Decimal("0.325867183420615")) < 0.00000001)
        self.assertTrue(abs(sample.ratio_y - Decimal("7.022031713343E-8")) < 0.00000001)
        self.assertEqual(sample.clusters, 559762153)
        self.assertEqual(sample.total_reads_2_clusters, 1.0)
        self.assertTrue(abs(sample.max_misindexed_reads_2_clusters - 0.0001070008032500904) < 0.00000001)
        self.assertEqual(sample.indexed_reads, 38828451)
        self.assertTrue(abs(sample.total_indexed_reads_2_clusters - Decimal("0.90282028945962")) < 0.00000001)
        self.assertEqual(sample.tags, 31398596)
        self.assertEqual(sample.non_excluded_sites, 29051311)
        self.assertTrue(abs(sample.non_excluded_sites_2_tags - Decimal("0.925242357970401")) < 0.00000001)
        self.assertTrue(abs(sample.tags_2_indexed_reads - Decimal("0.80864920416217500000")) < 0.00000001)
        self.assertTrue(abs(sample.perfect_match_tags_2_tags - Decimal("0.936365307544325")) < 0.00000001)
        self.assertTrue(abs(sample.gc_bias - Decimal("0.05035")) < 0.00000001)
        self.assertTrue(abs(sample.gcr2 - Decimal("0.82417")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_13 - Decimal("22.8842")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_18 - Decimal("17.66044")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_21 - Decimal("17.82128")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_x - Decimal("15.27829")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_y - Decimal("89.98756")) < 0.00000001)
        self.assertTrue(abs(sample.chr1_coverage - Decimal("0.999767156655")) < 0.00000001)
        self.assertTrue(abs(sample.chr2_coverage - Decimal("0.996221044411")) < 0.00000001)
        self.assertTrue(abs(sample.chr3_coverage - Decimal("1.00240419923")) < 0.00000001)
        self.assertTrue(abs(sample.chr4_coverage - Decimal("0.998675017099")) < 0.00000001)
        self.assertTrue(abs(sample.chr5_coverage - Decimal("1.00029748755")) < 0.00000001)
        self.assertTrue(abs(sample.chr6_coverage - Decimal("0.996906814503")) < 0.00000001)
        self.assertTrue(abs(sample.chr7_coverage - Decimal("1.00082776713")) < 0.00000001)
        self.assertTrue(abs(sample.chr8_coverage - Decimal("0.998424292775")) < 0.00000001)
        self.assertTrue(abs(sample.chr9_coverage - Decimal("0.999498912425")) < 0.00000001)
        self.assertTrue(abs(sample.chr10_coverage - Decimal("0.994719943037")) < 0.00000001)
        self.assertTrue(abs(sample.chr11_coverage - Decimal("1.00110849673")) < 0.00000001)
        self.assertTrue(abs(sample.chr12_coverage - Decimal("0.999569333688")) < 0.00000001)
        self.assertTrue(abs(sample.chr13_coverage - Decimal("0.995994623495")) < 0.00000001)
        self.assertTrue(abs(sample.chr14_coverage - Decimal("0.998788650217")) < 0.00000001)
        self.assertTrue(abs(sample.chr15_coverage - Decimal("0.994360417196")) < 0.00000001)
        self.assertTrue(abs(sample.chr16_coverage - Decimal("1.00836543998")) < 0.00000001)
        self.assertTrue(abs(sample.chr17_coverage - Decimal("0.997585308234")) < 0.00000001)
        self.assertTrue(abs(sample.chr18_coverage - Decimal("0.996679189689")) < 0.00000001)
        self.assertTrue(abs(sample.chr19_coverage - Decimal("1.01607827032")) < 0.00000001)
        self.assertTrue(abs(sample.chr20_coverage - Decimal("1.00249046855")) < 0.00000001)
        self.assertTrue(abs(sample.chr21_coverage - Decimal("0.998684864799")) < 0.00000001)
        self.assertTrue(abs(sample.chr22_coverage - Decimal("0.999147192931")) < 0.00000001)
        self.assertTrue(abs(sample.chrx_coverage - Decimal("0.978871276368")) < 0.00000001)
        self.assertTrue(abs(sample.chry_coverage - Decimal("6.99549576735E-8")) < 0.00000001)
        self.assertEqual(sample.chr1, 2354053)
        self.assertEqual(sample.chr2, 2486612)
        self.assertEqual(sample.chr3, 2055877)
        self.assertEqual(sample.chr4, 1845160)
        self.assertEqual(sample.chr5, 1823656)
        self.assertEqual(sample.chr6, 1736871)
        self.assertEqual(sample.chr7, 1547935)
        self.assertEqual(sample.chr8, 1508355)
        self.assertEqual(sample.chr9, 1172952)
        self.assertEqual(sample.chr10, 1413907)
        self.assertEqual(sample.chr11, 1401626)
        self.assertEqual(sample.chr12, 1371579)
        self.assertEqual(sample.chr13, 955609)
        self.assertEqual(sample.chr14, 918492)
        self.assertEqual(sample.chr15, 850503)
        self.assertEqual(sample.chr16, 822282)
        self.assertEqual(sample.chr17, 802915)
        self.assertEqual(sample.chr18, 795715)
        self.assertEqual(sample.chr19, 533643)
        self.assertEqual(sample.chr20, 687727)
        self.assertEqual(sample.chr21, 369009)
        self.assertEqual(sample.chr22, 362949)
        self.assertEqual(sample.Chrx, 1232818)
        self.assertEqual(sample.chry, 1066)
        self.assertTrue(abs(sample.ff_formatted - Decimal("0.08")) < 0.00000001)

        sample = next(iSamples)

        self.assertEqual(sample.sample_type, SampleType.objects.get(name="Test"))
        self.assertEqual(sample.sample_id, "130VY-2")
        self.assertEqual(sample.sample_project, "")
        self.assertEqual(sample.index, Index.objects.get(index_id="A005"))
        self.assertEqual(sample.well, "B2")
        self.assertEqual(sample.description, "d2")
        self.assertTrue(abs(sample.library_nm - Decimal("44.1000000000000000000")) < 0.00000001)
        self.assertEqual(sample.qc_flag, 0)
        self.assertEqual(sample.qc_failure, "")
        self.assertEqual(sample.qc_warning, "")
        self.assertTrue(abs(sample.ncv_13 - Decimal("-0.85104066")) < 0.00000001)
        self.assertTrue(abs(sample.ncv_18 - Decimal("-0.27928844")) < 0.00000001)
        self.assertTrue(abs(sample.ncv_21 - Decimal("-0.72567932")) < 0.00000001)
        self.assertTrue(abs(sample.ncv_X - Decimal("-3.2939618")) < 0.00000001)
        self.assertTrue(abs(sample.ncv_Y - Decimal("55.3614837")) < 0.00000001)
        self.assertTrue(abs(sample.ratio_13 - Decimal("0.199639971248165")) < 0.00000001)
        self.assertTrue(abs(sample.ratio_18 - Decimal("0.24951481535248")) < 0.00000001)
        self.assertTrue(abs(sample.ratio_21 - Decimal("0.249546600098229")) < 0.00000001)
        self.assertTrue(abs(sample.ratio_X - Decimal("0.326151134599377")) < 0.00000001)
        self.assertTrue(abs(sample.ratio_y - Decimal("7.173400858601E-8")) < 0.00000001)
        self.assertEqual(sample.clusters, 559762153)
        self.assertEqual(sample.total_reads_2_clusters, 1.0)
        self.assertTrue(abs(sample.max_misindexed_reads_2_clusters - 0.0001070008032500904) < 0.00000001)
        self.assertEqual(sample.indexed_reads, 35444004)
        self.assertTrue(abs(sample.total_indexed_reads_2_clusters - Decimal("0.90282028945962")) < 0.00000001)
        self.assertEqual(sample.tags, 28561479)
        self.assertEqual(sample.non_excluded_sites, 26393539)
        self.assertTrue(abs(sample.non_excluded_sites_2_tags - Decimal("0.924095667454756")) < 0.00000001)
        self.assertTrue(abs(sample.tags_2_indexed_reads - Decimal("0.805819765735271")) < 0.00000001)
        self.assertTrue(abs(sample.perfect_match_tags_2_tags - Decimal("0.936164510248226")) < 0.00000001)
        self.assertTrue(abs(sample.gc_bias - Decimal("0.03919")) < 0.00000001)
        self.assertTrue(abs(sample.gcr2 - Decimal("0.86071")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_13 - Decimal("23.67755")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_18 - Decimal("17.77966")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_21 - Decimal("17.88423")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_x - Decimal("14.96602")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_y - Decimal("91.42685")) < 0.00000001)
        self.assertTrue(abs(sample.chr1_coverage - Decimal("0.997651181433")) < 0.00000001)
        self.assertTrue(abs(sample.chr2_coverage - Decimal("0.996182338212")) < 0.00000001)
        self.assertTrue(abs(sample.chr3_coverage - Decimal("1.00127671888")) < 0.00000001)
        self.assertTrue(abs(sample.chr4_coverage - Decimal("0.999628197481")) < 0.00000001)
        self.assertTrue(abs(sample.chr5_coverage - Decimal("1.0003626279")) < 0.00000001)
        self.assertTrue(abs(sample.chr6_coverage - Decimal("0.997223433584")) < 0.00000001)
        self.assertTrue(abs(sample.chr7_coverage - Decimal("0.998559132761")) < 0.00000001)
        self.assertTrue(abs(sample.chr8_coverage - Decimal("1.00135340871")) < 0.00000001)
        self.assertTrue(abs(sample.chr9_coverage - Decimal("1.00190440161")) < 0.00000001)
        self.assertTrue(abs(sample.chr10_coverage - Decimal("0.994465583264")) < 0.00000001)
        self.assertTrue(abs(sample.chr11_coverage - Decimal("1.00105943377")) < 0.00000001)
        self.assertTrue(abs(sample.chr12_coverage - Decimal("1.00058080961")) < 0.00000001)
        self.assertTrue(abs(sample.chr13_coverage - Decimal("0.996579746622")) < 0.00000001)
        self.assertTrue(abs(sample.chr14_coverage - Decimal("1.00025531579")) < 0.00000001)
        self.assertTrue(abs(sample.chr15_coverage - Decimal("0.992899046942")) < 0.00000001)
        self.assertTrue(abs(sample.chr16_coverage - Decimal("1.00916856964")) < 0.00000001)
        self.assertTrue(abs(sample.chr17_coverage - Decimal("0.998225059697")) < 0.00000001)
        self.assertTrue(abs(sample.chr18_coverage - Decimal("0.997833312888")) < 0.00000001)
        self.assertTrue(abs(sample.chr19_coverage - Decimal("1.01844729688")) < 0.00000001)
        self.assertTrue(abs(sample.chr20_coverage - Decimal("1.00364725902")) < 0.00000001)
        self.assertTrue(abs(sample.chr21_coverage - Decimal("0.996826495268")) < 0.00000001)
        self.assertTrue(abs(sample.chr22_coverage - Decimal("0.994852107712")) < 0.00000001)
        self.assertTrue(abs(sample.chrx_coverage - Decimal("0.98010676849")) < 0.00000001)
        self.assertTrue(abs(sample.chry_coverage - Decimal("7.14601524025E-8")) < 0.00000001)
        self.assertEqual(sample.chr1, 2141941)
        self.assertEqual(sample.chr2, 2254052)
        self.assertEqual(sample.chr3, 1856963)
        self.assertEqual(sample.chr4, 1657486)
        self.assertEqual(sample.chr5, 1647483)
        self.assertEqual(sample.chr6, 1570690)
        self.assertEqual(sample.chr7, 1401373)
        self.assertEqual(sample.chr8, 1370342)
        self.assertEqual(sample.chr9, 1069424)
        self.assertEqual(sample.chr10, 1289908)
        self.assertEqual(sample.chr11, 1276737)
        self.assertEqual(sample.chr12, 1246935)
        self.assertEqual(sample.chr13, 860482)
        self.assertEqual(sample.chr14, 835223)
        self.assertEqual(sample.chr15, 776874)
        self.assertEqual(sample.chr16, 758248)
        self.assertEqual(sample.chr17, 741550)
        self.assertEqual(sample.chr18, 721958)
        self.assertEqual(sample.chr19, 497907)
        self.assertEqual(sample.chr20, 632968)
        self.assertEqual(sample.chr21, 334830)
        self.assertEqual(sample.chr22, 336248)
        self.assertEqual(sample.Chrx, 1112927)
        self.assertEqual(sample.chry, 990)
        self.assertTrue(abs(sample.ff_formatted - Decimal("0.07")) < 0.00000001)

        sample = next(iSamples)

        self.assertEqual(sample.sample_type, SampleType.objects.get(name="Control"))
        self.assertEqual(sample.sample_id, "XY012345")
        self.assertEqual(sample.sample_project, "")
        self.assertEqual(sample.index, Index.objects.get(index_id="A025"))
        self.assertEqual(sample.well, "G4")
        self.assertEqual(sample.description, "d3")
        self.assertTrue(abs(sample.library_nm - Decimal("54.9")) < 0.00000001)
        self.assertEqual(sample.qc_flag, 0)
        self.assertEqual(sample.qc_failure, "")
        self.assertEqual(sample.qc_warning, "")
        self.assertTrue(abs(sample.ncv_13 - Decimal("-0.78114759")) < 0.00000001)
        self.assertTrue(abs(sample.ncv_18 - Decimal("-0.68553864")) < 0.00000001)
        self.assertTrue(abs(sample.ncv_21 - Decimal("-0.52671249")) < 0.00000001)
        self.assertTrue(abs(sample.ncv_X - Decimal("-8.0505785")) < 0.00000001)
        self.assertTrue(abs(sample.ncv_Y - Decimal("127.67442885")) < 0.00000001)
        self.assertTrue(abs(sample.ratio_13 - Decimal("0.199670358575887")) < 0.00000001)
        self.assertTrue(abs(sample.ratio_18 - Decimal("0.249283504549480")) < 0.00000001)
        self.assertTrue(abs(sample.ratio_21 - Decimal("0.249706598511657")) < 0.00000001)
        self.assertTrue(abs(sample.ratio_X - Decimal("0.318079522308653")) < 0.00000001)
        self.assertTrue(abs(sample.ratio_y - Decimal("1.5501048888623E-7")) < 0.00000001)
        self.assertEqual(sample.clusters, 559762153)
        self.assertTrue(abs(sample.total_reads_2_clusters - Decimal("1.6")) < 0.00000001)
        self.assertTrue(abs(sample.max_misindexed_reads_2_clusters - 0.0001070008032500904) < 0.00000001)
        self.assertEqual(sample.indexed_reads, 37543895)
        self.assertTrue(abs(sample.total_indexed_reads_2_clusters - Decimal("0.90282028945962")) < 0.00000001)
        self.assertEqual(sample.tags, 30748027)
        self.assertEqual(sample.non_excluded_sites, 28497583)
        self.assertTrue(abs(sample.non_excluded_sites_2_tags - Decimal("0.926810133216027")) < 0.00000001)
        self.assertTrue(abs(sample.tags_2_indexed_reads - Decimal("0.818988733055001")) < 0.00000001)
        self.assertTrue(abs(sample.perfect_match_tags_2_tags - Decimal("0.937845020104867")) < 0.00000001)
        self.assertTrue(abs(sample.gc_bias - Decimal("0.00695")) < 0.00000001)
        self.assertTrue(abs(sample.gcr2 - Decimal("0.13847")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_13 - Decimal("26.1829")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_18 - Decimal("20.43631")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_21 - Decimal("20.49477")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_x - Decimal("15.34822")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_y - Decimal("97.83376")) < 0.00000001)
        self.assertTrue(abs(sample.chr1_coverage - Decimal("1.00149329993")) < 0.00000001)
        self.assertTrue(abs(sample.chr2_coverage - Decimal("1.00005899646")) < 0.00000001)
        self.assertTrue(abs(sample.chr3_coverage - Decimal("1.00071032123")) < 0.00000001)
        self.assertTrue(abs(sample.chr4_coverage - Decimal("1.00122760212")) < 0.00000001)
        self.assertTrue(abs(sample.chr5_coverage - Decimal("0.999845101557")) < 0.00000001)
        self.assertTrue(abs(sample.chr6_coverage - Decimal("0.999594247835")) < 0.00000001)
        self.assertTrue(abs(sample.chr7_coverage - Decimal("1.00015460739")) < 0.00000001)
        self.assertTrue(abs(sample.chr8_coverage - Decimal("1.00107714859")) < 0.00000001)
        self.assertTrue(abs(sample.chr9_coverage - Decimal("1.0013689022")) < 0.00000001)
        self.assertTrue(abs(sample.chr10_coverage - Decimal("0.999746775752")) < 0.00000001)
        self.assertTrue(abs(sample.chr11_coverage - Decimal("0.999034698484")) < 0.00000001)
        self.assertTrue(abs(sample.chr12_coverage - Decimal("1.0010478566")) < 0.00000001)
        self.assertTrue(abs(sample.chr13_coverage - Decimal("0.998531878599")) < 0.00000001)
        self.assertTrue(abs(sample.chr14_coverage - Decimal("0.998791392218")) < 0.00000001)
        self.assertTrue(abs(sample.chr15_coverage - Decimal("0.998253202924")) < 0.00000001)
        self.assertTrue(abs(sample.chr16_coverage - Decimal("1.00149627032")) < 0.00000001)
        self.assertTrue(abs(sample.chr17_coverage - Decimal("0.999200819481")) < 0.00000001)
        self.assertTrue(abs(sample.chr18_coverage - Decimal("0.997892598265")) < 0.00000001)
        self.assertTrue(abs(sample.chr19_coverage - Decimal("1.00384951439")) < 0.00000001)
        self.assertTrue(abs(sample.chr20_coverage - Decimal("1.00099151511")) < 0.00000001)
        self.assertTrue(abs(sample.chr21_coverage - Decimal("0.998723684614")) < 0.00000001)
        self.assertTrue(abs(sample.chr22_coverage - Decimal("0.997762268947")) < 0.00000001)
        self.assertTrue(abs(sample.chrx_coverage - Decimal("0.95419763491")) < 0.00000001)
        self.assertTrue(abs(sample.chry_coverage - Decimal("1.55019633957E-07")) < 0.00000001)
        self.assertEqual(sample.chr1, 2282891)
        self.assertEqual(sample.chr2, 2463877)
        self.assertEqual(sample.chr3, 2043949)
        self.assertEqual(sample.chr4, 1899300)
        self.assertEqual(sample.chr5, 1820069)
        self.assertEqual(sample.chr6, 1735136)
        self.assertEqual(sample.chr7, 1528588)
        self.assertEqual(sample.chr8, 1493903)
        self.assertEqual(sample.chr9, 1141890)
        self.assertEqual(sample.chr10, 1369602)
        self.assertEqual(sample.chr11, 1357742)
        self.assertEqual(sample.chr12, 1347096)
        self.assertEqual(sample.chr13, 976612)
        self.assertEqual(sample.chr14, 899946)
        self.assertEqual(sample.chr15, 815806)
        self.assertEqual(sample.chr16, 764324)
        self.assertEqual(sample.chr17, 746437)
        self.assertEqual(sample.chr18, 790915)
        self.assertEqual(sample.chr19, 481246)
        self.assertEqual(sample.chr20, 641772)
        self.assertEqual(sample.chr21, 363532)
        self.assertEqual(sample.chr22, 327793)
        self.assertEqual(sample.Chrx, 1202844)
        self.assertEqual(sample.chry, 2313)
        self.assertTrue(abs(sample.ff_formatted - Decimal("0.10")) < 0.00000001)

        sample = next(iSamples)

        self.assertEqual(sample.sample_type, SampleType.objects.get(name="Test"))
        self.assertEqual(sample.sample_id, "MN20-1234-BM")
        self.assertEqual(sample.sample_project, "")
        self.assertEqual(sample.index, Index.objects.get(index_id="A003"))
        self.assertEqual(sample.well, "B4")
        self.assertEqual(sample.description, "")
        self.assertTrue(abs(sample.library_nm - Decimal("43.9")) < 0.00000001)
        self.assertEqual(sample.qc_flag, 2)
        self.assertEqual(sample.qc_failure, "NCD_21;NCD_18")
        self.assertEqual(sample.qc_warning, "")
        self.assertEqual(sample.ncv_13, None)
        self.assertEqual(sample.ncv_18, None)
        self.assertEqual(sample.ncv_21, None)
        self.assertEqual(sample.ncv_X, None)
        self.assertEqual(sample.ncv_Y, None)
        self.assertEqual(sample.ratio_13, None)
        self.assertEqual(sample.ratio_18, None)
        self.assertEqual(sample.ratio_21, None)
        self.assertEqual(sample.ratio_X, None)
        self.assertEqual(sample.ratio_y, None)
        self.assertEqual(sample.clusters, 408619234)
        self.assertEqual(sample.total_reads_2_clusters, 1.0)
        self.assertTrue(abs(sample.max_misindexed_reads_2_clusters - 0.00010563624129352658) < 0.00000001)
        self.assertEqual(sample.indexed_reads, 22776432)
        self.assertTrue(abs(sample.total_indexed_reads_2_clusters - Decimal("0.927590662557994")) < 0.00000001)
        self.assertEqual(sample.tags, 17972441)
        self.assertEqual(sample.non_excluded_sites, 16722713)
        self.assertTrue(abs(sample.non_excluded_sites_2_tags - Decimal("0.930464203499124")) < 0.00000001)
        self.assertTrue(abs(sample.tags_2_indexed_reads - Decimal("0.789080616314267")) < 0.00000001)
        self.assertTrue(abs(sample.perfect_match_tags_2_tags - Decimal("0.935393862191563")) < 0.00000001)
        self.assertTrue(abs(sample.gc_bias - Decimal("0.08938")) < 0.00000001)
        self.assertTrue(abs(sample.gcr2 - Decimal("0.81036")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_13 - Decimal("13.15018")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_18 - Decimal("-59.89946")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_21 - Decimal("-75.72517")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_x - Decimal("-47.77625")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_y - Decimal("-90.1483")) < 0.00000001)
        self.assertTrue(abs(sample.chr1_coverage - Decimal("0.997787570191")) < 0.00000001)
        self.assertTrue(abs(sample.chr2_coverage - Decimal("0.993370110807")) < 0.00000001)
        self.assertTrue(abs(sample.chr3_coverage - Decimal("1.00222816166")) < 0.00000001)
        self.assertTrue(abs(sample.chr4_coverage - Decimal("1.00148714309")) < 0.00000001)
        self.assertTrue(abs(sample.chr5_coverage - Decimal("1.00238904966")) < 0.00000001)
        self.assertTrue(abs(sample.chr6_coverage - Decimal("0.994059786989")) < 0.00000001)
        self.assertTrue(abs(sample.chr7_coverage - Decimal("1.00410951749")) < 0.00000001)
        self.assertTrue(abs(sample.chr8_coverage - Decimal("0.999882726324")) < 0.00000001)
        self.assertTrue(abs(sample.chr9_coverage - Decimal("0.996999756351")) < 0.00000001)
        self.assertTrue(abs(sample.chr10_coverage - Decimal("0.99719996531")) < 0.00000001)
        self.assertTrue(abs(sample.chr11_coverage - Decimal("0.999751505041")) < 0.00000001)
        self.assertTrue(abs(sample.chr12_coverage - Decimal("1.00327138225")) < 0.00000001)
        self.assertTrue(abs(sample.chr13_coverage - Decimal("0.997911936493")) < 0.00000001)
        self.assertTrue(abs(sample.chr14_coverage - Decimal("0.995225512295")) < 0.00000001)
        self.assertTrue(abs(sample.chr15_coverage - Decimal("0.994999526549")) < 0.00000001)
        self.assertTrue(abs(sample.chr16_coverage - Decimal("1.01100101117")) < 0.00000001)
        self.assertTrue(abs(sample.chr17_coverage - Decimal("1.00258251107")) < 0.00000001)
        self.assertTrue(abs(sample.chr18_coverage - Decimal("0.999604849356")) < 0.00000001)
        self.assertTrue(abs(sample.chr19_coverage - Decimal("1.02610547408")) < 0.00000001)
        self.assertTrue(abs(sample.chr20_coverage - Decimal("0.965150624458")) < 0.00000001)
        self.assertTrue(abs(sample.chr21_coverage - Decimal("0.992689922444")) < 0.00000001)
        self.assertTrue(abs(sample.chr22_coverage - Decimal("1.00203732591")) < 0.00000001)
        self.assertTrue(abs(sample.chrx_coverage - Decimal("0.996733350503")) < 0.00000001)
        self.assertTrue(abs(sample.chry_coverage - Decimal("8.89324434289E-09")) < 0.00000001)
        self.assertEqual(sample.chr1, 1359202)
        self.assertEqual(sample.chr2, 1424941)
        self.assertEqual(sample.chr3, 1176848)
        self.assertEqual(sample.chr4, 1046405)
        self.assertEqual(sample.chr5, 1044219)
        self.assertEqual(sample.chr6, 990893)
        self.assertEqual(sample.chr7, 890084)
        self.assertEqual(sample.chr8, 867352)
        self.assertEqual(sample.chr9, 675439)
        self.assertEqual(sample.chr10, 823124)
        self.assertEqual(sample.chr11, 807993)
        self.assertEqual(sample.chr12, 790859)
        self.assertEqual(sample.chr13, 543097)
        self.assertEqual(sample.chr14, 527251)
        self.assertEqual(sample.chr15, 495880)
        self.assertEqual(sample.chr16, 482936)
        self.assertEqual(sample.chr17, 470399)
        self.assertEqual(sample.chr18, 459740)
        self.assertEqual(sample.chr19, 313281)
        self.assertEqual(sample.chr20, 389084)
        self.assertEqual(sample.chr21, 212090)
        self.assertEqual(sample.chr22, 214202)
        self.assertEqual(sample.Chrx, 717316)
        self.assertEqual(sample.chry, 78)
        self.assertEqual(sample.ff_formatted, None)

        sample = next(iSamples)

        self.assertEqual(sample.sample_type, SampleType.objects.get(name="Test"))
        self.assertEqual(sample.sample_id, "LK19-4321-C-BM")
        self.assertEqual(sample.sample_project, "")
        self.assertEqual(sample.index, Index.objects.get(index_id="A010"))
        self.assertEqual(sample.well, "D4")
        self.assertEqual(sample.description, "")
        self.assertTrue(abs(sample.library_nm - Decimal("61.2")) < 0.00000001)
        self.assertEqual(sample.qc_flag, 0)
        self.assertEqual(sample.qc_failure, "")
        self.assertEqual(sample.qc_warning, "")
        self.assertTrue(abs(sample.ncv_13 - Decimal("2.94861252")) < 0.00000001)
        self.assertTrue(abs(sample.ncv_18 - Decimal("-0.12303047")) < 0.00000001)
        self.assertTrue(abs(sample.ncv_21 - Decimal("-0.88540654")) < 0.00000001)
        self.assertTrue(abs(sample.ncv_X - Decimal("2.05340098")) < 0.00000001)
        self.assertTrue(abs(sample.ncv_Y - Decimal("-0.7353879")) < 0.00000001)
        self.assertTrue(abs(sample.ratio_13 - Decimal("0.201117789842433")) < 0.00000001)
        self.assertTrue(abs(sample.ratio_18 - Decimal("0.249772895752413")) < 0.00000001)
        self.assertTrue(abs(sample.ratio_21 - Decimal("0.249002860632985")) < 0.00000001)
        self.assertTrue(abs(sample.ratio_X - Decimal("0.336744893377815")) < 0.00000001)
        self.assertTrue(abs(sample.ratio_y - Decimal("6.3083996516E-09")) < 0.00000001)
        self.assertEqual(sample.clusters, 477059374)
        self.assertEqual(sample.total_reads_2_clusters, 1.0)
        self.assertTrue(abs(sample.max_misindexed_reads_2_clusters - 0.0001165892612771508) < 0.00000001)
        self.assertEqual(sample.indexed_reads, 25876409)
        self.assertTrue(abs(sample.total_indexed_reads_2_clusters - Decimal("0.918689278286774")) < 0.00000001)
        self.assertEqual(sample.tags, 20923248)
        self.assertEqual(sample.non_excluded_sites, 19495863)
        self.assertTrue(abs(sample.non_excluded_sites_2_tags - Decimal("0.931779951181576")) < 0.00000001)
        self.assertTrue(abs(sample.tags_2_indexed_reads - Decimal("0.808583911314742")) < 0.00000001)
        self.assertTrue(abs(sample.perfect_match_tags_2_tags - Decimal("0.937639079745171")) < 0.00000001)
        self.assertTrue(abs(sample.gc_bias - Decimal("0.0517")) < 0.00000001)
        self.assertTrue(abs(sample.gcr2 - Decimal("0.6581")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_13 - Decimal("16.75418")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_18 - Decimal("17.09129")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_21 - Decimal("11.96289")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_x - Decimal("14.79218")) < 0.00000001)
        self.assertTrue(abs(sample.ncd_y - Decimal("65.04944")) < 0.00000001)
        self.assertTrue(abs(sample.chr1_coverage - Decimal("0.998184128404")) < 0.00000001)
        self.assertTrue(abs(sample.chr2_coverage - Decimal("0.99441250147")) < 0.00000001)
        self.assertTrue(abs(sample.chr3_coverage - Decimal("1.00122891271")) < 0.00000001)
        self.assertTrue(abs(sample.chr4_coverage - Decimal("1.00322562984")) < 0.00000001)
        self.assertTrue(abs(sample.chr5_coverage - Decimal("1.00060542301")) < 0.00000001)
        self.assertTrue(abs(sample.chr6_coverage - Decimal("0.995303956252")) < 0.00000001)
        self.assertTrue(abs(sample.chr7_coverage - Decimal("1.0058501427")) < 0.00000001)
        self.assertTrue(abs(sample.chr8_coverage - Decimal("1.00104966922")) < 0.00000001)
        self.assertTrue(abs(sample.chr9_coverage - Decimal("1.00057124671")) < 0.00000001)
        self.assertTrue(abs(sample.chr10_coverage - Decimal("0.994357680568")) < 0.00000001)
        self.assertTrue(abs(sample.chr11_coverage - Decimal("0.997745131629")) < 0.00000001)
        self.assertTrue(abs(sample.chr12_coverage - Decimal("1.00128531106")) < 0.00000001)
        self.assertTrue(abs(sample.chr13_coverage - Decimal("1.00330609959")) < 0.00000001)
        self.assertTrue(abs(sample.chr14_coverage - Decimal("0.995603709857")) < 0.00000001)
        self.assertTrue(abs(sample.chr15_coverage - Decimal("0.990864677651")) < 0.00000001)
        self.assertTrue(abs(sample.chr16_coverage - Decimal("1.00445280196")) < 0.00000001)
        self.assertTrue(abs(sample.chr17_coverage - Decimal("0.998282886014")) < 0.00000001)
        self.assertTrue(abs(sample.chr18_coverage - Decimal("0.998627237515")) < 0.00000001)
        self.assertTrue(abs(sample.chr19_coverage - Decimal("1.03343426291")) < 0.00000001)
        self.assertTrue(abs(sample.chr20_coverage - Decimal("0.999507949576")) < 0.00000001)
        self.assertTrue(abs(sample.chr21_coverage - Decimal("0.99199797495")) < 0.00000001)
        self.assertTrue(abs(sample.chr22_coverage - Decimal("1.00312572838")) < 0.00000001)
        self.assertTrue(abs(sample.chrx_coverage - Decimal("1.00951354236")) < 0.00000001)
        self.assertTrue(abs(sample.chry_coverage - Decimal("6.27315147782E-09")) < 0.00000001)
        self.assertEqual(sample.chr1, 1572441)
        self.assertEqual(sample.chr2, 1671071)
        self.assertEqual(sample.chr3, 1383408)
        self.assertEqual(sample.chr4, 1241807)
        self.assertEqual(sample.chr5, 1227919)
        self.assertEqual(sample.chr6, 1166992)
        self.assertEqual(sample.chr7, 1040444)
        self.assertEqual(sample.chr8, 1021504)
        self.assertEqual(sample.chr9, 785567)
        self.assertEqual(sample.chr10, 950552)
        self.assertEqual(sample.chr11, 932991)
        self.assertEqual(sample.chr12, 919019)
        self.assertEqual(sample.chr13, 647704)
        self.assertEqual(sample.chr14, 613962)
        self.assertEqual(sample.chr15, 571071)
        self.assertEqual(sample.chr16, 544475)
        self.assertEqual(sample.chr17, 525739)
        self.assertEqual(sample.chr18, 539308)
        self.assertEqual(sample.chr19, 342031)
        self.assertEqual(sample.chr20, 457425)
        self.assertEqual(sample.chr21, 244288)
        self.assertEqual(sample.chr22, 235981)
        self.assertEqual(sample.Chrx, 860100)
        self.assertEqual(sample.chry, 64)
        self.assertTrue(abs(sample.ff_formatted - Decimal("0.01")) < 0.00000001)

    def test_data_import_multiple_barcode(self):
        csv = open("./dataprocessor/tests/200809_NDX123456_RUO_0001_ABCDEFGHIJ_NIPT_RESULTS_MULTIPLE_BARCODE.csv")
        from .utils.data import import_data_into_database
        # Expects an exception
        try:
            flowcell_barcode = import_data_into_database(self.user, csv)
            self.assertTrue(False)
        except Exception as e:
            self.assertEqual(str(e), "Multiple flowcell barcodes specified in the provided file: ABCDEFGHI, ABCDEFGHJ")

    def test_data_import_wrong_barcode_length(self):
        csv = open("./dataprocessor/tests/200809_NDX123456_RUO_0001_ABCDEFGHIJ_NIPT_RESULTS_WRONG_BARCODE_LENGTH.csv")
        from .utils.data import import_data_into_database
        # Expects an exception
        try:
            flowcell_barcode = import_data_into_database(self.user, csv)
            self.assertTrue(False)
        except Exception as e:
            self.assertEqual(str(e), "Invalid Flowcell bardcode length, should be 9 chars, found: 8")

    def test_csv_parsing_modified_header(self):
        from .utils.data import parse_niptool_csv, import_data_into_database
        # Expects an exception
        try:
            csv = open("./dataprocessor/tests/200809_NDX123456_RUO_0001_ABCDEFGHIJ_NIPT_RESULTS_MOD_HEADER.csv")
            parse_niptool_csv(csv)
            self.assertTrue(False)
        except KeyError as e:
            self.assertEqual(str(e), "'SampleProject'")

        # Expects an exception
        try:
            csv = open("./dataprocessor/tests/200809_NDX123456_RUO_0001_ABCDEFGHIJ_NIPT_RESULTS_MOD_HEADER.csv")
            import_data_into_database(self.user, csv)
            self.assertTrue(False)
        except KeyError as e:
            self.assertEqual(str(e), "'SampleProject'")
