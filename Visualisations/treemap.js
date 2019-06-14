// URL: https://observablehq.com/@d3/treemap
// Title: Treemap
// Author: D3 (@d3)
// Version: 106
// Runtime version: 1

const m0 = {
  id: "a1fd3857bac219b0@106",
  variables: [
    {
      inputs: ["md"],
      value: (function(md){return(
md`# Treemap

Introduced by [Ben Shneiderman](http://www.cs.umd.edu/hcil/treemap-history/), treemaps recursively partition space into rectangles according to each node’s associated value. D3 supports several treemap tiling methods. See also [nested](/@d3/nested-treemap) and [animated](/@d3/animated-treemap) treemaps.`
)})
    },
    {
      name: "viewof tile",
      inputs: ["html"],
      value: (function(html){return(
html`<select>
  <option>treemapBinary</option>
  <option>treemapDice</option>
  <option>treemapSlice</option>
  <option>treemapSliceDice</option>
  <option selected>treemapSquarify</option>
</select>`
)})
    },
    {
      name: "tile",
      inputs: ["Generators","viewof tile"],
      value: (G, _) => G.input(_)
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

  const leaf = svg.selectAll("g")
    .data(root.leaves())
    .join("g")
      .attr("transform", d => `translate(${d.x0},${d.y0})`);

  leaf.append("title")
      .text(d => `${d.ancestors().reverse().map(d => d.data.name).join("/")}\n${format(d.size)}`);

  leaf.append("rect")
      .attr("id", d => (d.leafUid = DOM.uid("leaf")).id)
      .attr("fill", d => { while (d.depth > 1) d = d.parent; return color(d.data.name); })
      .attr("fill-opacity", 0.6)
      .attr("width", d => d.x1 - d.x0)
      .attr("height", d => d.y1 - d.y0);

  leaf.append("clipPath")
      .attr("id", d => (d.clipUid = DOM.uid("clip")).id)
    .append("use")
      .attr("xlink:href", d => d.leafUid.href);

  leaf.append("text")
      .attr("clip-path", d => d.clipUid)
    .selectAll("tspan")
    .data(d => d.data.name.split(/(?=[A-Z][^A-Z])/g).concat(format(d.size)))
    .join("tspan")
      .attr("x", 3)
      .attr("y", (d, i, nodes) => `${(i === nodes.length - 1) * 0.3 + 1.1 + i * 0.9}em`)
      .attr("fill-opacity", (d, i, nodes) => i === nodes.length - 1 ? 0.7 : null)
      .text(d => d);

  return svg.node();
}
)
    },
    {
      name: "data",
      inputs: ["d3"],
      value: (function(d3){return(
d3.json("./HierarchieDiscipline800.json")
)})
    },
    {
      name: "treemap",
      inputs: ["d3","tile","width","height"],
      value: (function(d3,tile,width,height){return(
data => d3.treemap()
    .tile(d3[tile])
    .size([width, height])
    .padding(1)
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
d3.scaleOrdinal(d3.schemeCategory10)
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
  id: "a1fd3857bac219b0@106",
  modules: [m0]
};

export default notebook;
