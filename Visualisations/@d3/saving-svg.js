// https://observablehq.com/@mbostock/saving-svg@109
//import define1 from "../@d3/contours.js?v=3";

export default function define(runtime, observer) {
  const main = runtime.module();
  main.variable(observer()).define(["md"], function(md){return(
md`# Saving SVG

<figure style="display:flex;padding:10px;background:#fefedd;color:#444;font:15px/22px var(--sans-serif);">
<div style="margin:10px;"><b>Update:</b> Saving SVG is now built-in! Open the cell menu <svg viewBox="0 0 8 14" fill="currentColor" stroke="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="8" height="14"><circle r="1.5" cx="4" cy="2"></circle><circle r="1.5" cx="4" cy="7"></circle><circle r="1.5" cx="4" cy="12"></circle></svg> in the left margin to download any SVG cell as either SVG or PNG.</div>
<div><img src="https://user-images.githubusercontent.com/4732/57958244-0ed81780-78b4-11e9-859d-bc68cc4f45b6.png"></div>
</figure>

Say we have a dynamically-generated SVG, like this contour plot. Here’s how might you save it to a file in Observable using DOM.download.`
)});
  const child1 = runtime.module(define1);
  main.import("chart", child1);
  main.variable(observer()).define(["chart"], function(chart){return(
chart
)});
  main.variable(observer()).define(["md"], function(md){return(
md`You can serialize the SVG element as a string, and then download it as an SVG file.`
)});
  main.variable(observer()).define(["DOM","serialize","chart"], function(DOM,serialize,chart){return(
DOM.download(() => serialize(chart), undefined, "Save as SVG")
)});
  main.variable(observer("serialize")).define("serialize", ["NodeFilter"], function(NodeFilter)
{
  const xmlns = "http://www.w3.org/2000/xmlns/";
  const xlinkns = "http://www.w3.org/1999/xlink";
  const svgns = "http://www.w3.org/2000/svg";
  return function serialize(svg) {
    svg = svg.cloneNode(true);
    const fragment = window.location.href + "#";
    const walker = document.createTreeWalker(svg, NodeFilter.SHOW_ELEMENT, null, false);
    while (walker.nextNode()) {
      for (const attr of walker.currentNode.attributes) {
        if (attr.value.includes(fragment)) {
          attr.value = attr.value.replace(fragment, "#");
        }
      }
    }
    svg.setAttributeNS(xmlns, "xmlns", svgns);
    svg.setAttributeNS(xmlns, "xmlns:xlink", xlinkns);
    const serializer = new window.XMLSerializer;
    const string = serializer.serializeToString(svg);
    return new Blob([string], {type: "image/svg+xml"});
  };
}
);
  main.variable(observer()).define(["md"], function(md){return(
md`Alternatively, you can render the SVG to a canvas to generate a PNG.`
)});
  main.variable(observer()).define(["DOM","rasterize","chart"], function(DOM,rasterize,chart){return(
DOM.download(() => rasterize(chart), undefined, "Save as PNG")
)});
  main.variable(observer("rasterize")).define("rasterize", ["DOM","serialize"], function(DOM,serialize){return(
function rasterize(svg) {
  let resolve, reject;
  const promise = new Promise((y, n) => (resolve = y, reject = n));
  const image = new Image;
  image.onerror = reject;
  image.onload = () => {
    const rect = svg.getBoundingClientRect();
    const context = DOM.context2d(rect.width, rect.height);
    context.drawImage(image, 0, 0, rect.width, rect.height);
    context.canvas.toBlob(resolve);
  };
  image.src = URL.createObjectURL(serialize(svg));
  return promise;
}
)});
  main.variable(observer()).define(["md"], function(md){return(
md`To use this in your own notebook, import from this notebook:

\`\`\`js
import {rasterize} from "@mbostock/saving-svg"
\`\`\`

Happy downloading!`
)});
  return main;
}
