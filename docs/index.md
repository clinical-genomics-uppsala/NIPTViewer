# Welcome to NIPTViewer

NIPTViewer is a visualisation tool, mainly developed to plot data origination from Illumina VeriSeq NIPT Solution v1 tool. Makes it easy to compare runs against historical data. It introduce safe guard againts human errors by only allowing direct import of the output file from veriseq, removing the possibity of copy and paste errors that easly could be introduced when using for example excel or similar tool.

It's developed using [Django](https://www.djangoproject.com/), a web framework which enables rapid development. [NVD3](https://nvd3.org/) is used for generating plots.