import folium
import numpy as np
from IPython.display import clear_output, display
from map_code.map_style import HatchPattern, OceanBackground
from map_code.process_update import update_medal_ratios
from map_code.config import colormap, countries_json
from map_code.layout import map_output

with open("colorbar.html") as f:
    colorbar_html = f.read()

# Map update function
def update_map_from_choice(season):
    medal_ratios_df = update_medal_ratios(season=season)
    ratio_dict = dict(zip(medal_ratios_df["Country"], medal_ratios_df["Ratio"]))
    count_dict = dict(zip(medal_ratios_df["Country"], medal_ratios_df["TotalMedals"]))

    def style_function(feature):
        iso_a3 = feature["properties"]["iso_a3"]
        ratio = ratio_dict.get(iso_a3)
        if isinstance(ratio, (float, int)) and not np.isnan(ratio):
            clipped_ratio = min(max(ratio, 0.3), 0.7)
            color = colormap(clipped_ratio)
        else:
            color = "url(#diagonalHatch)"
        return {
            "fillColor": color,
            "color": "black",
            "weight": 1.0,
            "fillOpacity": 0.72,
            "opacity": 0.3,
        }

    def tooltip_function(feature):
        iso_a3 = feature["properties"]["iso_a3"]
        country = feature["properties"]["name"]
        ratio = ratio_dict.get(iso_a3)
        total = count_dict.get(iso_a3)
        if isinstance(ratio, (float, int)) and not np.isnan(ratio):
            return f"{country}: {ratio * 100:.1f}% women ({int(total)} total medals)"
        else:
            return f"{country}: Fewer than 10 medals"

    tooltip = folium.GeoJsonTooltip(
        fields=["tooltip_text"],
        aliases=[""],
        labels=False,
        localize=True,
        sticky=True,
        toLocaleString=False,
        style=(
            "background-color: white; border: none; "
            "box-shadow: 2px 2px 6px rgba(0,0,0,0.3); padding: 4px;"
        ),
    )

    geojson = folium.GeoJson(
        countries_json,
        style_function=style_function,
        highlight_function=lambda feature: {
            "weight": 1.0,
            "fillOpacity": 1.0,
            "color": "black",
            "opacity": 1.0,
        },
        tooltip=tooltip,
    )

    for feature in geojson.data["features"]:
        feature["properties"]["tooltip_text"] = tooltip_function(feature)

    m = folium.Map(location=(30, 10), zoom_start=2, tiles=None)

    m.get_root().add_child(HatchPattern())
    m.get_root().html.add_child(folium.Element(colorbar_html))

    folium.raster_layers.TileLayer(
        tiles="",
        name="Background",
        attr="Dummy",
        overlay=True,
        control=False
    ).add_to(m)

    m.get_root().add_child(OceanBackground("#EEF6FF"))

    geojson.add_to(m)

    m.render()
    m.get_root().script = folium.Element(
        m.get_root().script.render().replace("topright", "bottomright")
    )

    with map_output:
        clear_output(wait=True)
        display(m)
