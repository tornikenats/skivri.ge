/*

	BY TORNIKE NATSVLISHVILI

 */

_charts = function() {
	this.color = d3.scale.category20()
    // this.color = d3.scale.ordinal()
    // .range(["#0cc402", "#fc0a18", "#aea7a5", "#ff15ae", "#d99f07", "#11a5fe", "#037e43", "#ba4455", "#d10aff", "#9354a6", "#7b6d2b", "#08bbbb", "#95b42d", "#b54e04", "#ee74ff", "#2d7593", "#e19772", "#fa7fbe", "#fe035b", "#aea0db", "#905e76", "#92b27a", "#03c262", "#878aff", "#4a7662", "#ff6757", "#fe8504", "#9340e1", "#2a8602", "#07b6e5", "#d21170", "#526ab3", "#ff08e2", "#bb2ea7", "#e4919f", "#09bf91", "#90624c", "#bba94a", "#a26c05", "#5c7605", "#df89e7", "#b0487c", "#ee9345", "#70b458", "#b19b71", "#6b6d74", "#ec5206", "#85a7c7", "#ff678c", "#b55b3e", "#8054cc", "#7eb0a0", "#c480b3", "#d9102d", "#5a783f", "#fe66d2", "#bc13c8", "#62bd33", "#b8ab03", "#8f31ff", "#fd8581", "#049279", "#74739c", "#0e6ad6", "#747151", "#01878d", "#0380bf", "#bf81fd", "#8ba1fb", "#887a02", "#c09bb5", "#a97741", "#d04096", "#c19083", "#a583da", "#8ca149", "#b16368", "#c23e37", "#fd7b40", "#d12153", "#b24cd2", "#56a66f", "#5dafbd", "#78aceb", "#2375fe", "#d49f54", "#ea41d3", "#885e92", "#8468fd", "#cf4eff", ]);
}

_charts.prototype = {
	selectedItems: {},
	createPieChart: function(id, dataset, valueGetter, lableGetter, selectedCallback){
		this.selectedItems[id] = []
		var labelHeight = 20
		var paddingBottom = 10
		var rect = d3.select('#chart').node(). getBoundingClientRect()
		var width = rect.width
		var height = rect.height
		var radius = Math.min(width, height - labelHeight - paddingBottom) / 2;
		var that = this;
		
		var svg = d3.select('#' + id)
					.append('svg')
					.attr('width', width)
					.attr('height', height)
					.append('g')
					.attr('transform', 'translate(' + (width / 2) +  ',' + ((height - labelHeight - paddingBottom) / 2) + ')');
		
		var pieOverlay = d3.select('#'+ id)
                    .select('svg')
                    .append('g')
                    .attr('transform', 'translate(' + (width / 2) +  ',' + ((height - labelHeight - paddingBottom) / 2) + ')');
					
		var arc = d3.svg
					.arc()
					.outerRadius(radius)
					
		var outerArc = d3.svg
					.arc()
					.outerRadius(radius)
					.innerRadius(radius - 10)
							
		var pie = d3.layout
					.pie()
					.value(function(d) {return valueGetter(d)} )
					.sort(null)
							
		var pathPie = svg.selectAll('path')
                    .data(pie(dataset))
                  .enter()
                    .append('path')
                    .classed('pie-section', true)
                    .attr('d', arc)
                    .attr('fill', function(d,i){
                        return Charts.color(i)
                    })
                    .on('click', function(d, i){
                        // set accent
                        prevSelected = Charts.selectedItems[that.id]
                        if(prevSelected !== undefined){
                            $('#pie-section-accent' + prevSelected.index ).hide()
                        }
                        $('#pie-section-accent' + i).show()

                        Charts.selectedItems[that.id] = {'index': i, 'data': d.data}

                        selectedCallback(d.data)
                    })
                    .on('mouseover', function(d, i){
                        color = d3.select(this).attr('fill')
                        if(color.indexOf('#') == -1){
                            rgba = color.split(/[,()]+/)
                            rgba = [rgba[1], rgba[2], rgba[3]]
                        }else{
                            rgb = d3.rgb(color)
                            rgba = [rgb.r, rgb.g, rgb.b]
                        }
                        d3.select(this).attr({
                            fill: 'rgba({0}, {1}, {2}, {3})'.format(rgba[0], rgba[1], rgba[2], 0.8)
                        })

                        // set label
                        d3.select('#PieChartLabel')
                            .text(lableGetter(d.data))
                    })
                    .on('mouseout', function(d, i){
                        // expect rgba
                        color = d3.select(this).attr('fill')
                        rgba = color.split(/[,()]+/)
                        d3.select(this).attr({
                            fill: 'rgba({0}, {1}, {2}, {3})'.format(rgba[1], rgba[2], rgba[3], 1)
                        })

                        // set label
                        if(Charts.selectedItems[that.id] !== undefined){
                            d3.select('#PieChartLabel')
                                .text(lableGetter(Charts.selectedItems[that.id].data))
                        }else{
                            d3.select('#PieChartLabel')
                                .text('')

                        }
                    })
								
		var pathPieOuter = pieOverlay.selectAll('path')
								.data(pie(dataset))
							.enter()
								.append('path')
								.classed('gone pie-section-accent', true)
								.attr('id', function(d, i){
									return 'pie-section-accent'+ i
								})
								.attr('d', outerArc)
								.attr('fill', 'red')
					  
		var labelText = svg.append('text')
							.attr({
								id: 'PieChartLabel',
								x: 0,
								y: radius + labelHeight,
								'text-anchor': 'middle'
							})
	},
	createLegend: function(id, dataset, value_getter){
		var legendRectSize = 18;
		var legendSpacing = 4;
		
		var legend = d3.selectAll('.legend')
						.data(dataset)
						.enter()
						.append('g')
						.attr('class', 'legend')
						.attr('transform', function(d, i) {
							var height = legendRectSize + legendSpacing;
							var offset =  height * dataset.length / 2;
							var horz = -2 * legendRectSize;
							var vert = i * height - offset;
							return 'translate(' + horz + ',' + vert + ')';
						});
						
		legend.append('rect')
			.attr('width', legendRectSize)
			.attr('height', legendRectSize)
			.style('fill', this.color)
			.style('stroke', this.color)
			
		legend.append('text')
			.attr('x', legendRectSize + legendSpacing)
			.attr('y', legendRectSize - legendSpacing)
			.text(function(d) { value_getter(d) })
	},
    createSpinner: function(id) {
		var rect = d3.select('#chart').node(). getBoundingClientRect()
		var width = rect.width
		var height = rect.height

        var radius = Math.min(width, height) / 2;
        var tau = 2 * Math.PI;

        var arc = d3.svg.arc()
                .innerRadius(radius*0.5)
                .outerRadius(radius*0.9)
                .startAngle(0);

        var svg = d3.select('#' + id).append("svg")
                .attr("width", width)
                .attr("height", height)
              .append("g")
                .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")

        var background = svg.append("path")
                .datum({endAngle: 0.33*tau})
                .style("fill", "#4D4D4D")
                .attr("d", arc)
                .call(spin, 1500)

        function spin(selection, duration) {
            selection.transition()
                .ease("linear")
                .duration(duration)
                .attrTween("transform", function() {
                    return d3.interpolateString("rotate(0)", "rotate(360)");
                });

            setTimeout(function() { spin(selection, duration); }, duration);
        }

        function transitionFunction(path) {
            path.transition()
                .duration(7500)
                .attrTween("stroke-dasharray", tweenDash)
                .each("end", function() { d3.select(this).call(transition); });
        }

    }
}

var Charts = new _charts();