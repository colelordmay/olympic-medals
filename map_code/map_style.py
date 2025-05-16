from branca.element import MacroElement
from jinja2 import Template

class HatchPattern(MacroElement):
    """SVG hatching for countries with NaN fill"""
    def __init__(self):
        super().__init__()
        self._template = Template("""
        {% macro header(this, kwargs) %}
        <svg height="0" width="0" style="position:absolute">
          <defs>
            <pattern id="diagonalHatch" patternUnits="userSpaceOnUse" width="8" height="8">
              <rect width="8" height="8" fill="white"/>
              <path d="M0,0 l12,12" stroke="gray" stroke-width="0.6"/>
              <path d="M-6,6 l12,12" stroke="gray" stroke-width="0.6"/>
              <path d="M6,-6 l12,12" stroke="gray" stroke-width="0.6"/>
            </pattern>
          </defs>
        </svg>
        {% endmacro %}
        """)

class OceanBackground(MacroElement):
    """Customizable ocean background colour"""
    def __init__(self, colour="#ffffff"):
        super().__init__()
        self.colour = colour
        self._template = Template("""
        {% macro header(this, kwargs) %}
            <style>
                .leaflet-container {
                    background-color: {{ this.colour }};
                }
            </style>
        {% endmacro %}
        """)
