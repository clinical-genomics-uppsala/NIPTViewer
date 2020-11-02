from .data import extract_data, decimal_default

def data_structur_generator(samples_info):
    information = {}
    for comparison in samples_info.keys():
        data = []
        for type in samples_info[comparison]['data']:
            data.append({
                'min_x': min(samples_info[comparison]['data'][type],key=lambda v: v['x'])['x'],
                'max_x': max(samples_info[comparison]['data'][type],key=lambda v: v['x'])['x'],
                'min_y': min(samples_info[comparison]['data'][type],key=lambda v: v['y'])['y'],
                'max_y': max(samples_info[comparison]['data'][type],key=lambda v: v['y'])['y'],
                'key': type, 'values': samples_info[comparison]['data'][type]})
        information['data_' + comparison] = data
    return information

def chromosome_coverage(data, exclude_chry=True):
    if exclude_chry:
        return [{
            'key': sample.sample_id, 'values': [
            {'x': 0, 'y': decimal_default(sample.chr1_coverage), 'label': '1'},
            {'x': 1, 'y': decimal_default(sample.chr2_coverage), 'label': '2'},
            {'x': 2, 'y': decimal_default(sample.chr3_coverage), 'label': '3'},
            {'x': 3, 'y': decimal_default(sample.chr4_coverage), 'label': '4'},
            {'x': 4, 'y': decimal_default(sample.chr5_coverage), 'label': '5'},
            {'x': 5, 'y': decimal_default(sample.chr6_coverage), 'label': '6'},
            {'x': 6, 'y': decimal_default(sample.chr7_coverage), 'label': '7'},
            {'x': 8, 'y': decimal_default(sample.chr8_coverage), 'label': '8'},
            {'x': 8, 'y': decimal_default(sample.chr9_coverage), 'label': '9'},
            {'x': 9, 'y': decimal_default(sample.chr10_coverage), 'label': '10'},
            {'x': 10, 'y': decimal_default(sample.chr11_coverage), 'label': '11'},
            {'x': 11, 'y': decimal_default(sample.chr12_coverage), 'label': '12'},
            {'x': 12, 'y': decimal_default(sample.chr13_coverage), 'label': '13'},
            {'x': 13, 'y': decimal_default(sample.chr14_coverage), 'label': '14'},
            {'x': 14, 'y': decimal_default(sample.chr15_coverage), 'label': '15'},
            {'x': 15, 'y': decimal_default(sample.chr16_coverage), 'label': '16'},
            {'x': 16, 'y': decimal_default(sample.chr17_coverage), 'label': '17'},
            {'x': 17, 'y': decimal_default(sample.chr18_coverage), 'label': '18'},
            {'x': 18, 'y': decimal_default(sample.chr19_coverage), 'label': '19'},
            {'x': 19, 'y': decimal_default(sample.chr20_coverage), 'label': '20'},
            {'x': 20, 'y': decimal_default(sample.chr21_coverage), 'label': '21'},
            {'x': 21, 'y': decimal_default(sample.chr22_coverage), 'label': '22'},
            {'x': 22, 'y': decimal_default(sample.chrx_coverage), 'label': 'X'}]} for sample in data]
    else:
        return [{
            'key': sample.sample_id, 'values': [
            {'x': 0, 'y': decimal_default(sample.chr1_coverage), 'label': '1'},
            {'x': 1, 'y': decimal_default(sample.chr2_coverage), 'label': '2'},
            {'x': 2, 'y': decimal_default(sample.chr3_coverage), 'label': '3'},
            {'x': 3, 'y': decimal_default(sample.chr4_coverage), 'label': '4'},
            {'x': 4, 'y': decimal_default(sample.chr5_coverage), 'label': '5'},
            {'x': 5, 'y': decimal_default(sample.chr6_coverage), 'label': '6'},
            {'x': 6, 'y': decimal_default(sample.chr7_coverage), 'label': '7'},
            {'x': 8, 'y': decimal_default(sample.chr8_coverage), 'label': '8'},
            {'x': 8, 'y': decimal_default(sample.chr9_coverage), 'label': '9'},
            {'x': 9, 'y': decimal_default(sample.chr10_coverage), 'label': '10'},
            {'x': 10, 'y': decimal_default(sample.chr11_coverage), 'label': '11'},
            {'x': 11, 'y': decimal_default(sample.chr12_coverage), 'label': '12'},
            {'x': 12, 'y': decimal_default(sample.chr13_coverage), 'label': '13'},
            {'x': 13, 'y': decimal_default(sample.chr14_coverage), 'label': '14'},
            {'x': 14, 'y': decimal_default(sample.chr15_coverage), 'label': '15'},
            {'x': 15, 'y': decimal_default(sample.chr16_coverage), 'label': '16'},
            {'x': 16, 'y': decimal_default(sample.chr17_coverage), 'label': '17'},
            {'x': 17, 'y': decimal_default(sample.chr18_coverage), 'label': '18'},
            {'x': 18, 'y': decimal_default(sample.chr19_coverage), 'label': '19'},
            {'x': 19, 'y': decimal_default(sample.chr20_coverage), 'label': '20'},
            {'x': 20, 'y': decimal_default(sample.chr21_coverage), 'label': '21'},
            {'x': 21, 'y': decimal_default(sample.chr22_coverage), 'label': '22'},
            {'x': 22, 'y': decimal_default(sample.chrx_coverage), 'label': 'X'},
            {'x': 23, 'y': decimal_default(sample.chry_coverage), 'label': 'Y'}]} for sample in data]

