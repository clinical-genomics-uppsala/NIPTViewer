function scatterChart({data,id, x_label, y_label, x_format, y_format, limits=null, highlight_area=null, x_min=null, x_max=null, y_min=null, y_max=null, slope=null, intercept=null, std_err=null, x_ticks = null, y_ticks = null}) {
    var chart = nv.models.scatterChart()
                  .showLegend(true)
                  .showDistX(true)
                  .showDistY(true)
                  .useVoronoi(true)
                  .duration(300)
                  .pointRange([10, 50]);
                  //.color(["red"]);
   if(x_min !== null && x_max !== null){chart.xDomain([x_min,x_max])}
   if(y_min !== null && y_max !== null ){chart.yDomain([y_min,y_max])}


  chart.tooltip.contentGenerator(function(key) {
    return "<table><tr><td>Flowcell:</td><td><b>" + key.point.flowcell + "</td></tr><tr><td>Type:</td><td><b>" + key.point.type + "</td></tr><tr><td>Sample:</td><td><b>" + key.point.sample + "</td></tr><tr><td>y:</td><td><b>" + d3.format(y_format)(key.point.y) + "</b></td></tr><tr><td>x:</td><td><b>" + d3.format(x_format)(key.point.x) + "</b></td></tr></table>";
  });

  chart.xAxis.tickFormat(d3.format(x_format));
  chart.xAxis.axisLabel(x_label);
  chart.yAxis.tickFormat(d3.format(y_format));
  chart.yAxis.axisLabel(y_label);

  d3.select(id)
    .datum(data)
      //.attr('width', 400)
      //.attr('hieght', 400)
        .call(chart);
 if(std_err) {
     dev = 4.5
     var reg_std_h = d3.select(id).select('.nv-scatterWrap');
     reg_std_h
     .append('line')
       .attr({
           class: "high_error",
           x1: chart.xAxis.scale()((y_max-intercept-std_err*dev)/slope),
           y1: chart.yAxis.scale()(y_max),
           x2: chart.xAxis.scale()((y_min-intercept-std_err*dev)/slope),
           y2: chart.yAxis.scale()(y_min)
            })
            .style("stroke-dasharray","5,10")
            .style("stroke", "#C70039");
     var reg_std_l = d3.select(id).select('.nv-scatterWrap');
     reg_std_l
     .append('line')
       .attr({
          class: "low_error",
          x1: chart.xAxis.scale()(x_min),
          y1: chart.yAxis.scale()(x_min*slope+intercept-std_err*dev),
          x2: chart.xAxis.scale()((y_min-intercept+std_err*dev)/slope),
          y2: chart.yAxis.scale()(y_min)
           })
           .style("stroke-dasharray","5,10")
           .style("stroke", "#C70039");
 }

  if (limits !== null) {
    var custLine = d3.select(id).select('.nv-scatterWrap').datum(data).append('g');;
    custLine.selectAll('line')
      .data(limits)
        .enter()
          .append('line')
            .attr({
                     class: "limits",
                     x1: function(d){ return chart.xAxis.scale()(d[0][0])},
                     y1: function(d){ return chart.yAxis.scale()(d[1][0])},
                     x2: function(d){ return chart.xAxis.scale()(d[0][1])},
                     y2: function(d){ return chart.yAxis.scale()(d[1][1])}
                 })
                 .style("stroke", "#C70039");
  }
  var custRect = null
  if(highlight_area !== null) {
    custRect = d3.select(id).select('.nv-scatterWrap').datum(data).append('g');
    custRect.selectAll('rect').data(highlight_area).enter()
      .append('rect')
      .attr("x", function(d){ return chart.xAxis.scale()(d[0][0])})
          .attr("y", function(d){ return chart.yAxis.scale()(d[1][0])})
          .attr("width",  function(d){return chart.xAxis.scale()(d[0][1])-chart.xAxis.scale()(d[0][0])})
          .attr("height", function(d){return chart.yAxis.scale()(d[1][1])-chart.yAxis.scale()(d[1][0]);})
          .attr("fill", "red")
          .attr("class", "highlight_area")
          .attr("opacity", 0.1);
  }
  nv.utils.windowResize(function() {
     chart.update();
     custLine.selectAll('.limits').
        transition().attr({
                 x1: function(d){ return chart.xAxis.scale()(d[0][0])},
                 y1: function(d){ return chart.yAxis.scale()(d[1][0])},
                 x2: function(d){ return chart.xAxis.scale()(d[0][1])},
                 y2: function(d){ return chart.yAxis.scale()(d[1][1])}
             });
     if(std_err) {
         reg_std_h.
            selectAll('.high_error').
                transition().attr({
               x1: chart.xAxis.scale()((y_max-intercept-std_err*dev)/slope),
               y1: chart.yAxis.scale()(y_max),
               x2: chart.xAxis.scale()((y_min-intercept-std_err*dev)/slope),
               y2: chart.yAxis.scale()(y_min)
           });
         reg_std_l.
            selectAll('.low_error').
                transition().attr({
              x1: chart.xAxis.scale()(x_min),
              y1: chart.yAxis.scale()(x_min*slope+intercept-std_err*dev),
              x2: chart.xAxis.scale()((y_min-intercept+std_err*dev)/slope),
              y2: chart.yAxis.scale()(y_min)
         });
     }
     if (highlight_area !== null) {
         custRect.selectAll('.highlight_area').
             transition().attr({
                    x: function(d){ return chart.xAxis.scale()(d[0][0])},
                    y: function(d){ return chart.yAxis.scale()(d[1][0])},
                    width: function(d){return chart.xAxis.scale()(d[0][1])-chart.xAxis.scale()(d[0][0])},
                    height: function(d){return chart.yAxis.scale()(d[1][1])-chart.yAxis.scale()(d[1][0])}})
     }
  })
  return chart;
};

