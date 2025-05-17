from IPython.display import display, clear_output
import ipywidgets as widgets

map_output = widgets.Output()

season_buttons = widgets.ToggleButtons(
    # options=[('Both', 'both'), ('Summer', 'summer'), ('Winter', 'winter')],
    options=['both', 'summer', 'winter'],
    description='Medals from:',
    button_style='',  # 'success', 'info', 'warning', 'danger' or ''
    tooltips=['All medals', 'Summer medals only', 'Winter medals only'],
    value='both',
)

def render_layout(callback):
    season_buttons.observe(lambda change: callback(change['new']) if change['name'] == 'value' else None)
    display(season_buttons)
    display(map_output)