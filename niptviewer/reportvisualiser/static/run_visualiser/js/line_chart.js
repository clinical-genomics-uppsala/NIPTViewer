function lineChart({data,id, x_label, y_label}) {
    nv.addGraph(function() { 
      var chart = nv.models.lineChart().
        options({
                duration: 300,
                useInteractiveGuideline: true
            })
        ;

        chart.tooltip.contentGenerator(function(key) {
            return "#";//"<table><tr><td>Flowcell:</td><td><b>" + key.point.flowcell + "</td></tr><tr><td>Type:</td><td><b>" + key.point.type + "</td></tr><tr><td>Sample:</td><td><b>" + key.point.sample + "</td></tr><tr><td>y:</td><td><b>" + key.point.y.toFixed(2) + "</b></td></tr><tr><td>x:</td><td><b>" + key.point.x.toFixed(2) + "</b></td></tr></table>";
        });

        chart.xAxis.tickFormat(function(d) { return d3.time.format('%y-%m-%d')(new Date(d));});
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
