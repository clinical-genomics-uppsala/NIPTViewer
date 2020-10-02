function scatterChart(data,id, x_label, y_label,x_format, y_format) {
    nv.addGraph(function() { 
        var chart = nv.models.scatterChart()
                              .showDistX(true)
                              .showDistY(true)
                              .useVoronoi(true)
                              .color(d3.scale.category10().range())
                            //  .duration(300)
                              //.xDomain([-40,10])
                              //.yDomain([-200,800])

        //Configure how the tooltip looks.
        chart.tooltip.contentGenerator(function(key) {
          console.log();
            return "<table><tr><td>Flowcell:</td><td><b>" + key.point.flowcell + "</td></tr><tr><td>Type:</td><td><b>" + key.point.type + "</td></tr><tr><td>Sample:</td><td><b>" + key.point.sample + "</td></tr><tr><td>y:</td><td><b>" + key.point.y.toFixed(2) + "</b></td></tr><tr><td>x:</td><td><b>" + key.point.x.toFixed(2) + "</b></td></tr></table>";
        });

        //Axis settings
        chart.xAxis.tickFormat(d3.format(x_format));
        chart.xAxis.ticks(20);
        chart.xAxis.axisLabel(x_label);
        chart.yAxis.tickFormat(d3.format(y_format));;
        chart.yAxis.ticks(20);
        chart.yAxis.axisLabel(y_label);
        //We want to show shapes other than circles.
        //chart.scatter.onlyCircles(false);

        d3.select(id)
            .datum(data)
            .call(chart);

        // var custLine = d3.select(id)
      	//  .select('.nv-scatterWrap')
        //   .append('g');
        //
        // var xgrid_lower_upper = [[[-4,-4],[-200,800]], [[4,4],[-200,800]], [[-40,10],[0,0]]];
        // var xgrid_zero = [[0,[-200,800]]];
        // //var xgrid_skew = [[[-4,-33],[0,390]],[[4,-32],[0,500]]];
        // custLine.selectAll('line')
       	//   .data(xgrid_lower_upper)
        //   .enter()
        //   .append('line')
        //   .attr({
        //       x1: function(d){ return chart.xAxis.scale()(d[0][0]) },
        //       y1: function(d){ return chart.yAxis.scale()(d[1][0]) },
        //       x2: function(d){ return chart.xAxis.scale()(d[0][1])},
        //       y2: function(d){ return chart.yAxis.scale()(d[1][1]) }
        //   })
        //   .style("stroke", "#C70039");

          // var custLine2 = d3.select(id)
        	//  .select('.nv-scatterWrap')
          //   .append('g');
          //
          // custLine2.selectAll('line')
         	//   .data(xgrid_zero)
          //   .enter()
          //   .append('line')
          //   .attr({
          //       x1: function(d){ return chart.xAxis.scale()(d[0]) },
          //       y1: function(d){ return chart.yAxis.scale()(d[1][0]) },
          //       x2: function(d){ return chart.xAxis.scale()(d[0]) },
          //       y2: function(d){ return chart.yAxis.scale()(d[1][1]) }
          //   })
          //   .style("stroke", "#5DBDEA");
          //
          //   var custLine3 = d3.select(id)
          // 	 .select('.nv-scatterWrap')
          //     .append('g');
          //
          //   custLine3.selectAll('line')
          //  	  .data(xgrid_skew)
          //     .enter()
          //     .append('line')
          //     .attr({
          //         x1: function(d){ return chart.xAxis.scale()(d[0][0]) },
          //         y1: function(d){ return chart.yAxis.scale()(d[1][0]) },
          //         x2: function(d){ return chart.xAxis.scale()(d[0][1]) },
          //         y2: function(d){ return chart.yAxis.scale()(d[1][1]) }
          //     })
          //     .style("stroke", "#5DBDEA");

        nv.utils.windowResize(function() {
            chart.update();
            // custLine.selectAll('line')
           	//   .transition()
            //   .attr({
            //       x1: function(d){ return chart.xAxis.scale()(d[0][0]) },
            //       y1: function(d){ return chart.yAxis.scale()(d[1][0]) },
            //       x2: function(d){ return chart.xAxis.scale()(d[0][1])},
            //       y2: function(d){ return chart.yAxis.scale()(d[1][1]) }
            //   });
            //   custLine2.selectAll('line')
            //  	  .transition()
            //     .attr({
            //         x1: function(d){ return chart.xAxis.scale()(d[0]) },
            //         y1: function(d){ return chart.yAxis.scale()(d[1][0]) },
            //         x2: function(d){ return chart.xAxis.scale()(d[0]) },
            //         y2: function(d){ return chart.yAxis.scale()(d[1][1]) }
            //     });
            //     custLine3.selectAll('line')
            //    	  .transition()
            //       .attr({
            //           x1: function(d){ return chart.xAxis.scale()(d[0][0]) },
            //           y1: function(d){ return chart.yAxis.scale()(d[1][0]) },
            //           x2: function(d){ return chart.xAxis.scale()(d[0][1]) },
            //           y2: function(d){ return chart.yAxis.scale()(d[1][1]) }
            //       });
              })
          return chart;
    })
};
