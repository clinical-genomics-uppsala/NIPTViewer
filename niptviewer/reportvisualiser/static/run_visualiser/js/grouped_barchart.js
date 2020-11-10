function horizontalGroupedBarChart({data,id}) {
    nv.addGraph(function() { 
      chart = nv.models.multiBarChart()
            //.barColor(d3.scale.category20().range())
            //.duration(300)
            .stacked(true)
            .x(function(d) { return d.label })
            .margin({bottom: 100, left: 70})
            .rotateLabels(45)
            .showControls(false);
            //.groupSpacing(0.1);

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
