// URL: https://observablehq.com/@d3/sankey-diagram
// Title: Sankey Diagram
// Author: D3 (@d3)
// Version: 229
// Runtime version: 1

const m0 = {
  id: "99b2e903e7df3b0a@229",
  variables: [
    {
      inputs: ["md"],
      value: (function(md){return(
md`# Sankey Diagram

This [Sankey diagram](https://github.com/d3/d3-sankey) visualizes the flow of energy: *supplies* are on the left, and *demands* are on the right. Links show how varying amounts of energy are converted or transmitted before being consumed or lost.

Data: [Department of Energy & Climate Change](http://www.decc.gov.uk/en/content/cms/tackling/2050/calculator_on/calculator_on.aspx), [Tom Counsell](https://tamc.github.io/Sankey/)
`
)})
    },
    {
      name: "viewof edgeColor",
      inputs: ["html","URLSearchParams"],
      value: (function(html,URLSearchParams){return(
Object.assign(html`<select>
  <option value=input>Color by input
  <option value=output>Color by output
  <option value=path selected>Color by input-output
  <option value=none>No color
</select>`, {
  value: new URLSearchParams(html`<a href>`.search).get("color") || "path"
})
)})
    },
    {
      name: "edgeColor",
      inputs: ["Generators","viewof edgeColor"],
      value: (G, _) => G.input(_)
    },
    {
      name: "viewof align",
      inputs: ["html","URLSearchParams"],
      value: (function(html,URLSearchParams){return(
Object.assign(html`<select>
  <option value=left>Left-aligned
  <option value=right>Right-aligned
  <option value=center>Centered
  <option value=justify selected>Justified
</select>`, {
  value: new URLSearchParams(html`<a href>`.search).get("align") || "justify"
})
)})
    },
    {
      name: "align",
      inputs: ["Generators","viewof align"],
      value: (G, _) => G.input(_)
    },
    {
      name: "chart",
      inputs: ["d3","DOM","width","height","sankey","data","color","format","edgeColor"],
      value: (function(d3,DOM,width,height,sankey,data,color,format,edgeColor)
{
  const svg = d3.select(DOM.svg(width, height))
      .style("width", "100%")
      .style("height", "auto");

  const {nodes, links} = sankey(data);

  svg.append("g")
      .attr("stroke", "#000")
    .selectAll("rect")
    .data(nodes)
    .join("rect")
      .attr("x", d => d.x0)
      .attr("y", d => d.y0)
      .attr("height", d => d.y1 - d.y0)
      .attr("width", d => d.x1 - d.x0)
      .attr("fill", d => color(d.name))
    .append("title")
      .text(d => `${d.name}\n${format(d.value)}`);

  const link = svg.append("g")
      .attr("fill", "none")
      .attr("stroke-opacity", 0.5)
    .selectAll("g")
    .data(links)
    .join("g")
      .style("mix-blend-mode", "multiply");

  if (edgeColor === "path") {
    const gradient = link.append("linearGradient")
        .attr("id", d => (d.uid = DOM.uid("link")).id)
        .attr("gradientUnits", "userSpaceOnUse")
        .attr("x1", d => d.source.x1)
        .attr("x2", d => d.target.x0);

    gradient.append("stop")
        .attr("offset", "0%")
        .attr("stop-color", d => color(d.source.name));

    gradient.append("stop")
        .attr("offset", "100%")
        .attr("stop-color", d => color(d.target.name));
  }

  link.append("path")
      .attr("d", d3.sankeyLinkHorizontal())
      .attr("stroke", d => edgeColor === "none" ? "#aaa"
          : edgeColor === "path" ? d.uid 
          : edgeColor === "input" ? color(d.source.name) 
          : color(d.target.name))
      .attr("stroke-width", d => Math.max(1, d.width));

  link.append("title")
      .text(d => `${d.source.name} → ${d.target.name}\n${format(d.value)}`);

  svg.append("g")
      .style("font", "10px sans-serif")
    .selectAll("text")
    .data(nodes)
    .join("text")
      .attr("x", d => d.x0 < width / 2 ? d.x1 + 6 : d.x0 - 6)
      .attr("y", d => (d.y1 + d.y0) / 2)
      .attr("dy", "0.35em")
      .attr("text-anchor", d => d.x0 < width / 2 ? "start" : "end")
      .text(d => d.name);

  return svg.node();
}
)
    },
    {
      name: "sankey",
      inputs: ["d3","align","width","height"],
      value: (function(d3,align,width,height)
{
  const sankey = d3.sankey()
      .nodeAlign(d3[`sankey${align[0].toUpperCase()}${align.slice(1)}`])
      .nodeWidth(15)
      .nodePadding(10)
      .extent([[1, 5], [width - 1, height - 5]]);
  return ({nodes, links}) => sankey({
    nodes: nodes.map(d => Object.assign({}, d)),
    links: links.map(d => Object.assign({}, d))
  });
}
)
    },
    {
      name: "format",
      inputs: ["d3"],
      value: (function(d3)
{
  const f = d3.format(",.0f");
  return d => `${f(d)} TWh`;
}
)
    },
    {
      name: "color",
      inputs: ["d3"],
      value: (function(d3)
{
  const color = d3.scaleOrdinal(d3.schemeCategory10);
  return name => color(name.replace(/ .*/, ""));
}
)
    },
    {
      name: "data",
      inputs: ["d3"],
      value: (function(d3){return(
d3.json("https://gist.githubusercontent.com/mbostock/ca9a0bb7ba204d12974bca90acc507c0/raw/398136b7db83d7d7fd89181b080924eb76041692/energy.json")
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
600
)})
    },
    {
      name: "d3",
      inputs: ["require"],
      value: (function(require){return(
require("d3@5", "d3-sankey@0.12")
)})
    }
  ]
};

const notebook = {
  id: "99b2e903e7df3b0a@229",
  modules: [m0]
};

export default notebook;