from IPython.display import display, clear_output
import ipywidgets as widgets

map_output = widgets.Output()

season_buttons = widgets.ToggleButtons(
    options=['both', 'summer','winter'],
    description='Select medals from:',
    button_style='',
    tooltips=['All medals', 'Summer medals only', 'Winter medals only'],
    value='both',
)

def render_layout(callback):
    season_buttons.observe(lambda change: callback(change['new']) if change['name'] == 'value' else None)
    display(season_buttons)
    display(map_output)