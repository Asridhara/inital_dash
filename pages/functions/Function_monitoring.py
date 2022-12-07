from dash import dcc, register_page, html
import dash_mantine_components as dmc
import  dash


register_page(__name__, icon = 'eos-icons:monitoring')

layout  =html.Div([

    html.H4(
        children='LVC function monitoring',
        style={
            'textAlign': 'center'
        }
    ),

    html.Br(),

])