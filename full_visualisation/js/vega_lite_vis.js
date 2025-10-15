(function () {
  const embedOptions = { actions: false };

  vegaEmbed('#choropleth_map', 'js/malaysia_crime_map.vg.json', embedOptions)
    .then(() => {})
    .catch(console.error);

  vegaEmbed('#crime_stack', 'js/malaysia_crime_stacked.vg.json', embedOptions)
    .then(() => {})
    .catch(console.error);

  vegaEmbed('#crime_sunburst', 'js/malaysia_crime_sunburst.vg.json', embedOptions)
    .then(() => {})
    .catch(console.error);

  vegaEmbed('#crime_area', 'js/malaysia_crime_area.vg.json', embedOptions)
    .then(() => {})
    .catch(console.error);

  vegaEmbed('#crime_scattered', 'js/malaysia_crime_scattered.vg.json', embedOptions)
    .then(() => {})
    .catch(console.error);
})();
