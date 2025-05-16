from branca.colormap import linear

# URL or path to the GeoJSON data
countries_json = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"

# Color scale for the map
colormap = linear.RdYlGn_09.scale(0.3, 0.7)