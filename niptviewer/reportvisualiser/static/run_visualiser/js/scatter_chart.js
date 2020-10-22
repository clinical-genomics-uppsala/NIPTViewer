function scatterChart(data,id, x_label, y_label, x_format, y_format, limits=null, highlight_area=null, x_min=null, x_max=null, y_min=null, y_max=null, x_ticks = null, y_ticks = null) {
  if (y_min == null) {
    console.log(y_min, data[0].min_y)
    y_min=data[0].min_y - Math.abs(data[0].min_y*0.1);
  } else {
    if(data[0].min_y && y_min > data[0].min_y) {
      y_min = data[0].min_y - Math.abs(data[0].min_y*0.1);
    }
  }
  if (y_max == null) {
    y_max=data[0].max_y + Math.abs(data[0].max_y)*0.1;
  } else {
    if(data[0].max_y &&  y_max < data[0].max_y) {
      y_max = data[0].max_y + Math.abs(data[0].max_y)*0.1;
    }
  }
  if (x_min == null) {
    x_min=data[0].min_x - Math.abs(data[0].min_x*0.1);
  } else {

    if(data[0].min_x &&  x_min > data[0].min_x) {
      x_min = data[0].min_x - Math.abs(data[0].min_x*0.1);
    }
  }
  if (x_max == null) {
    x_max=data[0].max_x + Math.abs(data[0].max_x)*0.1;
  } else {
    if(data[0].max_x && x_max < data[0].max_x) {
      x_max = data[0].max_x + Math.abs(data[0].max_x)*0.1;
    }
  }
  console.log(x_min, y_max)
    var chart = nv.models.scatterChart()
                  .showLegend(false)
                  .showDistX(true)
                  .showDistY(true)
                  .useVoronoi(true)
                  .duration(300)
                   .pointRange([10, 50]);
   if(x_min && x_max){chart.xDomain([x_min,x_max])}
   if(y_min && y_max){chart.yDomain([y_min,y_max])}
                              //.xDomain([-40,10])
    //chart.pointSize(function(d) {return 1/d.size;})
    chart.color(function(d, i) {return d.values[0].color;});
        //Configure how the tooltip looks.
  chart.tooltip.contentGenerator(function(key) {
    return "<table><tr><td>Flowcell:</td><td><b>" + key.point.flowcell + "</td></tr><tr><td>Type:</td><td><b>" + key.point.type + "</td></tr><tr><td>Sample:</td><td><b>" + key.point.sample + "</td></tr><tr><td>y:</td><td><b>" + d3.format(y_format)(key.point.y) + "</b></td></tr><tr><td>x:</td><td><b>" + d3.format(x_format)(key.point.x) + "</b></td></tr></table>";
  });

        //Axis settings
  chart.xAxis.tickFormat(d3.format(x_format));

  //chart.xAxis.ticks(x_ticks);
  chart.xAxis.axisLabel(x_label);
  chart.yAxis.tickFormat(d3.format(y_format));
  //chart.yAxis.ticks(y_ticks);
  chart.yAxis.axisLabel(y_label);
        //We want to show shapes other than circles.

  d3.select(id)
    .datum(data)
      .attr('width', 600)
      .attr('hieght', 400)
        .call(chart);

  if (limits !== null) {
    var custLine = d3.select(id).select('.nv-scatterWrap').datum(data).append('g');
    custLine.selectAll('line')
      .data(limits)
        .enter()
          .append('line')
            .attr({
                     x1: function(d){ return chart.xAxis.scale()(d[0][0]) },
                     y1: function(d){ return chart.yAxis.scale()(d[1][0]) },
                     x2: function(d){ return chart.xAxis.scale()(d[0][1])},
                     y2: function(d){ return chart.yAxis.scale()(d[1][1]) }
                 })
                 .style("stroke", "#C70039");
  }
  var custRect = null
  if(highlight_area !== null) {
    custRect = d3.select(id).select('.nv-scatterWrap').datum(data).append('g');
    custRect.selectAll('rect').data(highlight_area).enter()
      .append('rect')
      .attr("x", function(d){ console.log(d);return chart.xAxis.scale()(d[0][0])})
          .attr("y", function(d){ return chart.yAxis.scale()(d[1][0])})
          .attr("width",  function(d){return chart.xAxis.scale()(d[0][1])-chart.xAxis.scale()(d[0][0])})
          .attr("height", function(d){return chart.yAxis.scale()(d[1][1])-chart.yAxis.scale()(d[1][0]);})
          .attr("fill", "red")
          .attr("opacity", 0.1);
}



 //ToDo update rectangle and line
  nv.utils.windowResize(function() {chart.update(); })
  return chart;
};

