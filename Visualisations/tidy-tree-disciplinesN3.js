// URL: https://observablehq.com/@d3/tidy-tree
// Title: Tidy Tree
// Author: D3 (@d3)
// Version: 131
// Runtime version: 1

const m0 = {
  id: "5432439324f2c616@131",
  variables: [
    {
      inputs: ["md"],
      value: (function(md){return(
md`# Tidy Tree

D3’s [tree layout](https://github.com/d3/d3-hierarchy/blob/master/README.md#tree) implements the [Reingold–Tilford “tidy” algorithm](http://reingold.co/tidier-drawings.pdf) for constructing hierarchical node-link diagrams, improved to run in linear time by [Buchheim *et al.*](http://dirk.jivas.de/papers/buchheim02improving.pdf) Tidy trees are typically more compact than [cluster dendrograms](/@d3/cluster-dendrogram), which place all leaves at the same level. See also the [radial variant](/@d3/radial-tidy-tree).`
)})
    },
    {
      name: "chart",
      inputs: ["tree","data","d3","DOM","width"],
      value: (function(tree,data,d3,DOM,width)
{
  const root = tree(data);

  let x0 = Infinity;
  let x1 = -x0;
  root.each(d => {
    if (d.x > x1) x1 = d.x;
    if (d.x < x0) x0 = d.x;
  });

  const svg = d3.select(DOM.svg(width, x1 - x0 + root.dx * 2))
      .style("width", "100%")
      .style("height", "auto");
  
  const g = svg.append("g")
      .attr("font-family", "sans-serif")
      .attr("font-size", 10)
      .attr("transform", `translate(${root.dy / 3},${root.dx - x0})`);
    
  const link = g.append("g")
    .attr("fill", "none")
    .attr("stroke", "#555")
    .attr("stroke-opacity", 0.4)
    .attr("stroke-width",1.5)
  .selectAll("path")
    .data(root.links())
    .join("path")
      .attr("d", d3.linkHorizontal()
          .x(d => d.y)
          .y(d => d.x));
  
  const node = g.append("g")
      .attr("stroke-linejoin", "round")
      .attr("stroke-width", 0)
    .selectAll("g")
    .data(root.descendants())
    .join("g")
      .attr("transform", d => `translate(${d.y},${d.x})`);

  node.append("circle")
      .attr("fill", d => d.children ? "#555" : "#999")
      .attr("r", 2.5);

  node.append("text")
      .attr("dy", "0.31em")
      .attr("x", d => d.children ? -4 : 4)
      .attr("text-anchor", d => d.children ? "end" : "start")
      .text(d => d.data.name)
    .clone(true).lower()
      .attr("stroke", "white");
  
  return svg.node();
}
)
    },
    {
      name: "data",
      inputs: ["d3"],
      value: (function(d3){return(
d3.json("HierarchieDiscipline0-Titres.json")
)})
    },
    {
      name: "tree",
      inputs: ["d3","width"],
      value: (function(d3,width){return(
data => {
  const root = d3.hierarchy(data);
  root.dx = 8;
  root.dy = width / (root.height +5);
  return d3.tree().nodeSize([root.dx,root.dy])(root);
}
)})
    },
    {
      name: "width",
      value: (function(){return(
1400
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
  id: "5432439324f2c616@131",
  modules: [m0]
};

export default notebook;