function scatterChartTime({data,id, x_label, y_label, x_format, y_format, x_min=null, x_max=null, y_min=null, y_max=null, x_ticks=null, y_ticks=null,limits=null}) {
  data.forEach(function (data, item) {
    if(data.min_y) {
      if (y_min == null) {
          y_min=data.min_y - Math.abs(data.min_y*0.1);
      } else {
        if(y_min > data.min_y) {
          y_min = data.min_y - Math.abs(data.min_y*0.1);
        }
      }
    }
    if(data.max_y) {
      if (y_max == null) {
        y_max=data.max_y + Math.abs(data.max_y)*0.1;
      } else {
        if(y_max < data.max_y) {
          y_max = data.max_y + Math.abs(data.max_y)*0.1;
        }
      }
    }
    if(data.min_x) {
      if (x_min == null) {
        x_min=data.min_x - 86400000*5;
      } else {
        if(x_min > data.min_x - 86400000*5) {
          x_min = data.min_x - 86400000*5;
        }
      }
    }
    if(data.max_x) {
      if (x_max == null) {
        x_max=data.max_x + 86400000*5;
      } else {
        if(x_max < data.max_x + 86400000*5) {
          x_max = data.max_x + 86400000*5;
        }
      }
    }
  });
  var chart = nv.models.scatterChart()
                  .showDistX(true)
                  .showDistY(true)
                  .useVoronoi(true)
                  .color(d3.scale.category10().range())
                  .duration(300)
                  .pointRange([10, 50]);

  if(x_min !== null && x_max !== null){chart.xDomain([x_min,x_max])}
  if(y_min !== null && y_max !== null ){chart.yDomain([y_min,y_max])}

  chart.tooltip.contentGenerator(function(key) {
    return "<table><tr><td>Flowcell:</td><td><b>" + key.point.flowcell + "</td></tr><tr><td>Type:</td><td><b>" + key.point.type + "</td></tr><tr><td>Sample:</td><td><b>" + key.point.sample + "</td></tr><tr><td>y:</td><td><b>" + d3.format(y_format)(key.point.y) + "</b></td></tr><tr><td>x:</td><td><b>" + d3.time.format('%y-%m-%d')(new Date(key.point.x)) + "</b></td></tr></table>";
  });

  chart.xAxis.tickFormat(function(d) { return d3.time.format('%y-%m-%d')(new Date(d));});
  chart.xAxis.axisLabel(x_label);
  chart.yAxis.tickFormat(d3.format(y_format));;
  chart.yAxis.axisLabel(y_label);


  d3.select(id)
    .datum(data)
        .call(chart);
    if (limits !== null) {
      var custLine = d3.select(id).select('.nv-scatterWrap').datum(data).append('g');
      custLine.selectAll('line')
        .data(limits)
          .enter()
            .append('line')
              .attr({
                       x1: function(d){ return chart.xAxis.scale()(x_min) },
                       y1: function(d){ return chart.yAxis.scale()(d[0]) },
                       x2: function(d){ return chart.xAxis.scale()(x_max)},
                       y2: function(d){ return chart.yAxis.scale()(d[1]) }
                   })
                   .style("stroke", "#C70039");
    }

  nv.utils.windowResize(function() {
      chart.update();
      if (limits !== null) {
      custLine.selectAll('line').
        transition().
            attr({
                 x1: function(d){ return chart.xAxis.scale()(x_min) },
                 y1: function(d){ return chart.yAxis.scale()(d[0]) },
                 x2: function(d){ return chart.xAxis.scale()(x_max)},
                 y2: function(d){ return chart.yAxis.scale()(d[1]) }
             });
         }
  })
  return chart;
};
