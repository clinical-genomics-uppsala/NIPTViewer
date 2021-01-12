from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command



class UtilDataTestTestsCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Testuser')
        self.admin_ser = User.objects.create(username='admin')

        call_command("loaddata","index", app_label='dataprocessor')
        call_command("loaddata","sample_types", app_label='dataprocessor')

        csv = open("./dataprocessor/tests/200809_NDX123456_RUO_0001_ABCDEFGHIJ_NIPT_RESULTS.csv")
        from dataprocessor.utils.data import import_data_into_database
        import_data_into_database(self.user,csv)

    def test_extract_qc_status(self):
        from dataprocessor.models import Flowcell, SamplesRunData

        samples = SamplesRunData.objects.filter(flowcell_id=Flowcell.objects.get(flowcell_barcode="ABCDEFGHI"))
        from .utils.data import extract_qc_status
        qc_failure, qc_warning = extract_qc_status(samples)
        self.assertEqual(qc_failure, [('120AB-1', 'NCC;'), ('MN20-1234-BM', 'NCD_21;NCD_18')])
        self.assertEqual(qc_warning, [('120AB-1', 'ACB'), ('MN20-1234-BM', '')])

    def test_extra_info_samples(self):
        from dataprocessor.models import Flowcell, SamplesRunData

        samples = SamplesRunData.objects.filter(flowcell_id=Flowcell.objects.get(flowcell_barcode="ABCDEFGHI"))
        from .utils.data import extract_info_samples, extra_info_per_sample, sample_info
        data = extract_info_samples(samples, sample_info())

        self.assertEqual(data['x_vs_y']['data']['120AB-1'], [{'x': -3.46129478, 'y': 54.04707311, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '120AB-1'}])
        self.assertEqual(data['x_vs_y']['data']['130VY-2'], [{'x': -3.2939618, 'y': 55.3614837, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '130VY-2'}])
        self.assertEqual(data['x_vs_y']['data']['XY012345'], [{'x': -8.0505785, 'y': 127.67442885, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Control', 'flowcell': 'ABCDEFGHI', 'sample': 'XY012345'}])
        self.assertEqual(data['x_vs_y']['data']['LK19-4321-C-BM'],[{'x': 2.05340098, 'y': -0.7353879, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': 'LK19-4321-C-BM'}] )
        self.assertEqual(data['x_vs_y']['fields'], ('ncv_X', 'ncv_Y'))

        self.assertEqual(data['x_vs_ff']['data']['120AB-1'], [{'x': -3.46129478, 'y': 0.08, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '120AB-1'}])
        self.assertEqual(data['x_vs_ff']['data']['130VY-2'], [{'x': -3.2939618, 'y': 0.07, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '130VY-2'}])
        self.assertEqual(data['x_vs_ff']['data']['XY012345'], [{'x': -8.0505785, 'y': 0.1, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Control', 'flowcell': 'ABCDEFGHI', 'sample': 'XY012345'}])
        self.assertEqual(data['x_vs_ff']['data']['LK19-4321-C-BM'], [{'x': 2.05340098, 'y': 0.01, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': 'LK19-4321-C-BM'}])
        self.assertEqual(data['x_vs_ff']['fields'], ('ncv_X', 'ff_formatted'))

        self.assertEqual(data['y_vs_ff']['data']['120AB-1'], [{'x': 54.04707311, 'y': 0.08, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '120AB-1'}])
        self.assertEqual(data['y_vs_ff']['data']['130VY-2'], [{'x': 55.3614837, 'y': 0.07, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '130VY-2'}])
        self.assertEqual(data['y_vs_ff']['data']['XY012345'], [{'x': 127.67442885, 'y': 0.1, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Control', 'flowcell': 'ABCDEFGHI', 'sample': 'XY012345'}])
        self.assertEqual(data['y_vs_ff']['data']['LK19-4321-C-BM'], [{'x': -0.7353879, 'y': 0.01, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': 'LK19-4321-C-BM'}])
        self.assertEqual(data['y_vs_ff']['fields'], ('ncv_Y', 'ff_formatted'))

        self.assertEqual(data['chr13_vs_ff']['data']['120AB-1'], [{'x': -0.65537058, 'y': 0.08, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '120AB-1'}])
        self.assertEqual(data['chr13_vs_ff']['data']['130VY-2'], [{'x': -0.85104066, 'y': 0.07, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '130VY-2'}])
        self.assertEqual(data['chr13_vs_ff']['data']['XY012345'], [{'x': -0.78114759, 'y': 0.1, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Control', 'flowcell': 'ABCDEFGHI', 'sample': 'XY012345'}])
        self.assertEqual(data['chr13_vs_ff']['data']['LK19-4321-C-BM'], [{'x': 2.94861252, 'y': 0.01, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': 'LK19-4321-C-BM'}])
        self.assertEqual(data['chr13_vs_ff']['fields'], ('ncv_13', 'ff_formatted'))

        self.assertEqual(data['chr18_vs_ff']['data']['120AB-1'], [{'x': -0.26181607, 'y': 0.08, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '120AB-1'}])
        self.assertEqual(data['chr18_vs_ff']['data']['130VY-2'], [{'x': -0.27928844, 'y': 0.07, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '130VY-2'}])
        self.assertEqual(data['chr18_vs_ff']['data']['XY012345'], [{'x': -0.68553864, 'y': 0.1, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Control', 'flowcell': 'ABCDEFGHI', 'sample': 'XY012345'}])
        self.assertEqual(data['chr18_vs_ff']['data']['LK19-4321-C-BM'], [{'x': -0.12303047, 'y': 0.01, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': 'LK19-4321-C-BM'}])
        self.assertEqual(data['chr18_vs_ff']['fields'], ('ncv_18', 'ff_formatted'))

        self.assertEqual(data['chr21_vs_ff']['data']['120AB-1'], [{'x': 0.03433961, 'y': 0.08, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '120AB-1'}])
        self.assertEqual(data['chr21_vs_ff']['data']['130VY-2'], [{'x': -0.72567932, 'y': 0.07, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '130VY-2'}])
        self.assertEqual(data['chr21_vs_ff']['data']['XY012345'], [{'x': -0.52671249, 'y': 0.1, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Control', 'flowcell': 'ABCDEFGHI', 'sample': 'XY012345'}])
        self.assertEqual(data['chr21_vs_ff']['data']['LK19-4321-C-BM'], [{'x': -0.88540654, 'y': 0.01, 'shape': 'circle', 'size': 1.0, 'color': '#bdbdbd', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': 'LK19-4321-C-BM'}])
        self.assertEqual(data['chr21_vs_ff']['fields'], ('ncv_21', 'ff_formatted'))

    def test_extra_info_per_samples(self):
        from dataprocessor.models import Flowcell, SamplesRunData

        samples = SamplesRunData.objects.filter(flowcell_id=Flowcell.objects.get(flowcell_barcode="ABCDEFGHI"))
        from .utils.data import extra_info_per_sample, sample_info
        from .utils.colors import samples as colors
        colors ,data = extra_info_per_sample(samples, sample_info(), colors=colors[:3])

        self.assertEqual(colors['120AB-1'], '#140c1c')
        self.assertEqual(colors['130VY-2'], '#442434')
        self.assertEqual(colors['XY012345'], '#30346d')
        self.assertEqual(colors['MN20-1234-BM'], '#140c1c') # No NCV entries due to qc failure
        self.assertEqual(colors['LK19-4321-C-BM'], '#442434')

        self.assertEqual(data['x_vs_y']['data']['120AB-1'], [{'x': -3.46129478, 'y': 54.04707311, 'shape': 'circle', 'size': 1.0, 'color': '#140c1c', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '120AB-1'}])
        self.assertEqual(data['x_vs_y']['data']['130VY-2'], [{'x': -3.2939618, 'y': 55.3614837, 'shape': 'circle', 'size': 1.0, 'color': '#442434', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '130VY-2'}])
        self.assertEqual(data['x_vs_y']['data']['XY012345'], [{'x': -8.0505785, 'y': 127.67442885, 'shape': 'circle', 'size': 1.0, 'color': '#30346d', 'type': 'Control', 'flowcell': 'ABCDEFGHI', 'sample': 'XY012345'}])
        self.assertEqual(data['x_vs_y']['data']['LK19-4321-C-BM'],[{'x': 2.05340098, 'y': -0.7353879, 'shape': 'circle', 'size': 1.0, 'color': '#442434', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': 'LK19-4321-C-BM'}] )
        self.assertEqual(data['x_vs_y']['fields'], ('ncv_X', 'ncv_Y'))

        self.assertEqual(data['x_vs_ff']['data']['120AB-1'], [{'x': -3.46129478, 'y': 0.08, 'shape': 'circle', 'size': 1.0, 'color': '#140c1c', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '120AB-1'}])
        self.assertEqual(data['x_vs_ff']['data']['130VY-2'], [{'x': -3.2939618, 'y': 0.07, 'shape': 'circle', 'size': 1.0, 'color': '#442434', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '130VY-2'}])
        self.assertEqual(data['x_vs_ff']['data']['XY012345'], [{'x': -8.0505785, 'y': 0.1, 'shape': 'circle', 'size': 1.0, 'color': '#30346d', 'type': 'Control', 'flowcell': 'ABCDEFGHI', 'sample': 'XY012345'}])
        self.assertEqual(data['x_vs_ff']['data']['LK19-4321-C-BM'], [{'x': 2.05340098, 'y': 0.01, 'shape': 'circle', 'size': 1.0, 'color': '#442434', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': 'LK19-4321-C-BM'}])
        self.assertEqual(data['x_vs_ff']['fields'], ('ncv_X', 'ff_formatted'))

        self.assertEqual(data['y_vs_ff']['data']['120AB-1'], [{'x': 54.04707311, 'y': 0.08, 'shape': 'circle', 'size': 1.0, 'color': '#140c1c', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '120AB-1'}])
        self.assertEqual(data['y_vs_ff']['data']['130VY-2'], [{'x': 55.3614837, 'y': 0.07, 'shape': 'circle', 'size': 1.0, 'color': '#442434', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '130VY-2'}])
        self.assertEqual(data['y_vs_ff']['data']['XY012345'], [{'x': 127.67442885, 'y': 0.1, 'shape': 'circle', 'size': 1.0, 'color': '#30346d', 'type': 'Control', 'flowcell': 'ABCDEFGHI', 'sample': 'XY012345'}])
        self.assertEqual(data['y_vs_ff']['data']['LK19-4321-C-BM'], [{'x': -0.7353879, 'y': 0.01, 'shape': 'circle', 'size': 1.0, 'color': '#442434', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': 'LK19-4321-C-BM'}])
        self.assertEqual(data['y_vs_ff']['fields'], ('ncv_Y', 'ff_formatted'))

        self.assertEqual(data['chr13_vs_ff']['data']['120AB-1'], [{'x': -0.65537058, 'y': 0.08, 'shape': 'circle', 'size': 1.0, 'color': '#140c1c', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '120AB-1'}])
        self.assertEqual(data['chr13_vs_ff']['data']['130VY-2'], [{'x': -0.85104066, 'y': 0.07, 'shape': 'circle', 'size': 1.0, 'color': '#442434', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '130VY-2'}])
        self.assertEqual(data['chr13_vs_ff']['data']['XY012345'], [{'x': -0.78114759, 'y': 0.1, 'shape': 'circle', 'size': 1.0, 'color': '#30346d', 'type': 'Control', 'flowcell': 'ABCDEFGHI', 'sample': 'XY012345'}])
        self.assertEqual(data['chr13_vs_ff']['data']['LK19-4321-C-BM'], [{'x': 2.94861252, 'y': 0.01, 'shape': 'circle', 'size': 1.0, 'color': '#442434', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': 'LK19-4321-C-BM'}])
        self.assertEqual(data['chr13_vs_ff']['fields'], ('ncv_13', 'ff_formatted'))

        self.assertEqual(data['chr18_vs_ff']['data']['120AB-1'], [{'x': -0.26181607, 'y': 0.08, 'shape': 'circle', 'size': 1.0, 'color': '#140c1c', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '120AB-1'}])
        self.assertEqual(data['chr18_vs_ff']['data']['130VY-2'], [{'x': -0.27928844, 'y': 0.07, 'shape': 'circle', 'size': 1.0, 'color': '#442434', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '130VY-2'}])
        self.assertEqual(data['chr18_vs_ff']['data']['XY012345'], [{'x': -0.68553864, 'y': 0.1, 'shape': 'circle', 'size': 1.0, 'color': '#30346d', 'type': 'Control', 'flowcell': 'ABCDEFGHI', 'sample': 'XY012345'}])
        self.assertEqual(data['chr18_vs_ff']['data']['LK19-4321-C-BM'], [{'x': -0.12303047, 'y': 0.01, 'shape': 'circle', 'size': 1.0, 'color': '#442434', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': 'LK19-4321-C-BM'}])
        self.assertEqual(data['chr18_vs_ff']['fields'], ('ncv_18', 'ff_formatted'))

        self.assertEqual(data['chr21_vs_ff']['data']['120AB-1'], [{'x': 0.03433961, 'y': 0.08, 'shape': 'circle', 'size': 1.0, 'color': '#140c1c', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '120AB-1'}])
        self.assertEqual(data['chr21_vs_ff']['data']['130VY-2'], [{'x': -0.72567932, 'y': 0.07, 'shape': 'circle', 'size': 1.0, 'color': '#442434', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '130VY-2'}])
        self.assertEqual(data['chr21_vs_ff']['data']['XY012345'], [{'x': -0.52671249, 'y': 0.1, 'shape': 'circle', 'size': 1.0, 'color': '#30346d', 'type': 'Control', 'flowcell': 'ABCDEFGHI', 'sample': 'XY012345'}])
        self.assertEqual(data['chr21_vs_ff']['data']['LK19-4321-C-BM'], [{'x': -0.88540654, 'y': 0.01, 'shape': 'circle', 'size': 1.0, 'color': '#442434', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': 'LK19-4321-C-BM'}])
        self.assertEqual(data['chr21_vs_ff']['fields'], ('ncv_21', 'ff_formatted'))


class UtilPlotsTestTestsCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Testuser')
        self.admin_ser = User.objects.create(username='admin')

        call_command("loaddata","index", app_label='dataprocessor')
        call_command("loaddata","sample_types", app_label='dataprocessor')

        csv = open("./dataprocessor/tests/200809_NDX123456_RUO_0001_ABCDEFGHIJ_NIPT_RESULTS.csv")
        from dataprocessor.utils.data import import_data_into_database
        import_data_into_database(self.user,csv)

    def test_chromosome_percentage_reads(self):
        from dataprocessor.models import Flowcell, SamplesRunData

        samples = SamplesRunData.objects.filter(flowcell_id=Flowcell.objects.get(flowcell_barcode="ABCDEFGHI"))
        from .utils.plots import chromosome_percentage_reads

        data = chromosome_percentage_reads(samples)
        self.assertEqual(len(data),24)
        self.assertEqual(data[0], {'key': 'Chr1', 'values': [{'x': 0, 'y': 0.01959082251048674, 'label': '120AB-1'}, {'x': 0, 'y': 0.017825590995162167, 'label': '130VY-2'}, {'x': 0, 'y': 0.018998600452830753, 'label': 'XY012345'}, {'x': 0, 'y': 0.011311506214133071, 'label': 'MN20-1234-BM'}, {'x': 0, 'y': 0.013086116811818716, 'label': 'LK19-4321-C-BM'}]})
        self.assertEqual(data[1], {'key': 'Chr2', 'values': [{'x': 1, 'y': 0.020694000663726116, 'label': '120AB-1'}, {'x': 1, 'y': 0.018758597474826465, 'label': '130VY-2'}, {'x': 1, 'y': 0.02050479619391345, 'label': 'XY012345'}, {'x': 1, 'y': 0.01185859715941633, 'label': 'MN20-1234-BM'}, {'x': 1, 'y': 0.013906932156337003, 'label': 'LK19-4321-C-BM'}]})
        self.assertEqual(data[2], {'key': 'Chr3', 'values': [{'x': 2, 'y': 0.017109352002861428, 'label': '120AB-1'}, {'x': 2, 'y': 0.015453956449383676, 'label': '130VY-2'}, {'x': 2, 'y': 0.017010085193275966, 'label': 'XY012345'}, {'x': 2, 'y': 0.009793925748409786, 'label': 'MN20-1234-BM'}, {'x': 2, 'y': 0.011512952591801223, 'label': 'LK19-4321-C-BM'}]})
        self.assertEqual(data[3], {'key': 'Chr4', 'values': [{'x': 3, 'y': 0.015355729910690081, 'label': '120AB-1'}, {'x': 3, 'y': 0.013793875515808959, 'label': '130VY-2'}, {'x': 3, 'y': 0.01580629203937527, 'label': 'XY012345'}, {'x': 3, 'y': 0.008708357300827925, 'label': 'MN20-1234-BM'}, {'x': 3, 'y': 0.010334525403327797, 'label': 'LK19-4321-C-BM'}]})
        self.assertEqual(data[4], {'key': 'Chr5', 'values': [{'x': 4, 'y': 0.015176770028620515, 'label': '120AB-1'}, {'x': 4, 'y': 0.01371062887795824, 'label': '130VY-2'}, {'x': 4, 'y': 0.015146918415107517, 'label': 'XY012345'}, {'x': 4, 'y': 0.008690165043470964, 'label': 'MN20-1234-BM'}, {'x': 4, 'y': 0.01021894714615787, 'label': 'LK19-4321-C-BM'}]})
        self.assertEqual(data[5], {'key': 'Chr6', 'values': [{'x': 5, 'y': 0.014454530753815491, 'label': '120AB-1'}, {'x': 5, 'y': 0.013071544697165451, 'label': '130VY-2'}, {'x': 5, 'y': 0.014440091793836384, 'label': 'XY012345'}, {'x': 5, 'y': 0.008246377158833612, 'label': 'MN20-1234-BM'}, {'x': 5, 'y': 0.009711902469127901, 'label': 'LK19-4321-C-BM'}]})
        self.assertEqual(data[6], {'key': 'Chr7', 'values': [{'x': 6, 'y': 0.012882173784010086, 'label': '120AB-1'}, {'x': 6, 'y': 0.011662460324380265, 'label': '130VY-2'}, {'x': 6, 'y': 0.012721164816450567, 'label': 'XY012345'}, {'x': 6, 'y': 0.0074074278121283085, 'label': 'MN20-1234-BM'}, {'x': 6, 'y': 0.008658748862536599, 'label': 'LK19-4321-C-BM'}]})
        self.assertEqual(data[7], {'key': 'Chr8', 'values': [{'x': 7, 'y': 0.0125527824088095, 'label': '120AB-1'}, {'x': 7, 'y': 0.011404215156016207, 'label': '130VY-2'}, {'x': 7, 'y': 0.012432510449375472, 'label': 'XY012345'}, {'x': 7, 'y': 0.0072182483088170475, 'label': 'MN20-1234-BM'}, {'x': 7, 'y': 0.008501127017000997, 'label': 'LK19-4321-C-BM'}]})
        self.assertEqual(data[8], {'key': 'Chr9', 'values': [{'x': 8, 'y': 0.009761502585252093, 'label': '120AB-1'}, {'x': 8, 'y': 0.008899925266106912, 'label': '130VY-2'}, {'x': 8, 'y': 0.009502999429706853, 'label': 'XY012345'}, {'x': 8, 'y': 0.005621116247450951, 'label': 'MN20-1234-BM'}, {'x': 8, 'y': 0.00653761986968668, 'label': 'LK19-4321-C-BM'}]})
        self.assertEqual(data[9], {'key': 'Chr10', 'values': [{'x': 9, 'y': 0.011766770367249496, 'label': '120AB-1'}, {'x': 9, 'y': 0.010734829964685133, 'label': '130VY-2'}, {'x': 9, 'y': 0.011398056752336358, 'label': 'XY012345'}, {'x': 9, 'y': 0.0068501755007733, 'label': 'MN20-1234-BM'}, {'x': 9, 'y': 0.007910652614443342, 'label': 'LK19-4321-C-BM'}]})
        self.assertEqual(data[10], {'key': 'Chr11', 'values': [{'x': 10, 'y': 0.011664565832665404, 'label': '120AB-1'}, {'x': 10, 'y': 0.010625218701350952, 'label': '130VY-2'}, {'x': 10, 'y': 0.011299355850116072, 'label': 'XY012345'}, {'x': 10, 'y': 0.006724252789854652, 'label': 'MN20-1234-BM'}, {'x': 10, 'y': 0.007764507037386812, 'label': 'LK19-4321-C-BM'}]})
        self.assertEqual(data[11], {'key': 'Chr12', 'values': [{'x': 11, 'y': 0.011414509676762118, 'label': '120AB-1'}, {'x': 11, 'y': 0.010377201476395726, 'label': '130VY-2'}, {'x': 11, 'y': 0.011210758058797593, 'label': 'XY012345'}, {'x': 11, 'y': 0.006581660778164737, 'label': 'MN20-1234-BM'}, {'x': 11, 'y': 0.00764822971817755, 'label': 'LK19-4321-C-BM'}]})
        self.assertEqual(data[12], {'key': 'Chr13', 'values': [{'x': 12, 'y': 0.007952737813644691, 'label': '120AB-1'}, {'x': 12, 'y': 0.007161075020600069, 'label': '130VY-2'}, {'x': 12, 'y': 0.008127528289979655, 'label': 'XY012345'}, {'x': 12, 'y': 0.004519744004479856, 'label': 'MN20-1234-BM'}, {'x': 12, 'y': 0.005390300941963628, 'label': 'LK19-4321-C-BM'}]})
        self.assertEqual(data[13], {'key': 'Chr14', 'values': [{'x': 13, 'y': 0.007643843936097441, 'label': '120AB-1'}, {'x': 13, 'y': 0.006950865400938836, 'label': '130VY-2'}, {'x': 13, 'y': 0.007489501024413002, 'label': 'XY012345'}, {'x': 13, 'y': 0.004387870944059733, 'label': 'MN20-1234-BM'}, {'x': 13, 'y': 0.005109494378496772, 'label': 'LK19-4321-C-BM'}]})
        self.assertEqual(data[14], {'key': 'Chr15', 'values': [{'x': 14, 'y': 0.007078028114760587, 'label': '120AB-1'}, {'x': 14, 'y': 0.006465275270782721, 'label': '130VY-2'}, {'x': 14, 'y': 0.006789273881679872, 'label': 'XY012345'}, {'x': 14, 'y': 0.004126796238869798, 'label': 'MN20-1234-BM'}, {'x': 14, 'y': 0.004752548307912428, 'label': 'LK19-4321-C-BM'}]})
        self.assertEqual(data[15], {'key': 'Chr16', 'values': [{'x': 15, 'y': 0.0068431682360456875, 'label': '120AB-1'}, {'x': 15, 'y': 0.006310266585727488, 'label': '130VY-2'}, {'x': 15, 'y': 0.0063608320732393316, 'label': 'XY012345'}, {'x': 15, 'y': 0.004019074107475246, 'label': 'MN20-1234-BM'}, {'x': 15, 'y': 0.004531211950791791, 'label': 'LK19-4321-C-BM'}]})
        self.assertEqual(data[16], {'key': 'Chr17', 'values': [{'x': 16, 'y': 0.00668199282514347, 'label': '120AB-1'}, {'x': 16, 'y': 0.006171303038908403, 'label': '130VY-2'}, {'x': 16, 'y': 0.0062119734696968135, 'label': 'XY012345'}, {'x': 16, 'y': 0.003914739098104611, 'label': 'MN20-1234-BM'}, {'x': 16, 'y': 0.004375287827351716, 'label': 'LK19-4321-C-BM'}]})
        self.assertEqual(data[17], {'key': 'Chr18', 'values': [{'x': 17, 'y': 0.0066220732217719645, 'label': '120AB-1'}, {'x': 17, 'y': 0.006008255140400827, 'label': '130VY-2'}, {'x': 17, 'y': 0.006582126819524294, 'label': 'XY012345'}, {'x': 17, 'y': 0.0038260331186133765, 'label': 'MN20-1234-BM'}, {'x': 17, 'y': 0.004488211313205601, 'label': 'LK19-4321-C-BM'}]})
        self.assertEqual(data[18], {'key': 'Chr19', 'values': [{'x': 18, 'y': 0.004441066236386214, 'label': '120AB-1'}, {'x': 18, 'y': 0.004143665271652304, 'label': '130VY-2'}, {'x': 18, 'y': 0.004005009645017212, 'label': 'XY012345'}, {'x': 18, 'y': 0.002607176842198454, 'label': 'MN20-1234-BM'}, {'x': 18, 'y': 0.0028464391473277326, 'label': 'LK19-4321-C-BM'}]})
        self.assertEqual(data[19], {'key': 'Chr20', 'values': [{'x': 19, 'y': 0.005723379037204989, 'label': '120AB-1'}, {'x': 19, 'y': 0.005267665487063279, 'label': '130VY-2'}, {'x': 19, 'y': 0.005340933846519215, 'label': 'XY012345'}, {'x': 19, 'y': 0.003238022077527661, 'label': 'MN20-1234-BM'}, {'x': 19, 'y': 0.00380676730169601, 'label': 'LK19-4321-C-BM'}]})
        self.assertEqual(data[20], {'key': 'Chr21', 'values': [{'x': 20, 'y': 0.0030709545722939127, 'label': '120AB-1'}, {'x': 20, 'y': 0.002786511221789091, 'label': '130VY-2'}, {'x': 20, 'y': 0.0030253740628958933, 'label': 'XY012345'}, {'x': 20, 'y': 0.0017650484276476074, 'label': 'MN20-1234-BM'}, {'x': 20, 'y': 0.0020330055650581297, 'label': 'LK19-4321-C-BM'}]})
        self.assertEqual(data[21], {'key': 'Chr22', 'values': [{'x': 21, 'y': 0.003020522239456228, 'label': '120AB-1'}, {'x': 21, 'y': 0.002798312054786424, 'label': '130VY-2'}, {'x': 21, 'y': 0.0027279481316605787, 'label': 'XY012345'}, {'x': 21, 'y': 0.0017826248446365825, 'label': 'MN20-1234-BM'}, {'x': 21, 'y': 0.001963873322668254, 'label': 'LK19-4321-C-BM'}]})
        self.assertEqual(data[22], {'key': 'ChrX', 'values': [{'x': 22, 'y': 0.010259717442951897, 'label': '120AB-1'}, {'x': 22, 'y': 0.009261964502977834, 'label': '130VY-2'}, {'x': 22, 'y': 0.010010268805249464, 'label': 'XY012345'}, {'x': 22, 'y': 0.005969623640560475, 'label': 'MN20-1234-BM'}, {'x': 22, 'y': 0.007157895952754525, 'label': 'LK19-4321-C-BM'}]})
        self.assertEqual(data[23], {'key': 'ChrY', 'values': [{'x': 23, 'y': 8.871430165836906e-06, 'label': '120AB-1'}, {'x': 23, 'y': 8.238945463582118e-06, 'label': '130VY-2'}, {'x': 23, 'y': 1.9249172583096402e-05, 'label': 'XY012345'}, {'x': 23, 'y': 6.491290365246517e-07, 'label': 'MN20-1234-BM'}, {'x': 23, 'y': 5.326186966356117e-07, 'label': 'LK19-4321-C-BM'}]})


    def test_chromosome_coverage(self):
        from dataprocessor.models import Flowcell, SamplesRunData

        samples = SamplesRunData.objects.filter(flowcell_id=Flowcell.objects.get(flowcell_barcode="ABCDEFGHI"))
        from .utils.plots import chromosome_coverage

        data = chromosome_coverage(samples)
        self.assertEqual(data[0] , {'key': '120AB-1', 'values': [{'x': 0, 'y': 0.999767156655, 'label': '1'}, {'x': 1, 'y': 0.996221044411, 'label': '2'}, {'x': 2, 'y': 1.00240419923, 'label': '3'}, {'x': 3, 'y': 0.998675017099, 'label': '4'}, {'x': 4, 'y': 1.00029748755, 'label': '5'}, {'x': 5, 'y': 0.996906814503, 'label': '6'}, {'x': 6, 'y': 1.00082776713, 'label': '7'}, {'x': 8, 'y': 0.998424292775, 'label': '8'}, {'x': 8, 'y': 0.999498912425, 'label': '9'}, {'x': 9, 'y': 0.994719943037, 'label': '10'}, {'x': 10, 'y': 1.00110849673, 'label': '11'}, {'x': 11, 'y': 0.999569333688, 'label': '12'}, {'x': 12, 'y': 0.995994623495, 'label': '13'}, {'x': 13, 'y': 0.998788650217, 'label': '14'}, {'x': 14, 'y': 0.994360417196, 'label': '15'}, {'x': 15, 'y': 1.00836543998, 'label': '16'}, {'x': 16, 'y': 0.997585308234, 'label': '17'}, {'x': 17, 'y': 0.996679189689, 'label': '18'}, {'x': 18, 'y': 1.01607827032, 'label': '19'}, {'x': 19, 'y': 1.00249046855, 'label': '20'}, {'x': 20, 'y': 0.998684864799, 'label': '21'}, {'x': 21, 'y': 0.999147192931, 'label': '22'}, {'x': 22, 'y': 0.978871276368, 'label': 'X'}]})
        self.assertEqual(data[1] , {'key': '130VY-2', 'values': [{'x': 0, 'y': 0.997651181433, 'label': '1'}, {'x': 1, 'y': 0.996182338212, 'label': '2'}, {'x': 2, 'y': 1.00127671888, 'label': '3'}, {'x': 3, 'y': 0.999628197481, 'label': '4'}, {'x': 4, 'y': 1.0003626279, 'label': '5'}, {'x': 5, 'y': 0.997223433584, 'label': '6'}, {'x': 6, 'y': 0.998559132761, 'label': '7'}, {'x': 8, 'y': 1.00135340871, 'label': '8'}, {'x': 8, 'y': 1.00190440161, 'label': '9'}, {'x': 9, 'y': 0.994465583264, 'label': '10'}, {'x': 10, 'y': 1.00105943377, 'label': '11'}, {'x': 11, 'y': 1.00058080961, 'label': '12'}, {'x': 12, 'y': 0.996579746622, 'label': '13'}, {'x': 13, 'y': 1.00025531579, 'label': '14'}, {'x': 14, 'y': 0.992899046942, 'label': '15'}, {'x': 15, 'y': 1.00916856964, 'label': '16'}, {'x': 16, 'y': 0.998225059697, 'label': '17'}, {'x': 17, 'y': 0.997833312888, 'label': '18'}, {'x': 18, 'y': 1.01844729688, 'label': '19'}, {'x': 19, 'y': 1.00364725902, 'label': '20'}, {'x': 20, 'y': 0.996826495268, 'label': '21'}, {'x': 21, 'y': 0.994852107712, 'label': '22'}, {'x': 22, 'y': 0.98010676849, 'label': 'X'}]})
        self.assertEqual(data[2] , {'key': 'XY012345', 'values': [{'x': 0, 'y': 1.00149329993, 'label': '1'}, {'x': 1, 'y': 1.00005899646, 'label': '2'}, {'x': 2, 'y': 1.00071032123, 'label': '3'}, {'x': 3, 'y': 1.00122760212, 'label': '4'}, {'x': 4, 'y': 0.999845101557, 'label': '5'}, {'x': 5, 'y': 0.999594247835, 'label': '6'}, {'x': 6, 'y': 1.00015460739, 'label': '7'}, {'x': 8, 'y': 1.00107714859, 'label': '8'}, {'x': 8, 'y': 1.0013689022, 'label': '9'}, {'x': 9, 'y': 0.999746775752, 'label': '10'}, {'x': 10, 'y': 0.999034698484, 'label': '11'}, {'x': 11, 'y': 1.0010478566, 'label': '12'}, {'x': 12, 'y': 0.998531878599, 'label': '13'}, {'x': 13, 'y': 0.998791392218, 'label': '14'}, {'x': 14, 'y': 0.998253202924, 'label': '15'}, {'x': 15, 'y': 1.00149627032, 'label': '16'}, {'x': 16, 'y': 0.999200819481, 'label': '17'}, {'x': 17, 'y': 0.997892598265, 'label': '18'}, {'x': 18, 'y': 1.00384951439, 'label': '19'}, {'x': 19, 'y': 1.00099151511, 'label': '20'}, {'x': 20, 'y': 0.998723684614, 'label': '21'}, {'x': 21, 'y': 0.997762268947, 'label': '22'}, {'x': 22, 'y': 0.95419763491, 'label': 'X'}]})
        self.assertEqual(data[3] , {'key': 'MN20-1234-BM', 'values': [{'x': 0, 'y': 0.997787570191, 'label': '1'}, {'x': 1, 'y': 0.993370110807, 'label': '2'}, {'x': 2, 'y': 1.00222816166, 'label': '3'}, {'x': 3, 'y': 1.00148714309, 'label': '4'}, {'x': 4, 'y': 1.00238904966, 'label': '5'}, {'x': 5, 'y': 0.994059786989, 'label': '6'}, {'x': 6, 'y': 1.00410951749, 'label': '7'}, {'x': 8, 'y': 0.999882726324, 'label': '8'}, {'x': 8, 'y': 0.996999756351, 'label': '9'}, {'x': 9, 'y': 0.99719996531, 'label': '10'}, {'x': 10, 'y': 0.999751505041, 'label': '11'}, {'x': 11, 'y': 1.00327138225, 'label': '12'}, {'x': 12, 'y': 0.997911936493, 'label': '13'}, {'x': 13, 'y': 0.995225512295, 'label': '14'}, {'x': 14, 'y': 0.994999526549, 'label': '15'}, {'x': 15, 'y': 1.01100101117, 'label': '16'}, {'x': 16, 'y': 1.00258251107, 'label': '17'}, {'x': 17, 'y': 0.999604849356, 'label': '18'}, {'x': 18, 'y': 1.02610547408, 'label': '19'}, {'x': 19, 'y': 0.965150624458, 'label': '20'}, {'x': 20, 'y': 0.992689922444, 'label': '21'}, {'x': 21, 'y': 1.00203732591, 'label': '22'}, {'x': 22, 'y': 0.996733350503, 'label': 'X'}]})
        self.assertEqual(data[4] , {'key': 'LK19-4321-C-BM', 'values': [{'x': 0, 'y': 0.998184128404, 'label': '1'}, {'x': 1, 'y': 0.99441250147, 'label': '2'}, {'x': 2, 'y': 1.00122891271, 'label': '3'}, {'x': 3, 'y': 1.00322562984, 'label': '4'}, {'x': 4, 'y': 1.00060542301, 'label': '5'}, {'x': 5, 'y': 0.995303956252, 'label': '6'}, {'x': 6, 'y': 1.0058501427, 'label': '7'}, {'x': 8, 'y': 1.00104966922, 'label': '8'}, {'x': 8, 'y': 1.00057124671, 'label': '9'}, {'x': 9, 'y': 0.994357680568, 'label': '10'}, {'x': 10, 'y': 0.997745131629, 'label': '11'}, {'x': 11, 'y': 1.00128531106, 'label': '12'}, {'x': 12, 'y': 1.00330609959, 'label': '13'}, {'x': 13, 'y': 0.995603709857, 'label': '14'}, {'x': 14, 'y': 0.990864677651, 'label': '15'}, {'x': 15, 'y': 1.00445280196, 'label': '16'}, {'x': 16, 'y': 0.998282886014, 'label': '17'}, {'x': 17, 'y': 0.998627237515, 'label': '18'}, {'x': 18, 'y': 1.03343426291, 'label': '19'}, {'x': 19, 'y': 0.999507949576, 'label': '20'}, {'x': 20, 'y': 0.99199797495, 'label': '21'}, {'x': 21, 'y': 1.00312572838, 'label': '22'}, {'x': 22, 'y': 1.00951354236, 'label': 'X'}]})

        data = chromosome_coverage(samples, False)
        self.assertEqual(data[0] , {'key': '120AB-1', 'values': [{'x': 0, 'y': 0.999767156655, 'label': '1'}, {'x': 1, 'y': 0.996221044411, 'label': '2'}, {'x': 2, 'y': 1.00240419923, 'label': '3'}, {'x': 3, 'y': 0.998675017099, 'label': '4'}, {'x': 4, 'y': 1.00029748755, 'label': '5'}, {'x': 5, 'y': 0.996906814503, 'label': '6'}, {'x': 6, 'y': 1.00082776713, 'label': '7'}, {'x': 8, 'y': 0.998424292775, 'label': '8'}, {'x': 8, 'y': 0.999498912425, 'label': '9'}, {'x': 9, 'y': 0.994719943037, 'label': '10'}, {'x': 10, 'y': 1.00110849673, 'label': '11'}, {'x': 11, 'y': 0.999569333688, 'label': '12'}, {'x': 12, 'y': 0.995994623495, 'label': '13'}, {'x': 13, 'y': 0.998788650217, 'label': '14'}, {'x': 14, 'y': 0.994360417196, 'label': '15'}, {'x': 15, 'y': 1.00836543998, 'label': '16'}, {'x': 16, 'y': 0.997585308234, 'label': '17'}, {'x': 17, 'y': 0.996679189689, 'label': '18'}, {'x': 18, 'y': 1.01607827032, 'label': '19'}, {'x': 19, 'y': 1.00249046855, 'label': '20'}, {'x': 20, 'y': 0.998684864799, 'label': '21'}, {'x': 21, 'y': 0.999147192931, 'label': '22'}, {'x': 22, 'y': 0.978871276368, 'label': 'X'}, {'x': 23, 'y': 6.99549576735e-08, 'label': 'Y'}]})
        self.assertEqual(data[1] , {'key': '130VY-2', 'values': [{'x': 0, 'y': 0.997651181433, 'label': '1'}, {'x': 1, 'y': 0.996182338212, 'label': '2'}, {'x': 2, 'y': 1.00127671888, 'label': '3'}, {'x': 3, 'y': 0.999628197481, 'label': '4'}, {'x': 4, 'y': 1.0003626279, 'label': '5'}, {'x': 5, 'y': 0.997223433584, 'label': '6'}, {'x': 6, 'y': 0.998559132761, 'label': '7'}, {'x': 8, 'y': 1.00135340871, 'label': '8'}, {'x': 8, 'y': 1.00190440161, 'label': '9'}, {'x': 9, 'y': 0.994465583264, 'label': '10'}, {'x': 10, 'y': 1.00105943377, 'label': '11'}, {'x': 11, 'y': 1.00058080961, 'label': '12'}, {'x': 12, 'y': 0.996579746622, 'label': '13'}, {'x': 13, 'y': 1.00025531579, 'label': '14'}, {'x': 14, 'y': 0.992899046942, 'label': '15'}, {'x': 15, 'y': 1.00916856964, 'label': '16'}, {'x': 16, 'y': 0.998225059697, 'label': '17'}, {'x': 17, 'y': 0.997833312888, 'label': '18'}, {'x': 18, 'y': 1.01844729688, 'label': '19'}, {'x': 19, 'y': 1.00364725902, 'label': '20'}, {'x': 20, 'y': 0.996826495268, 'label': '21'}, {'x': 21, 'y': 0.994852107712, 'label': '22'}, {'x': 22, 'y': 0.98010676849, 'label': 'X'}, {'x': 23, 'y': 7.14601524025e-08, 'label': 'Y'}]})
        self.assertEqual(data[2] , {'key': 'XY012345', 'values': [{'x': 0, 'y': 1.00149329993, 'label': '1'}, {'x': 1, 'y': 1.00005899646, 'label': '2'}, {'x': 2, 'y': 1.00071032123, 'label': '3'}, {'x': 3, 'y': 1.00122760212, 'label': '4'}, {'x': 4, 'y': 0.999845101557, 'label': '5'}, {'x': 5, 'y': 0.999594247835, 'label': '6'}, {'x': 6, 'y': 1.00015460739, 'label': '7'}, {'x': 8, 'y': 1.00107714859, 'label': '8'}, {'x': 8, 'y': 1.0013689022, 'label': '9'}, {'x': 9, 'y': 0.999746775752, 'label': '10'}, {'x': 10, 'y': 0.999034698484, 'label': '11'}, {'x': 11, 'y': 1.0010478566, 'label': '12'}, {'x': 12, 'y': 0.998531878599, 'label': '13'}, {'x': 13, 'y': 0.998791392218, 'label': '14'}, {'x': 14, 'y': 0.998253202924, 'label': '15'}, {'x': 15, 'y': 1.00149627032, 'label': '16'}, {'x': 16, 'y': 0.999200819481, 'label': '17'}, {'x': 17, 'y': 0.997892598265, 'label': '18'}, {'x': 18, 'y': 1.00384951439, 'label': '19'}, {'x': 19, 'y': 1.00099151511, 'label': '20'}, {'x': 20, 'y': 0.998723684614, 'label': '21'}, {'x': 21, 'y': 0.997762268947, 'label': '22'}, {'x': 22, 'y': 0.95419763491, 'label': 'X'}, {'x': 23, 'y': 1.55019633957e-07, 'label': 'Y'}]})
        self.assertEqual(data[3] , {'key': 'MN20-1234-BM', 'values': [{'x': 0, 'y': 0.997787570191, 'label': '1'}, {'x': 1, 'y': 0.993370110807, 'label': '2'}, {'x': 2, 'y': 1.00222816166, 'label': '3'}, {'x': 3, 'y': 1.00148714309, 'label': '4'}, {'x': 4, 'y': 1.00238904966, 'label': '5'}, {'x': 5, 'y': 0.994059786989, 'label': '6'}, {'x': 6, 'y': 1.00410951749, 'label': '7'}, {'x': 8, 'y': 0.999882726324, 'label': '8'}, {'x': 8, 'y': 0.996999756351, 'label': '9'}, {'x': 9, 'y': 0.99719996531, 'label': '10'}, {'x': 10, 'y': 0.999751505041, 'label': '11'}, {'x': 11, 'y': 1.00327138225, 'label': '12'}, {'x': 12, 'y': 0.997911936493, 'label': '13'}, {'x': 13, 'y': 0.995225512295, 'label': '14'}, {'x': 14, 'y': 0.994999526549, 'label': '15'}, {'x': 15, 'y': 1.01100101117, 'label': '16'}, {'x': 16, 'y': 1.00258251107, 'label': '17'}, {'x': 17, 'y': 0.999604849356, 'label': '18'}, {'x': 18, 'y': 1.02610547408, 'label': '19'}, {'x': 19, 'y': 0.965150624458, 'label': '20'}, {'x': 20, 'y': 0.992689922444, 'label': '21'}, {'x': 21, 'y': 1.00203732591, 'label': '22'}, {'x': 22, 'y': 0.996733350503, 'label': 'X'}, {'x': 23, 'y': 8.89324434289e-09, 'label': 'Y'}]})
        self.assertEqual(data[4] , {'key': 'LK19-4321-C-BM', 'values': [{'x': 0, 'y': 0.998184128404, 'label': '1'}, {'x': 1, 'y': 0.99441250147, 'label': '2'}, {'x': 2, 'y': 1.00122891271, 'label': '3'}, {'x': 3, 'y': 1.00322562984, 'label': '4'}, {'x': 4, 'y': 1.00060542301, 'label': '5'}, {'x': 5, 'y': 0.995303956252, 'label': '6'}, {'x': 6, 'y': 1.0058501427, 'label': '7'}, {'x': 8, 'y': 1.00104966922, 'label': '8'}, {'x': 8, 'y': 1.00057124671, 'label': '9'}, {'x': 9, 'y': 0.994357680568, 'label': '10'}, {'x': 10, 'y': 0.997745131629, 'label': '11'}, {'x': 11, 'y': 1.00128531106, 'label': '12'}, {'x': 12, 'y': 1.00330609959, 'label': '13'}, {'x': 13, 'y': 0.995603709857, 'label': '14'}, {'x': 14, 'y': 0.990864677651, 'label': '15'}, {'x': 15, 'y': 1.00445280196, 'label': '16'}, {'x': 16, 'y': 0.998282886014, 'label': '17'}, {'x': 17, 'y': 0.998627237515, 'label': '18'}, {'x': 18, 'y': 1.03343426291, 'label': '19'}, {'x': 19, 'y': 0.999507949576, 'label': '20'}, {'x': 20, 'y': 0.99199797495, 'label': '21'}, {'x': 21, 'y': 1.00312572838, 'label': '22'}, {'x': 22, 'y': 1.00951354236, 'label': 'X'}, {'x': 23, 'y': 6.27315147782e-09, 'label': 'Y'}]})


    def test_median_coverage(self):
        from dataprocessor.models import Flowcell, BatchRun

        samples = BatchRun.objects.filter(flowcell_id=Flowcell.objects.get(flowcell_barcode="ABCDEFGHI"))
        from .utils.plots import median_coverage

        data = median_coverage(samples)
        self.assertEqual(data[0]['key'], '13')
        self.assertEqual({k: data[0]['values'][0][k] for k in ['x', 'shape', 'size', 'color', 'label']}, {'x': 1596931200000.0, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'label': 'ABCDEFGHI'})
        self.assertTrue(abs(data[0]['values'][0]['y'] - 0.200009977208429) < 0.00000001)
        self.assertEqual(data[1]['key'], '18')
        self.assertEqual({k: data[1]['values'][0][k] for k in ['x', 'shape', 'size', 'color', 'label']}, {'x': 1596931200000.0,  'shape': 'circle', 'size': 1, 'color': '#c62828', 'label': 'ABCDEFGHI'})
        self.assertTrue(abs(data[1]['values'][0]['y'] - 0.249673836653633) < 0.00000001)
        self.assertEqual(data[2]['key'], '21')
        self.assertEqual({k: data[2]['values'][0][k] for k in ['x', 'shape', 'size', 'color', 'label']}, {'x': 1596931200000.0, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'label': 'ABCDEFGHI'})
        self.assertTrue(abs(data[2]['values'][0]['y'] - 0.250130152346746) < 0.00000001)
        self.assertEqual(data[3]['key'], 'x')
        self.assertEqual({k: data[3]['values'][0][k] for k in ['x', 'shape', 'size', 'color', 'label']}, {'x': 1596931200000.0, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'label': 'ABCDEFGHI'})
        self.assertTrue(abs(data[3]['values'][0]['y'] - 0.331740734144767) < 0.00000001)
        self.assertEqual(data[4]['key'], 'y')
        self.assertEqual({k: data[4]['values'][0][k] for k in ['x', 'shape', 'size', 'color', 'label']}, {'x': 1596931200000.0, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'label': 'ABCDEFGHI'})
        self.assertTrue(abs(data[4]['values'][0]['y'] - 7.97904055829e-09) < 0.00000001)


    def test_ncd(self):
        from dataprocessor.models import Flowcell, SamplesRunData

        samples = SamplesRunData.objects.filter(flowcell_id=Flowcell.objects.get(flowcell_barcode="ABCDEFGHI"))
        from .utils.plots import ncd_data

        data = ncd_data(samples)
        self.assertEqual(data[0]['max_y'], 26.1829)
        self.assertEqual(data[0]['min_y'], 13.15018)
        self.assertEqual(data[0]['key'], '13')
        self.assertEqual(data[0]['values'], [{'x': 1596931200000.0, 'y': 22.8842, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'flowcell': 'ABCDEFGHI', 'type': 'Test', 'sample': '120AB-1'}, {'x': 1596931200000.0, 'y': 23.67755, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'flowcell': 'ABCDEFGHI', 'type': 'Test', 'sample': '130VY-2'}, {'x': 1596931200000.0, 'y': 26.1829, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'flowcell': 'ABCDEFGHI', 'type': 'Control', 'sample': 'XY012345'}, {'x': 1596931200000.0, 'y': 13.15018, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'flowcell': 'ABCDEFGHI', 'type': 'Test', 'sample': 'MN20-1234-BM'}, {'x': 1596931200000.0, 'y': 16.75418, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'flowcell': 'ABCDEFGHI', 'type': 'Test', 'sample': 'LK19-4321-C-BM'}])
        self.assertEqual(data[1]['max_y'], 20.43631)
        self.assertEqual(data[1]['min_y'], -59.89946)
        self.assertEqual(data[1]['key'], '18')
        self.assertEqual(data[1]['values'], [{'x': 1596931200000.0, 'y': 17.66044, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'flowcell': 'ABCDEFGHI', 'type': 'Test', 'sample': '120AB-1'}, {'x': 1596931200000.0, 'y': 17.77966, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'flowcell': 'ABCDEFGHI', 'type': 'Test', 'sample': '130VY-2'}, {'x': 1596931200000.0, 'y': 20.43631, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'flowcell': 'ABCDEFGHI', 'type': 'Control', 'sample': 'XY012345'}, {'x': 1596931200000.0, 'y': -59.89946, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'flowcell': 'ABCDEFGHI', 'type': 'Test', 'sample': 'MN20-1234-BM'}, {'x': 1596931200000.0, 'y': 17.09129, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'flowcell': 'ABCDEFGHI', 'type': 'Test', 'sample': 'LK19-4321-C-BM'}])

        self.assertEqual(data[-1]['max_y'], 97.83376)
        self.assertEqual(data[-1]['min_y'], -90.1483)
        self.assertEqual(data[-1]['key'], 'y')
        self.assertEqual(data[-1]['values'], [{'x': 1596931200000.0, 'y': 89.98756, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'flowcell': 'ABCDEFGHI', 'type': 'Test', 'sample': '120AB-1'}, {'x': 1596931200000.0, 'y': 91.42685, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'flowcell': 'ABCDEFGHI', 'type': 'Test', 'sample': '130VY-2'}, {'x': 1596931200000.0, 'y': 97.83376, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'flowcell': 'ABCDEFGHI', 'type': 'Control', 'sample': 'XY012345'}, {'x': 1596931200000.0, 'y': -90.1483, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'flowcell': 'ABCDEFGHI', 'type': 'Test', 'sample': 'MN20-1234-BM'}, {'x': 1596931200000.0, 'y': 65.04944, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'flowcell': 'ABCDEFGHI', 'type': 'Test', 'sample': 'LK19-4321-C-BM'}])

        data = ncd_data(samples, "TESTAR" )
        self.assertEqual(data[0]['max_y'], 26.1829)
        self.assertEqual(data[0]['min_y'], 13.15018)
        self.assertEqual(data[0]['key'], 'TESTAR 13')
        self.assertEqual(data[0]['values'], [{'x': 1596931200000.0, 'y': 22.8842, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'flowcell': 'ABCDEFGHI', 'type': 'Test', 'sample': '120AB-1'}, {'x': 1596931200000.0, 'y': 23.67755, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'flowcell': 'ABCDEFGHI', 'type': 'Test', 'sample': '130VY-2'}, {'x': 1596931200000.0, 'y': 26.1829, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'flowcell': 'ABCDEFGHI', 'type': 'Control', 'sample': 'XY012345'}, {'x': 1596931200000.0, 'y': 13.15018, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'flowcell': 'ABCDEFGHI', 'type': 'Test', 'sample': 'MN20-1234-BM'}, {'x': 1596931200000.0, 'y': 16.75418, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'flowcell': 'ABCDEFGHI', 'type': 'Test', 'sample': 'LK19-4321-C-BM'}])

    def test_fetal_fraction(self):
        from dataprocessor.models import Flowcell, SamplesRunData

        samples = SamplesRunData.objects.filter(flowcell_id=Flowcell.objects.get(flowcell_barcode="ABCDEFGHI"))
        from .utils.plots import fetal_fraction

        data = fetal_fraction(samples)

        self.assertEqual(data[0]['min_x'], 1596931200000.0)
        self.assertEqual(data[0]['max_x'], 1596931200000.0)
        self.assertEqual(data[0]['min_y'], 0.01)
        self.assertEqual(data[0]['max_y'], 0.1)
        self.assertEqual(data[0]['key'], 'hist')
        self.assertEqual(data[0]['values'], [{'x': 1596931200000.0, 'y': 0.08, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '120AB-1'}, {'x': 1596931200000.0, 'y': 0.07, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': '130VY-2'}, {'x': 1596931200000.0, 'y': 0.1, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'type': 'Control', 'flowcell': 'ABCDEFGHI', 'sample': 'XY012345'}, {'x': 1596931200000.0, 'y': 0.01, 'shape': 'circle', 'size': 1, 'color': '#c62828', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': 'LK19-4321-C-BM'}])
        self.assertEqual(data[1]['min_x'], 1596931200000.0)
        self.assertEqual(data[1]['max_x'], 1596931200000.0)
        self.assertEqual(data[1]['min_y'], -0.01)
        self.assertEqual(data[1]['max_y'], -0.01)
        self.assertEqual(data[1]['key'], 'NA')
        self.assertEqual(data[1]['values'], [{'x': 1596931200000.0, 'y': -0.01, 'shape': 'circle', 'size': 1, 'color': '#f44336', 'type': 'Test', 'flowcell': 'ABCDEFGHI', 'sample': 'MN20-1234-BM'}])
