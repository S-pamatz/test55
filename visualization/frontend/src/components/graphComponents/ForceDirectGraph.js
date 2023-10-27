import React, { useRef, useEffect, useContext } from "react";
import * as d3 from "d3";
import "./ForceDirectGraph.css";
import GraphContext from "../data/GraphContext";

const ForceDirectGraph = () => {
  const graphRef = useRef(null);
  const ctx = useContext(GraphContext);

  const nodes = ctx.nodes;
  const links = ctx.links;

  useEffect(() => {
    console.log("Effect ran. Nodes and links updated.");
    console.log("Nodes:", nodes);
    // console.log("Links:", links);

    d3.select(graphRef.current).selectAll("*").remove();
    const svg = d3.select(graphRef.current);
    const g = svg.append("g"); // create a group to apply zoom transformations
    const defaultRadius = 40;
    const width = +svg.attr("width");
    const height = +svg.attr("height");
    const fontSize = 12/3;

    const simulation = d3
      .forceSimulation(nodes)
      .force(
        "link",
        d3
          .forceLink(links)
          .id((d) => d.id)
          .distance(100)
          .strength(3)
      )
      .force(
        "charge",
        d3.forceManyBody().strength(-100).distanceMin(50).distanceMax(200)
      )
      .force(
        "collide",
        d3.forceCollide().radius((d) => defaultRadius + 20)
      )
      .force("x", d3.forceX(width / 2).strength(0.1))
      .force("y", d3.forceY(height / 2).strength(0.1))
      .alphaDecay(0.4); // adjust alpha decay for faster stabilization
    // .velocityDecay(0.2); // adjust velocity decay for faster stabilization

    const link = g
      .selectAll(".link")
      .data(links)
      .enter()
      .append("line")
      .attr("class", "link")
      .attr("stroke", '#9D2235')
      .attr("stroke-width", 2);

    const nodeGroup = g
      .selectAll(".nodeGroup")
      .data(nodes)
      .enter()
      .append("g")
      .attr("class", "nodeGroup")
      .call(
        d3.drag().on("start", dragstart).on("drag", drag).on("end", dragend)
      );
      const defs = svg.append('defs');

      const gradient = defs.append('linearGradient')
        .attr('id', 'nodeGradient')
        .attr('x1', '0%')     // Gradient starts at the top
        .attr('y1', '20%')
        .attr('x2', '30%')     // Gradient ends at the bottom
        .attr('y2', '150%');
      
      gradient.append('stop')
        .attr('offset', '0%')
        .attr('stop-color', '#9D2235');
      
      gradient.append('stop')
        .attr('offset', '80%')
        .attr('stop-color', 'black');
      

    // Append a circle behind the image
    nodeGroup
      .append("circle")
      .attr("r", (d) => d.radius || defaultRadius) // needd to improve this to make it dynamic with state update )
      .attr("fill", (d) => (d.fill !== undefined ? d.fill : "url(#nodeGradient)"))
      // if node has fill color, use it here else no color
      .attr("opacity", 0.8);

    // Append the circle (or other shape) to the group
    nodeGroup
      .append("image")
      .attr("xlink:href", (d) => d.icon)
      .attr("width", defaultRadius)
      .attr("height", defaultRadius)
      .attr("x", -defaultRadius / 2) // center the image
      .attr("y", -defaultRadius / 2); // center the image

    // Append the text to the group
    nodeGroup
      .append("text")
      .attr("text-anchor", "middle")
      .attr("dy", defaultRadius / 2 + 10)
      .attr("dx", 0)
      .attr("font-size", fontSize + "px")
      .attr("data-full-text", (d) => d.Name)
      .attr("fill", "white")
      .text((d) => d.Name.slice(0, 5));

    nodeGroup.select("text").on("mouseover", function (event, d) {
      // Show full name
      d3.select(this).text(d3.select(this).attr("data-full-text"));
    });

    nodeGroup.select("text").on("mouseout", function (event, d) {
      d3.select(this).text(d.Name.slice(0, 5)); // Limit name length to fit circle
    });

    nodeGroup.select("circle").on("mouseover", function (event, d) {
      d3.select(this).attr("r", (d) => defaultRadius+10);
    });

    nodeGroup.select("circle").on("mouseout", function (event, d) {
      d3.select(this).attr("r", (d) => defaultRadius);
    });

    nodeGroup.select("circle").on("click", (event, d) => {
      // console.log("Node clicked: ", d);
      ctx.onNodeClick(d); // Call the callback provided from the parent
    });
    nodeGroup.select("image").on("click", (event, d) => {
      // console.log("Node clicked: ", d);
      ctx.onNodeClick(d); // Call the callback provided from the parent
    });

    simulation.on("tick", () => {
      link
        .attr("x1", (d) => {
          const deltaX = d.target.x - d.source.x;
          const deltaY = d.target.y - d.source.y;
          const dist = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
          const normX = deltaX / dist;
          const sourceX = d.source.x + defaultRadius * normX;
          return sourceX;
        })
        .attr("y1", (d) => {
          const deltaX = d.target.x - d.source.x;
          const deltaY = d.target.y - d.source.y;
          const dist = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
          const normY = deltaY / dist;
          const sourceY = d.source.y + defaultRadius * normY;
          return sourceY;
        })
        .attr("x2", (d) => {
          const deltaX = d.target.x - d.source.x;
          const deltaY = d.target.y - d.source.y;
          const dist = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
          const normX = deltaX / dist;
          const targetX = d.target.x - defaultRadius * normX;
          return targetX;
        })
        .attr("y2", (d) => {
          const deltaX = d.target.x - d.source.x;
          const deltaY = d.target.y - d.source.y;
          const dist = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
          const normY = deltaY / dist;
          const targetY = d.target.y - defaultRadius * normY;
          return targetY;
        });

      nodeGroup.attr("transform", (d) => `translate(${d.x}, ${d.y})`);
    });

    function dragstart(event, d) {
      if (d.fx != null || d.fy != null) return; // Prevent dragging for fixed nodes
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function drag(event, d) {
      if (d.fx != null || d.fy != null) return; // Prevent dragging for fixed nodes
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragend(event, d) {
      if (d.fx != null || d.fy != null) return; // Prevent dragging for fixed nodes
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    svg.call(
      d3.zoom().on("zoom", (event) => {
        const scaleFactor = 1 / event.transform.k;
        g.attr("transform", event.transform);

        // Adjust font size based on zoom level
        g.selectAll("text").attr("font-size", fontSize * scaleFactor + "px");
      })
    );
  }, [nodes, links]);

  return (
    <svg className="graph" ref={graphRef} width={1500} height={1000}></svg>
  );
};

export default ForceDirectGraph;
