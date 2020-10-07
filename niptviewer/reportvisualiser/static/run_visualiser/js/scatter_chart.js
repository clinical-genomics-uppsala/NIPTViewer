function scatterChart(data,id, x_label, y_label, x_format, y_format, x_ticks, y_ticks) {
  var chart = nv.models.scatterChart()
                  .showDistX(true)
                  .showDistY(true)
                  .useVoronoi(true)
                  .color(d3.scale.category10().range())
                  .duration(300);
                              //.xDomain([-40,10])
                              //.yDomain([-200,800])

        //Configure how the tooltip looks.
  chart.tooltip.contentGenerator(function(key) {
    return "<table><tr><td>Flowcell:</td><td><b>" + key.point.flowcell + "</td></tr><tr><td>Type:</td><td><b>" + key.point.type + "</td></tr><tr><td>Sample:</td><td><b>" + key.point.sample + "</td></tr><tr><td>y:</td><td><b>" + key.point.y.toFixed(2) + "</b></td></tr><tr><td>x:</td><td><b>" + key.point.x.toFixed(2) + "</b></td></tr></table>";
  });

        //Axis settings
  chart.xAxis.tickFormat(d3.format(x_format));
  //chart.xAxis.ticks(x_ticks);
  chart.xAxis.axisLabel(x_label);
  chart.yAxis.tickFormat(d3.format(y_format));;
  //chart.yAxis.ticks(y_ticks);
  chart.yAxis.axisLabel(y_label);
        //We want to show shapes other than circles.


  d3.select(id)
    .datum(data)
      //.attr('width', 600)
      //.attr('hieght', 400)
        .call(chart);


  nv.utils.windowResize(function() {chart.update();})
  return chart;
};

function scatterChartTime(data,id, x_label, y_label, x_format, y_format, x_ticks, y_ticks) {
  var chart = nv.models.scatterChart()
                  .showDistX(true)
                  .showDistY(true)
                  .useVoronoi(true)
                  .color(d3.scale.category10().range())
                  .duration(300);
                              //.xDomain([-40,10])
                              //.yDomain([-200,800])

        //Configure how the tooltip looks.
  chart.tooltip.contentGenerator(function(key) {
    return "<table><tr><td>Flowcell:</td><td><b>" + key.point.flowcell + "</td></tr><tr><td>Type:</td><td><b>" + key.point.type + "</td></tr><tr><td>Sample:</td><td><b>" + key.point.sample + "</td></tr><tr><td>y:</td><td><b>" + key.point.y.toFixed(2) + "</b></td></tr><tr><td>x:</td><td><b>" + key.point.x.toFixed(2) + "</b></td></tr></table>";
  });

        //Axis settings
  chart.xAxis.tickFormat(function(d) { return d3.time.format('%y-%m-%d')(new Date(d));});
  //chart.xAxis.ticks(x_ticks);
  chart.xAxis.axisLabel(x_label);
  chart.yAxis.tickFormat(d3.format(y_format));;
  //chart.yAxis.ticks(y_ticks);
  chart.yAxis.axisLabel(y_label);
        //We want to show shapes other than circles.


  d3.select(id)
    .datum(data)
        .call(chart);


  nv.utils.windowResize(function() {chart.update();})
  return chart;
};
