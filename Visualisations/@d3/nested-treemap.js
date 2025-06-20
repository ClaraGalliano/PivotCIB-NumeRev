// https://observablehq.com/@d3/nested-treemap@139
export default function define(runtime, observer) {
  const main = runtime.module();
  main.variable(observer()).define(["md"], function(md){return(
md`# Carte proportionnelle imbriquée

Révèle la représentation des domaines, sections et disciplines ("normalisées") dans le corpus d'étude.

Seuil score CIB par IPC-CAT : 1000`
)});
  main.variable(observer("chart")).define("chart", ["treemap","data","d3","width","height","DOM","format","color"], function(treemap,data,d3,width,height,DOM,format,color)
{
  const root = treemap(data);

  const svg = d3.create("svg")
      .attr("viewBox", [0, 0, width, height])
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
      .text(d => `${d.ancestors().reverse().map(d => d.data.name).join("/")}\n${format(d.value)}`);

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
    .data(d => d.data.name.split(/(?=[A-Z][^A-Z])/g).concat(format(d.value)))
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
);
  main.variable(observer("data")).define("data", ["d3"], function(d3){return(
d3.json("JSON/ValHierarchieDiscipline-1000.json")
)});
  main.variable(observer("treemap")).define("treemap", ["d3","width","height"], function(d3,width,height){return(
data => d3.treemap()
    .size([width, height])
    .paddingOuter(3)
    .paddingTop(19)
    .paddingInner(1)
    .round(true)
  (d3.hierarchy(data)
    .sum(d => d.value)
    .sort((a, b) => b.value - a.value))
)});
  main.variable(observer("width")).define("width", function(){return(
975
)});
  main.variable(observer("height")).define("height", function(){return(
1060
)});
  main.variable(observer("format")).define("format", ["d3"], function(d3){return(
d3.format(",d")
)});
  main.variable(observer("color")).define("color", ["d3"], function(d3){return(
d3.scaleSequential([8, 0], d3.interpolateMagma)
)});
  main.variable(observer("d3")).define("d3", ["require"], function(require){return(
require("d3@5")
)});
  return main;
}