function scatterChartTime(data,id, x_label, y_label, x_format, y_format, x_min=null, x_max=null, y_min=null, y_max=null, x_ticks=null, y_ticks=null,limits=null) {
  console.log("Defined:", x_format,y_format,x_min, x_max, y_min, y_max, limits)
  if (y_min == null && data[0].min_y) {
      y_min=data[0].min_y - Math.abs(data[0].min_y*0.1);
  } else {
    if(data[0].min_y &&  y_min > data[0].min_y) {
      y_min = data[0].min_y - Math.abs(data[0].min_y*0.1);
    }
  }
  if (y_max == null && data[0].max_y) {
    y_max=data[0].max_y + Math.abs(data[0].max_y)*0.1;
  } else {
    if(data[0].max_y &&  y_max < data[0].max_y) {
      y_max = data[0].max_y + Math.abs(data[0].max_y)*0.1;
    }
  }
  if (x_min == null) {

    x_min=data[0].min_x - 86400000*5;
  } else {
    if(data[0].min_x && x_min > data[0].min_x) {
      x_min = data[0].min_x - 86400000*5;
    }
  }
  if (x_max == null) {
    x_max=data[0].max_x + 86400000*5;
  } else {
    if(data[0].max_x &&  x_max < data[0].max_x) {
      x_max = data[0].max_x + 86400000*5;
    }
  }
console.log("Defined:", x_format,y_format,x_min, x_max, y_min, y_max, limits)
  var chart = nv.models.scatterChart()
                  .showDistX(true)
                  .showDistY(true)
                  .useVoronoi(true)
                  .color(d3.scale.category10().range())
                  .duration(300);

    //if(x_min  !== null && x_max  !== null){chart.xDomain([x_min,x_max])}
    //if(y_min !== null && y_max !== null){chart.yDomain([y_min,y_max])}

                              //.yDomain([-200,800])

        //Configure how the tooltip looks.
  chart.tooltip.contentGenerator(function(key) {
    return "<table><tr><td>Flowcell:</td><td><b>" + key.point.flowcell + "</td></tr><tr><td>Type:</td><td><b>" + key.point.type + "</td></tr><tr><td>Sample:</td><td><b>" + key.point.sample + "</td></tr><tr><td>y:</td><td><b>" + d3.format(y_format)(key.point.y) + "</b></td></tr><tr><td>x:</td><td><b>" + d3.time.format('%y-%m-%d')(new Date(key.point.x)) + "</b></td></tr></table>";
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
      console.log("Limits: " + limits)
    if (limits !== null) {
      var custLine = d3.select(id).select('.nv-scatterWrap').datum(data).append('g');
      custLine.selectAll('line')
        .data(limits)
          .enter()
            .append('line')
              .attr({
                       x1: function(d){ return chart.xAxis.scale()(d[0][0]) },
                       y1: function(d){ return chart.yAxis.scale()(d[1][0]) },
                       x2: function(d){ return chart.xAxis.scale()(d[0][1])},
                       y2: function(d){ return chart.yAxis.scale()(d[1][1]) }
                   })
                   .style("stroke", "#C70039");
    }

  nv.utils.windowResize(function() {chart.update();})
  return chart;
};
