from branca.colormap import linear

# URL to GeoJSON data defining country outlines
countries_json = ("https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json")
colormap = linear.RdYlGn_09.scale(0.3, 0.7)