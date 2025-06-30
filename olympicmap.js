// *************** CONSTANTS ***************
const width = 800,
      height = 570;

const svg = d3.select("#data"),
      g = svg.append("g");

const tooltip = d3.select("#tooltip");

const slider = d3.select("#minMedalsSlider"),
      sliderLabel = d3.select("#sliderLabel");

const seasonSelect = d3.select("#seasonSelect");

const projection = d3.geoMercator()
                     .scale(130)
                     .center([0, 20])
                     .translate([width/2 - 8, height/2 + 30]);

const path = d3.geoPath().projection(projection);

const colorScale = d3.scaleDiverging()
                     .domain([0.3, 0.5, 0.7])
                     .interpolator(t => {
                       const colors = [
                         d3.rgb("#d62728"),
                         d3.rgb("#f7f7a5"),
                         d3.rgb("#2ca02c")
                       ];
                       return t < 0.5
                         ? d3.interpolateRgb(colors[0], colors[1])(t / 0.5)
                         : d3.interpolateRgb(colors[1], colors[2])((t - 0.5) / 0.5);
                     })
                     .clamp(true);

const dataURLs = {
  both: "https://raw.githubusercontent.com/colelordmay/olympic-medals/master/data/both_counts.csv",
  summer: "https://raw.githubusercontent.com/colelordmay/olympic-medals/master/data/summer_counts.csv",
  winter: "https://raw.githubusercontent.com/colelordmay/olympic-medals/master/data/winter_counts.csv",
};

let topo, data = new Map();

// *************** INITIALIZE ***************
d3.json("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson")
  .then(world => {
    topo = world;
    loadMedalDataAndDraw("both");
  });

svg.insert("rect", ":first-child")
   .attr("id", "oceanRect")
   .attr("width", width)
   .attr("height", height)
   .attr("fill", "#e6f0f6");

// *************** FUNCTIONS ***************
function loadMedalDataAndDraw(season) {
  d3.csv(dataURLs[season], d => ({
    country: d.country,
    ratio: +d.ratio,
    total: +d.total,
  })).then(rawData => {
    data = new Map(rawData.map(d => [d.country, { ratio: d.ratio, total: d.total }]));
    topo.features.forEach(f => {
      if (!data.has(f.id)) {
        data.set(f.id, { ratio: 0, total: 0 });
      }
    });
    updateMap(+slider.property("value"));
  });
}

function updateMap(minMedals) {
  sliderLabel.text(minMedals);

  g.selectAll("path")
    .data(topo.features)
    .join("path")
    .attr("d", path)
    .attr("fill", d => {
      const datum = data.get(d.id);
      return !datum || datum.total < minMedals
        ? "url(#hashPattern)"
        : colorScale(datum.ratio);
    })
    .attr("stroke", "#333333")
    .attr("vector-effect", "non-scaling-stroke")
    .style("stroke-width", "0.9px")
    .style("opacity", 1)
    .on("mouseover", (event, d) => {
      d3.selectAll("path")
        .interrupt()
        .transition()
        .duration(50)
        .style("opacity", 0.74);

      d3.select("#oceanRect")
        .transition()
        .duration(50)
        .style("opacity", 0.45);

      d3.select(event.currentTarget)
        .transition()
        .duration(50)
        .style("opacity", 1)
        .attr("stroke", "black");

      const datum = data.get(d.id);

      tooltip.style("opacity", 1)
             .html(`<strong>${d.properties.name}</strong><br>Medals won by women: ${
                     datum?.ratio != null
                       ? (datum.ratio * 100).toFixed(1) + "%"
                       : "0.0%"
                   }<br>Total medals: ${datum?.total ?? 0}`);
    })
    .on("mousemove", event => {
      tooltip.style("left", event.pageX + 10 + "px")
             .style("top", event.pageY + 10 + "px");
    })
    .on("mouseleave", () => {
      d3.selectAll("path")
        .interrupt()
        .transition()
        .style("opacity", 1)
        .attr("stroke", "#333333");

      d3.select("#oceanRect")
        .transition()
        .duration(50)
        .style("opacity", 1);

      tooltip.style("opacity", 0);
    });
}

// *************** INTERACTIVITY ***************
svg.call(d3.zoom()
          .scaleExtent([1, 10])
          .on("zoom", event => g.attr("transform", event.transform)))
   .call(d3.zoom().transform, d3.zoomIdentity.scale(1.1));

slider.on("input", () => updateMap(+slider.property("value")));

seasonSelect.on("change", () => loadMedalDataAndDraw(seasonSelect.property("value")));

// *************** COLORBAR ***************
const colorbarSvg = d3.select("#colorbar_svg");

const gradientWidth = 600,
      gradientHeight = 25,
      gradientX = 150,
      gradientY = 35,
      triangleWidth = 20;

const defs = colorbarSvg.append("defs");

const linearGradient = defs.append("linearGradient")
                           .attr("id", "colorbar-gradient")
                           .attr("x1", "0%")
                           .attr("y1", "0%")
                           .attr("x2", "100%")
                           .attr("y2", "0%");

const xScale = d3.scaleLinear()
                 .domain([0.3, 0.7])
                 .range([gradientX, gradientX + gradientWidth]);

const numStops = 10;

for (let i = 0; i <= numStops; i++) {
  const t = 0.3 + (0.4 * i) / numStops;
  const normT = (t - 0.3) / 0.4;
  linearGradient.append("stop")
                .attr("offset", `${normT * 100}%`)
                .attr("stop-color", colorScale(t));
}

colorbarSvg.append("rect")
           .attr("x", gradientX)
           .attr("y", gradientY)
           .attr("width", gradientWidth)
           .attr("height", gradientHeight)
           .style("fill", "url(#colorbar-gradient)");

colorbarSvg.append("polygon")
           .attr("points", `${gradientX},${gradientY} ${gradientX - triangleWidth},${gradientY + gradientHeight / 2} ${gradientX},${gradientY + gradientHeight}`)
           .attr("fill", colorScale(0.3));

colorbarSvg.append("polygon")
           .attr("points", `${gradientX + gradientWidth},${gradientY} ${gradientX + gradientWidth + triangleWidth},${gradientY + gradientHeight / 2} ${gradientX + gradientWidth},${gradientY + gradientHeight}`)
           .attr("fill", colorScale(0.7));

colorbarSvg.append("g")
           .attr("transform", `translate(0,${gradientY + gradientHeight})`)
           .call(d3.axisBottom(xScale)
                  .tickValues([0.3, 0.4, 0.5, 0.6, 0.7])
                  .tickFormat(d => `${Math.round(d * 100)}%`))
           .selectAll("text")
           .attr("font-size", "16px");

colorbarSvg.append("text")
           .attr("x", gradientX + gradientWidth / 2)
           .attr("y", gradientY - 15)
           .attr("text-anchor", "middle")
           .attr("font-weight", "700")
           .attr("font-size", "20px")
           .attr("fill", "#333333")
           .text("Percentage of Olympic medals won by women");