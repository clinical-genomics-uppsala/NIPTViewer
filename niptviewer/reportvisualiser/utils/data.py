from decimal import Decimal

import numpy
from scipy import stats

def sample_info():
    return {'x_vs_y': {'data': {}, 'fields': ('ncv_X', 'ncv_Y')},
            'x_vs_ff': {'data': {}, 'fields': ('ncv_X', 'ff_formatted')},
            'y_vs_ff': {'data': {}, 'fields': ('ncv_Y', 'ff_formatted')},
            'chr13_vs_ff': {'data': {}, 'fields': ('ncv_13', 'ff_formatted')},
            'chr18_vs_ff': {'data': {}, 'fields': ('ncv_18', 'ff_formatted')},
            'chr21_vs_ff': {'data': {}, 'fields': ('ncv_21', 'ff_formatted')}}


def decimal_default(obj):
    if isinstance(obj, Decimal) or isinstance(obj, int):
        return float(obj)
    elif isinstance(obj, float):
        return obj
    else:
        raise TypeError


def extract_qc_status(data):
    qc_failure = []
    qc_warning = []
    for sample in data:
        if sample.qc_flag != 0:
            if not sample.qc_failure == "nan":
                qc_failure.append((sample.sample_id, sample.qc_failure))
            if not sample.qc_warning == "nan":
                qc_warning.append((sample.sample_id, sample.qc_warning))
    return qc_failure, qc_warning


def extract_data(data, info, label=lambda x: x.sample_type.name, shape='circle', color="#c62828", size=1,
                 x_format=decimal_default, y_format=decimal_default,
                 extra_info=lambda x: {"type": x.sample_type.name,
                                       "flowcell": x.flowcell_id.flowcell_barcode,
                                       "sample": x.sample_id},
                 replace_NA_with=None, na_color="#f44336"):
    for item in data:
        for key in info:
            try:
                entry = {'x': x_format(getattr(item, info[key]['fields'][0])),
                         'y': y_format(getattr(item, info[key]['fields'][1])),
                         'shape': shape, 'size': size, 'color': color}
                entry.update(extra_info(item))
            except TypeError as err:
                if getattr(item, info[key]['fields'][0]) is None or getattr(item, info[key]['fields'][1]) is None:
                    if replace_NA_with is not None:
                        x = replace_NA_with if getattr(item, info[key]['fields'][0]) is None else x_format(
                            getattr(item, info[key]['fields'][0]))
                        y = replace_NA_with if getattr(item, info[key]['fields'][1]) is None else y_format(
                            getattr(item, info[key]['fields'][1]))
                        entry = {'x': x, 'y': y, 'shape': shape, 'size': size, 'color': na_color}
                        entry.update(extra_info(item))
                        if "NA" in info[key]['data']:
                            info[key]['data']["NA"].append(entry)
                        else:
                            info[key]['data']["NA"] = [entry]
                        continue
                    else:
                        continue
                else:
                    raise err

            if label(item) in info[key]['data']:
                info[key]['data'][label(item)].append(entry)
            else:
                info[key]['data'][label(item)] = [entry]
    return info


def extract_info_samples(data, info, label=lambda x: x.sample_id, size=1.0, shape="circle", color="#bdbdbd"):
    return extract_data(data, info, size=size, label=label, shape=shape, color=color)


def extra_info_per_sample(data, info, label=lambda x: x.sample_id, size=1.0, shape="circle", colors=["#bdbdbd"]):
    counter = 0
    color_length = len(colors)
    color_dict = {}
    for sample in data:
        extract_info_samples([sample], info, label=label, size=size, shape=shape, color=colors[counter % color_length])
        color_dict[sample.sample_id] = color = colors[counter % color_length]
        counter = counter + 1
    return (color_dict, info)


def generate_regression_line_from_sample_data(samples, x_value=lambda v: v['x'], y_value=lambda v: v['y'],
                                              filter=lambda v: v['y'] > 3.0):
    x_value_list = list()
    y_value_list = list()
    for sample in samples:
        if filter(sample):
            x_value_list.append(x_value(sample))
            y_value_list.append(y_value(sample))
    return stats.linregress(x_value_list,y_value_list)
