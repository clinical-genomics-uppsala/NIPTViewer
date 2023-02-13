import shutil

def copy_plot_scripts(*args, **kwargs):
    script_list = [
        'chromosome_line_chart.js',
        'grouped_barchart.js',
        'line_chart.js',
        'scatter_chart.js'
    ]
    for s in script_list:
        shutil.copy(f"niptviewer/reportvisualiser/static//run_visualiser/js/{s}", f'docs/static/{s}')