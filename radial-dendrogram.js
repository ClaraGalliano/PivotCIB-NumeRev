// URL: https://observablehq.com/@d3/radial-dendrogram
// Title: Radial Dendrogram
// Author: D3 (@d3)
// Version: 162
// Runtime version: 1

const m0 = {
  id: "bde1f995226f3be4@162",
  variables: [
    {
      inputs: ["md"],
      value: (function(md){return(
md`# Radial Dendrogram

D3’s [cluster layout](https://github.com/d3/d3-hierarchy/blob/master/README.md#cluster) produces node-link diagrams with leaf nodes at equal depth. These are less compact than [tidy trees](/@d3/radial-tidy-tree), but are useful for dendrograms, hierarchical clustering and [phylogenetic trees](/@mbostock/tree-of-life). See also the [radial variant](/@d3/cluster-dendrogram).`
)})
    },
    {
      name: "chart",
      inputs: ["tree","d3","data","DOM","width"],
      value: (function(tree,d3,data,DOM,width)
{
  const root = tree(d3.hierarchy(data)
      .sort((a, b) => (a.height - b.height) || a.data.name.localeCompare(b.data.name)));

  const svg = d3.select(DOM.svg(width, width))
      .style("width", "100%")
      .style("height", "auto")
      .style("padding", "10px")
      .style("box-sizing", "border-box")
      .style("font", "10px sans-serif");
  
  const g = svg.append("g");
    
  const link = g.append("g")
      .attr("fill", "none")
      .attr("stroke", "#555")
      .attr("stroke-opacity", 0.4)
      .attr("stroke-width", 1.5)
    .selectAll("path")
    .data(root.links())
    .enter().append("path")
      .attr("d", d3.linkRadial()
          .angle(d => d.x)
          .radius(d => d.y));
  
  const node = g.append("g")
      .attr("stroke-linejoin", "round")
      .attr("stroke-width", 3)
    .selectAll("g")
    .data(root.descendants().reverse())
    .enter().append("g")
      .attr("transform", d => `
        rotate(${d.x * 180 / Math.PI - 90})
        translate(${d.y},0)
      `);
  
  node.append("circle")
      .attr("fill", d => d.children ? "#555" : "#999")
      .attr("r", 2.5);
  
  node.append("text")
      .attr("dy", "0.31em")
      .attr("x", d => d.x < Math.PI === !d.children ? 6 : -6)
      .attr("text-anchor", d => d.x < Math.PI === !d.children ? "start" : "end")
      .attr("transform", d => d.x >= Math.PI ? "rotate(180)" : null)
      .text(d => d.data.name)
    .filter(d => d.children)
    .clone(true).lower()
      .attr("stroke", "white");
  
  document.body.appendChild(svg.node());

  const box = g.node().getBBox();

  svg.remove()
      .attr("width", box.width)
      .attr("height", box.height)
      .attr("viewBox", `${box.x} ${box.y} ${box.width} ${box.height}`);

  return svg.node();
}
)
    },
    {
      name: "data",
      inputs: ["require"],
      value: //(function(require){return(
d3.json("HierarchieDiscipline.json")
    },
    {
      name: "width",
      value: (function(){return(
932
)})
    },
    {
      name: "radius",
      inputs: ["width"],
      value: (function(width){return(
width / 2
)})
    },
    {
      name: "tree",
      inputs: ["d3","radius"],
      value: (function(d3,radius){return(
d3.cluster().size([2 * Math.PI, radius - 100])
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
  id: "bde1f995226f3be4@162",
  modules: [m0]
};

export default notebook;
