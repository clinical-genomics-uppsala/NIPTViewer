function chromosomeLineChart({data,id, x_label, y_label}) {
    nv.addGraph(function() { 
      var chart = nv.models.lineChart().
        options({
                duration: 300,
                useInteractiveGuideline: true
            })
        ;
        //Configure how the tooltip looks.
        chart.tooltip.contentGenerator(function(key) {
            return "#";//"<table><tr><td>Flowcell:</td><td><b>" + key.point.flowcell + "</td></tr><tr><td>Type:</td><td><b>" + key.point.type + "</td></tr><tr><td>Sample:</td><td><b>" + key.point.sample + "</td></tr><tr><td>y:</td><td><b>" + key.point.y.toFixed(2) + "</b></td></tr><tr><td>x:</td><td><b>" + key.point.x.toFixed(2) + "</b></td></tr></table>";
        });


        var chromosome = ['Chr1', 'Chr2', 'Chr3', 'Chr4', 'Chr5', 'Chr6', 'Chr7', 'Chr8', 'Chr9', 'Chr10',
                          'Chr11', 'Chr12', 'Chr13', 'Chr14', 'Chr15', 'Chr16', 'Chr17', 'Chr18', 'Chr19', 'Chr20',
                          'Chr21', 'Chr22', 'ChrX']
        chart.forceX([0,23])
        chart.forceY([0.9,1.1])
        chart.xAxis.tickValues([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,23])
        chart.xAxis.tickFormat(function(d) { return chromosome[d]});
        chart.xAxis.axisLabel(x_label);
        chart.yAxis.tickFormat(d3.format('.03f'));;
        chart.yAxis.axisLabel(y_label);

        d3.select(id)
          .datum(data)
            .call(chart);

        nv.utils.windowResize(function() {chart.update();})
        return chart;
    })
};
