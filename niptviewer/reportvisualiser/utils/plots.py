from decimal import Decimal

def decimal_default(obj):
    if isinstance(obj, Decimal) or isinstance(obj,int):
        return float(obj)
    elif isinstance(obj,float):
        return obj
    else:
        print(type(obj))
        raise TypeError


def extract_data(data, info, label=lambda x: x.sample_type.name,  shape='circle',color="#c62828", size=1, x_format=decimal_default, y_format=decimal_default, extra_info=lambda x: {"type": x.sample_type.name, "flowcell": x.flowcell_id.flowcell_barcode, "sample": x.sample_id}):
    for item in data:
        for key in info:
            entry = {'x': x_format(getattr(item, info[key]['fields'][0])),
                        'y': y_format(getattr(item, info[key]['fields'][1])),
                            'shape': shape, 'size': size, 'color': color}
            entry.update(extra_info(item))
            if label(item) in info[key]['data']:
                info[key]['data'][label(item)].append(entry)
            else:
                info[key]['data'][label(item)] = [entry]
    return info

def data_structur_generator(samples_info, context=None):
    if context is None:
        context = {}
    for comparison in samples_info.keys():
        data = []
        for type in samples_info[comparison]['data']:
            data.append({
                'min_x': min(samples_info[comparison]['data'][type],key=lambda v: v['x'])['x'],
                'max_x': max(samples_info[comparison]['data'][type],key=lambda v: v['x'])['x'],
                'min_y': min(samples_info[comparison]['data'][type],key=lambda v: v['y'])['y'],
                'max_y': max(samples_info[comparison]['data'][type],key=lambda v: v['y'])['y'],
                'key': type, 'values': samples_info[comparison]['data'][type]})
        context['data_' + comparison] = data
    return context
