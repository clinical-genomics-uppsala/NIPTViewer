import os
import requests
import shutil

def copy_plot_scripts(*args, **kwargs):
    script_list = [
        'chromosome_line_chart.js',
        'grouped_barchart.js',
        'line_chart.js',
        'scatter_chart.js'
    ]
    if not os.path.exists("docs/static/"):
        os.makedirs("docs/static")

    for s in script_list:
        shutil.copy(f"niptviewer/reportvisualiser/static//run_visualiser/js/{s}", f'docs/static/{s}')

    urls = [
            'https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.2/d3.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.6/nv.d3.min.js.map',
            'https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.6/nv.d3.min.css',
            'https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.6/nv.d3.min.css.map',
            'https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.6/nv.d3.min.js',
    ]
    for u in urls:
        req = requests.get(u, allow_redirects=True)
        filename = u.split('/',)[-1]
        open(f"docs/static/{filename}", "wb").write(req.content)
