import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { drillDown } from '../services/api';

const WaterfallChart = ({ data, customerId, campaignStatus }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    if (!data || !chartRef.current) return;

    const handleDrilldown = async (nodeId) => {
      try {
        const drilldownData = await drillDown(customerId, campaignStatus, nodeId);
        updateChart(drilldownData); // Update the chart with new data
      } catch (error) {
        console.error("Error during drilldown:", error);
      }
    };

    const margin = { top: 20, right: 30, bottom: 30, left: 40 },
          width = 960 - margin.left - margin.right,
          height = 500 - margin.top - margin.bottom;

    d3.select(chartRef.current).selectAll("*").remove();

    const svg = d3.select(chartRef.current)
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", `translate(<span class="math-inline">\{margin\.left\},</span>{margin.top})`);

    const updateChart = (currentData) => {
      d3.select(chartRef.current).selectAll("svg > g > *").remove();

      const x = d3.scaleBand().rangeRound([0, width]).padding(0.1);
      const y = d3.scaleLinear().rangeRound([height, 0]);

      x.domain(currentData.children.map(d => d.name));
      y.domain([0, d3.max(currentData.children, d => d.spend)]);

      svg.append("g")
          .attr("transform", `translate(0,${height})`)
          .call(d3.axisBottom(x));

      svg.append("g")
          .call(d3.axisLeft(y))
        .append("text")
          .attr("fill", "#000")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("dy", "0.71em")
          .attr("text-anchor", "end")
          .text("Spend");

          const bars = svg.selectAll(".bar")
          .data(currentData.children, d => d.id);

        bars.exit().remove();

        bars.enter()
          .append("rect")
          .attr("class", "bar")
          .merge(bars) // Merge enter and update selections
          .attr("x", d => x(d.name))
          .attr("width", x.bandwidth())
          .attr("y", d => y(d.spend))
          .attr("height", d => height - y(d.spend))
          .attr("fill", "steelblue")
          .on("click", (event, d) => {
            if (d.children !== undefined) { // Check if there are children to drill down into
              handleDrilldown(d.id);
            }
          });
    };

    updateChart(data); // Initial chart rendering

  }, [data]);

  return <div ref={chartRef}></div>;
};

export default WaterfallChart;