def median_coverage(data):
    batch_data = {'13': {'data': {}, 'fields': ('flowcell_id', 'median_13')},
                  '18': {'data': {}, 'fields': ('flowcell_id', 'median_18')},
                  '21': {'data': {}, 'fields': ('flowcell_id', 'median_21')},
                  'x': {'data': {}, 'fields': ('flowcell_id', 'median_x')},
                  'y': {'data': {}, 'fields': ('flowcell_id', 'median_y')}}
    batch_data = extract_data(data=data, info=batch_data, label=lambda x: "median", x_format= lambda x: getattr(x, 'run_date').timestamp()*1000, extra_info=lambda x: {'label': x.flowcell_id.flowcell_barcode})
    return [{"key": k, 'values': d['data']['median']} for k,d in batch_data.items()]

def ncd_data(data):
    info_to_extract = {'13': {'data': {}, 'fields': ('flowcell_id', 'ncd_13')},
                  '18': {'data': {}, 'fields': ('flowcell_id', 'ncd_18')},
                  '21': {'data': {}, 'fields': ('flowcell_id', 'ncd_21')},
                  'x': {'data': {}, 'fields': ('flowcell_id', 'ncd_x')},
                  'y': {'data': {}, 'fields': ('flowcell_id', 'ncd_y')}}
    ncd_batch_data = extract_data(data=data, info=info_to_extract, label=lambda x: "ncd", x_format= lambda x: getattr(x, 'run_date').timestamp()*1000, extra_info=lambda x: {'label': x.flowcell_id.flowcell_barcode})
    return  [{"key": k, 'values': d['data']['ncd']} for k,d in ncd_batch_data.items()]

def fetal_fraction(data, label=lambda x: 'hist'):
    samples_info_ff_formated = {'ff_time': {'data': {}, 'fields': ('flowcell_id', 'ff_formatted')}}
    samples_info_ff_formated = extract_data(data=data, info=samples_info_ff_formated, label=label,x_format= lambda x: getattr(x, 'run_date').timestamp()*1000,replace_NA_with=-0.01)
    print(str(samples_info_ff_formated))
    return  data_structur_generator(samples_info_ff_formated)['data_ff_time']

def sample_data(data, colors="#bdbdbd", circle_size=1.0, label=lambda x: 'other'):
    samples_info = {'x_vs_y': {'data': {}, 'fields': ('ncv_X', 'ncv_Y')},
                    'x_vs_ff': {'data': {}, 'fields': ('ncv_X', 'ff_formatted')},
                   'y_vs_ff': {'data': {}, 'fields': ('ncv_Y', 'ff_formatted')},
                   'chr13_vs_ff': {'data': {}, 'fields': ('ncv_13', 'ff_formatted')},
                   'chr18_vs_ff': {'data': {}, 'fields': ('ncv_18', 'ff_formatted')},
                   'chr21_vs_ff': {'data': {}, 'fields': ('ncv_21', 'ff_formatted')}}
    if isinstance(colors, list):
        colors = ["#140c1c", "#442434", "#30346d", "#ffab40", "#854c30", "#346524", "#d04648", "#757161", "#597dce", "#d27d2c", "#8595a1", "#6daa2c", "#d2aa99", "#6dc2ca", "#dad45e", "#deeed6"]
        counter = 0
        shapes = ['diamond', 'square']
        color_dict = {}
        for sample in data:
            samples_info = extract_data([sample], samples_info, label=lambda x: x.sample_id, size=1.0, color=colors[counter])
            color_dict[sample.sample_id] = color=colors[counter]
            counter = counter + 1
    else:
        samples_info = extract_data(data=samples, info=samples_info, size=circle_size, label=label, color=colors)
