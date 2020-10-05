from decimal import Decimal

def decimal_default(obj):
    if isinstance(obj, Decimal) or isinstance(obj,int):
        return float(obj)
    elif isinstance(obj,float):
        return obj
    else:
        print(type(obj))
        raise TypeError


def extract_data(prefix, data, info, only_prefix=False, shape='circle', size=1, x_format=decimal_default, y_format=decimal_default):
    label = lambda f: prefix + "_"  + item.sample_type.name
    if only_prefix:
        label = lambda f: prefix
    for item in data:
        for key in info:
            if label(item) in info[key]['data']:
                info[key]['data'][label(item)].append(
                    {'type': item.sample_type.name,
                        'flowcell': item.flowcell_id.flowcell_barcode,
                            'sample': item.sample_id,
                                'x': x_format(getattr(item, info[key]['fields'][0])),
                                    'y': y_format(getattr(item, info[key]['fields'][1])),
                                        'shape': shape, 'size': size})
            else:
                info[key]['data'][label(item)] = [{
                        'type': item.sample_type.name,
                            'flowcell': item.flowcell_id.flowcell_barcode,
                                'sample': item.sample_id,
                                    'x': x_format(getattr(item, info[key]['fields'][0])),
                                        'y': y_format(getattr(item, info[key]['fields'][1])),
                                            'shape': shape, 'size': size}]
    return info

def data_structur_generator(samples_info, context=None):
    if context is None:
        context = {}
    for comparison in samples_info.keys():
        data = []
        for type in samples_info[comparison]['data']:
            data.append({'key': type, 'values': samples_info[comparison]['data'][type]})
        context['data_' + comparison] = data
    return context
