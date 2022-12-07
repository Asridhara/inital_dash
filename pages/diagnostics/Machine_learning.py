from dash import dcc, register_page, html
import dash_mantine_components as dmc
import  dash


register_page(__name__, icon = 'ic:round-auto-graph', assets_ignore='.css')

layout =html.Div([

    html.H4(
        children='Fault tracing using machine learning',
        style={
            'textAlign': 'center'
        }
    ),

    html.Br(),

])