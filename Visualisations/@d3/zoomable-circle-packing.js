// URL: https://observablehq.com/@d3/zoomable-circle-packing
// Title: Zoomable Circle Packing
// Author: D3 (@d3)
// Version: 156
// Runtime version: 1

const m0 = {
  id: "5831f55fccfa1c41@156",
  variables: [
    {
      inputs: ["md"],
      value: (function(md){return(
md`# Zoomable Circle Packing

Click to zoom in or out.`
)})
    },
    {
      name: "chart",
      inputs: ["pack","data","d3","DOM","width","height","color"],
      value: (function(pack,data,d3,DOM,width,height,color)
{
  const root = pack(data);
  let focus = root;
  let view;

  const svg = d3.select(DOM.svg(width, height))
      .attr("viewBox", `-${width / 2} -${height / 2} ${width} ${height}`)
      .style("display", "block")
      .style("margin", "0 -14px")
      .style("width", "calc(100% + 28px)")
      .style("height", "auto")
      .style("background", color(0))
      .style("cursor", "pointer")
      .on("click", () => zoom(root));

  const node = svg.append("g")
    .selectAll("circle")
    .data(root.descendants().slice(1))
    .join("circle")
      .attr("fill", d => d.children ? color(d.depth) : "white")
      .attr("pointer-events", d => !d.children ? "none" : null)
      .on("mouseover", function() { d3.select(this).attr("stroke", "#000"); })
      .on("mouseout", function() { d3.select(this).attr("stroke", null); })
      .on("click", d => focus !== d && (zoom(d), d3.event.stopPropagation()));

  const label = svg.append("g")
      .style("font", "10px sans-serif")
      .attr("pointer-events", "none")
      .attr("text-anchor", "middle")
    .selectAll("text")
    .data(root.descendants())
    .join("text")
      .style("fill-opacity", d => d.parent === root ? 1 : 0)
      .style("display", d => d.parent === root ? "inline" : "none")
      .text(d => d.data.name);

  zoomTo([root.x, root.y, root.r * 2]);

  function zoomTo(v) {
    const k = width / v[2];

    view = v;

    label.attr("transform", d => `translate(${(d.x - v[0]) * k},${(d.y - v[1]) * k})`);
    node.attr("transform", d => `translate(${(d.x - v[0]) * k},${(d.y - v[1]) * k})`);
    node.attr("r", d => d.r * k);
  }

  function zoom(d) {
    const focus0 = focus;

    focus = d;

    const transition = svg.transition()
        .duration(d3.event.altKey ? 7500 : 750)
        .tween("zoom", d => {
          const i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2]);
          return t => zoomTo(i(t));
        });

    label
      .filter(function(d) { return d.parent === focus || this.style.display === "inline"; })
      .transition(transition)
        .style("fill-opacity", d => d.parent === focus ? 1 : 0)
        .on("start", function(d) { if (d.parent === focus) this.style.display = "inline"; })
        .on("end", function(d) { if (d.parent !== focus) this.style.display = "none"; });
  }

  return svg.node();
}
)
    },
    {
      name: "data",
      inputs: ["d3"],
      value: (function(d3){return(
d3.json("./JSON/HierarchieDiscipline-1200.json")
)})
    },
    {
      name: "pack",
      inputs: ["d3","width","height"],
      value: (function(d3,width,height){return(
data => d3.pack()
    .size([width, height])
    .padding(3)
  (d3.hierarchy(data)
    .sum(d => d.size)
    .sort((a, b) => b.size - a.size))
)})
    },
    {
      name: "width",
      value: (function(){return(
932
)})
    },
    {
      name: "height",
      inputs: ["width"],
      value: (function(width){return(
width
)})
    },
    {
      name: "format",
      inputs: ["d3"],
      value: (function(d3){return(
d3.format(",d")
)})
    },
    {
      name: "color",
      inputs: ["d3"],
      value: (function(d3){return(
d3.scaleLinear()
    .domain([0, 5])
    .range(["hsl(152,80%,80%)", "hsl(228,30%,40%)"])
    .interpolate(d3.interpolateHcl)
)})
    },
    {
      name: "d3",
      inputs: ["require"],
      value: (function(require){return(
require("d3@5")
)})
    }
  ]
};

const notebook = {
  id: "5831f55fccfa1c41@156",
  modules: [m0]
};

export default notebook;
