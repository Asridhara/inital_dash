import re
import os
import json
from click import style

import numpy as np
import pandas as pd

from dash import Input, Output, html, dcc
from jupyter_dash import JupyterDash
import plotly.express as px
import plotly.graph_objects as go
from natsort import natsorted, index_natsorted , order_by_index
import dash
from dash import dcc, html, Output, Input, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash_bootstrap_components  as dbc
from dash import  Input, Output, html
#from dash import DiskcacheManager, CeleryManager,
# import time
import os
from uuid import uuid4
import flask
from dash import Dash,html
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import flask
from werkzeug.serving import run_simple

#cache = diskcache.Cache("./cache")
#background_callback_manager = DiskcacheManager(cache)

server = flask.Flask(__name__)

app = dash.Dash(__name__,server=server, use_pages=True,  external_stylesheets= [dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True )


SIDEBAR_STYLE = {

    "background-color": "#f8f9fa",
}


def create_nav_link(icon, label, href):
    return dcc.Link(
        dmc.Group(
            [
                dmc.ThemeIcon(
                    DashIconify(icon=icon, width=18),
                    size=30,
                    radius=30,
                    variant="light",
                ),
                html.H6(
                    children = label,
                    style ={"color": "#FFFFFF"}),
                #dmc.Text(label, size="sm", color="dark"),
            ]
        ),
        href=href,
        style={"textDecoration": "none"},
    )


sidebar = dmc.Navbar(
    fixed=True,
    width={"base": 300},
    position={"top": 70, "left": 0},
    height=1000,
 
    children=[
        dmc.ScrollArea(
            offsetScrollbars=True,
            type="scroll",
            children=[
                dmc.Space(h=20),
                dmc.Group(
                    direction="column",
                    children=[
                        create_nav_link(
                            icon="clarity:home-solid",
                            label="Home",
                            href="/home",
                        ),
                    ],
                ),
                dmc.Divider(
                    label="Fault Analysis", style={"marginBottom": 20, "marginTop": 20}
                ),
                dmc.Group(
                    direction="column",
                    children=[
                        create_nav_link(
                            icon=page["icon"], label=page["name"], href=page["path"]
                        )
                        for page in dash.page_registry.values()
                        if page["path"].startswith("/diagnostics")
                    ],
                ),
                dmc.Divider(
                    label="Function Behaviour", style={"marginBottom": 20, "marginTop": 20}
                ),
                dmc.Group(
                    direction="column",
                    children=[
                        create_nav_link(
                            icon=page["icon"],label=page["name"], href=page["path"]
                        )
                        for page in dash.page_registry.values()
                        if page["path"].startswith("/functions")
                    ],
                ),
            ],
        )
    ],style={"backgroundColor": "#36454F"}
)

app.layout = dmc.Container(
    [
        dmc.Header(
            height=70,
            fixed=True,
            children=[
                dmc.Center(
                      html.H1(
                        children='LVC Dashboard',
                        style={
                            'textAlign': 'center'
                        }
                            ),

                )], 
            style={"backgroundColor": "#81CA68"},
        ),
        sidebar,
        dmc.Container(
            dash.page_container,
            size="lg",
            mt = 20,
            pt=40,
            style={"marginLeft": 400, "marginTop": 80},
        ),
    ],
    fluid=True, 
)


@server.route('/')
def render_dashboard():
    return flask.redirect('/')

            # @server.route('/diagnostics/')
            # def render_dashboard():
            #     return flask.redirect('/diagnostics')

            # @server.route('/functions/')
            # def render_dashboard():
            #     return flask.redirect('/functions')

app = DispatcherMiddleware(server, {
    '/': app.server,
 
})

# 
