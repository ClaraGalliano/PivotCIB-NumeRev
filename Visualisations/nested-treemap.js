// URL: https://observablehq.com/@d3/nested-treemap
// Title: Nested Treemap
// Author: D3 (@d3)
// Version: 138
// Runtime version: 1

const m0 = {
  id: "5752d221584a7334@138",
  variables: [
    {
      inputs: ["md"],
      value: (function(md){return(
md`# Nested Treemap

This treemap variant applies padding to label internal nodes, better revealing the hierarchical structure. It is, however, less compact than a [standard treemap](/@d3/treemap). Compare to [cascaded treemaps](/@d3/cascaded-treemap) and [circle packing](/@d3/circle-packing).`
)})
    },
    {
      name: "chart",
      inputs: ["treemap","data","d3","DOM","width","height","format","color"],
      value: (function(treemap,data,d3,DOM,width,height,format,color)
{
  const root = treemap(data);

  const svg = d3.select(DOM.svg(width, height))
      .style("width", "100%")
      .style("height", "auto")
      .style("font", "10px sans-serif");

  const shadow = DOM.uid("shadow");

  svg.append("filter")
      .attr("id", shadow.id)
    .append("feDropShadow")
      .attr("flood-opacity", 0.3)
      .attr("dx", 0)
      .attr("stdDeviation", 3);

  const node = svg.selectAll("g")
    .data(d3.nest().key(d => d.height).entries(root.descendants()))
    .join("g")
      .attr("filter", shadow)
    .selectAll("g")
    .data(d => d.values)
    .join("g")
      .attr("transform", d => `translate(${d.x0},${d.y0})`);

  node.append("title")
      .text(d => `${d.ancestors().reverse().map(d => d.data.name).join("/")}\n${format(d.size)}`);

  node.append("rect")
      .attr("id", d => (d.nodeUid = DOM.uid("node")).id)
      .attr("fill", d => color(d.height))
      .attr("width", d => d.x1 - d.x0)
      .attr("height", d => d.y1 - d.y0);

  node.append("clipPath")
      .attr("id", d => (d.clipUid = DOM.uid("clip")).id)
    .append("use")
      .attr("xlink:href", d => d.nodeUid.href);

  node.append("text")
      .attr("clip-path", d => d.clipUid)
    .selectAll("tspan")
    .data(d => d.data.name.split(/(?=[A-Z][^A-Z])/g).concat(format(d.size)))
    .join("tspan")
      .attr("fill-opacity", (d, i, nodes) => i === nodes.length - 1 ? 0.7 : null)
      .text(d => d);

  node.filter(d => d.children).selectAll("tspan")
      .attr("dx", 3)
      .attr("y", 13);

  node.filter(d => !d.children).selectAll("tspan")
      .attr("x", 3)
      .attr("y", (d, i, nodes) => `${(i === nodes.length - 1) * 0.3 + 1.1 + i * 0.9}em`);

  return svg.node();
}
)
    },
    {
      name: "data",
      inputs: ["d3"],
      value: (function(d3){return(
d3.json("./DonneesHierarchieDiscipline.json")
)})
    },
    {
      name: "treemap",
      inputs: ["d3","width","height"],
      value: (function(d3,width,height){return(
data => d3.treemap()
    .size([width, height])
    .paddingOuter(3)
    .paddingTop(19)
    .paddingInner(1)
    .round(true)
  (d3.hierarchy(data)
    .sum(d => d.size)
    .sort((a, b) => b.size - a.size))
)})
    },
    {
      name: "width",
      value: (function(){return(
975
)})
    },
    {
      name: "height",
      value: (function(){return(
1060
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
d3.scaleSequential([8, 0], d3.interpolateMagma)
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
  id: "5752d221584a7334@138",
  modules: [m0]
};

export default notebook;
