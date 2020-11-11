function horizontalGroupedBarChart({data,id}) {
    nv.addGraph(function() { 
      stacked = true;
      if(data[0]['values'].length == 1){stacked=false;}
      chart = nv.models.multiBarChart()
            .stacked(stacked)
            .x(function(d) { return d.label })
            .margin({bottom: 100, left: 70})
            .rotateLabels(45)
            .showControls(false);
      
        chart.reduceXTicks(false).staggerLabels(true);

        chart.xAxis
            .axisLabel("Sample")
            .axisLabelDistance(35)
            .showMaxMin(false)
            .tickFormat(function(d) { return d;});

        chart.yAxis
            .axisLabel("Reads")
            .axisLabelDistance(-5)
            .tickFormat(d3.format('.1%'));

        d3.select(id)
            .datum(data)
            .call(chart);

        nv.utils.windowResize(chart.update);

    return chart;
    });
};
