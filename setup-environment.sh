#!/bin/bash

mkdir -p niptviewer/assets/css/
wget --output-document niptviewer/assets/css/materialize.min.1.0.0.css https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css
wget --output-document niptviewer/assets/css/nv.d3.1.8.6.css https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.6/nv.d3.css

mkdir -p niptviewer/assets/js/nv/1.8.6
wget --output-document niptviewer/assets/js/nv/1.8.6/nv.d3.min.js https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.6/nv.d3.min.js
wget --output-document niptviewer/assets/js/nv/1.8.6/nv.d3.min.js.map https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.6/nv.d3.js.map
wget --output-document niptviewer/assets/js/d3.min.3.5.2.js https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.2/d3.min.js
wget --output-document niptviewer/assets/js/jquery-2.1.1.min.js https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.1/jquery.min.js
wget --output-document niptviewer/assets/js/jquery-2.1.1.min.js https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.1/jquery.min.js.map
wget --output-document niptviewer/assets/js/materialize.min.1.0.0.js https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js
