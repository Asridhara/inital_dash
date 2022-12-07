import numpy as np
import pandas as pd

import dash
from jupyter_dash import JupyterDash
import plotly.express as px
import plotly.graph_objects as gopy 
import sys
import os
from natsort import natsorted, index_natsorted , order_by_index
from dash.exceptions import PreventUpdate
from dash import dcc, html, Input, Output,  callback, register_page, State
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from helper.dtc_helper import *
from helper.parallel_plots import *


def create_callback_for_plot(number,dtc_list,df, did_information):
    @callback(
        Output('select-did-1', 'options'),
        Input('select-snapshot-1','value'),
        Input('dtc-plot','selectedData')
    )
    def update_2040_did_dp_list(snapshot_value, selectedData):
        if snapshot_value is None or selectedData is None:
            raise PreventUpdate
        else:
            dtc_value = selectedData["points"][0]["customdata"][0]
            return [{'label': i, 'value': i} for i in list(dtc_list[dtc_value][snapshot_value].keys())]


    @callback(
        Output('select-signal-1', 'options'),
        Input('select-did-1','value'),
        Input('select-snapshot-1','value'),
        Input('dtc-plot','selectedData')
    )
    def update_2040_signal_dp_list(did_value, snapshot_value, selectedData):
        if snapshot_value is None or did_value is None:
            raise PreventUpdate
        else:
            dtc_value = selectedData["points"][0]["customdata"][0]
            return [{'label': i, 'value': i} for i in dtc_list[dtc_value][snapshot_value][did_value]]

            
    @callback(
        Output('snapshot-plot-1', 'figure'),
        [Input('select-snapshot-1', 'value'),
        Input('select-did-1',  'value'),
        Input('select-signal-1',  'value'),
        Input('dtc-plot', 'selectedData')]
    )
    def update_2040_snapshot_graph(snapshot_value, did_value, signal, selectData):
        try:
            if snapshot_value is None or signal is None:
                raise PreventUpdate
            else:
                dtc_value = selectData["points"][0]["customdata"][0]
            
                dtc_filtered_df = df[df.columns[df.columns.str.contains(dtc_value)==True]]
                dtc_filtered_df =  dtc_filtered_df.dropna(thresh = dtc_filtered_df.shape[0]*0.7,how='all',axis=0)
                dtc_filtered_df =  dtc_filtered_df.dropna(thresh = dtc_filtered_df.shape[0]*0.7,how='all',axis=1)
                plot_snapshot_df = dtc_filtered_df[dtc_filtered_df.columns[(dtc_filtered_df.columns.str.contains(rf'\d+/{dtc_value}/{snapshot_value}/{did_value}/{signal}'))]]
                trace_data = plot_snapshots_2040(plot_snapshot_df,did_information,did_value, signal)
                fig = go.Figure(trace_data) 
                return fig
                
        except IndexError:
            raise PreventUpdate

    @callback(
        Output('x-values-graph-1','data'),
        Output('y-values-graph-1','data'),
        Output('customdata-graph-1','data'),
        Input('snapshot-plot-1', 'selectedData'),  
    )
    def update_select_data(selectData):
        selected_x_values = []
        selected_y_values = []
        selected_index = []
        if selectData is None:
            raise PreventUpdate
        elif len(selectData["points"]) > 1:
            for i in range(len(selectData["points"])):
                selected_x_values.append(selectData["points"][i]["x"])
                selected_y_values.append(selectData["points"][i]["y"])
                selected_index.extend(selectData["points"][i]["customdata"])
        else:
            selected_x_values = selectData["points"][0]["x"]
            selected_y_values = selectData["points"][0]["y"]
            selected_index = selectData["points"][0]["customdata"]
        return selected_x_values,selected_y_values,selected_index


    @callback(
        Output('select-30-did-1', 'options'),
        Input('dtc-plot','selectedData')
    )
    def update_30_did_dp_list(selectData):
        if selectData is None:
            raise PreventUpdate
        else:
            dtc_value = selectData["points"][0]["customdata"][0]
            return [{'label': i, 'value': i} for i in list(dtc_list[dtc_value]['30'].keys())]

    @callback(
        Output('select-30-signal-1', 'options'),
        Input('select-30-did-1','value'),
        State('dtc-plot','selectedData')
    )
    def update_30_signal_dp_list(did_value, selectData):
        if selectData is None or did_value is None:
            raise PreventUpdate
        else:
            dtc_value = selectData["points"][0]["customdata"][0]
            return [{'label': i, 'value': i} for i in dtc_list[dtc_value]['30'][did_value]]


    @callback(
        Output('snapshot-30-plot-1','figure'),
        [Input('select-30-did-1', 'value'),
        Input('select-30-signal-1',  'value'),
        Input('dtc-plot', 'selectedData'),
        Input('customdata-graph-1','data'),]
    )
    def update_snapshot_graph( did_value, signal, dtc_hoverData, snapshot_hoverData):
        try:
            if signal is None or len(snapshot_hoverData) < 1:
                raise PreventUpdate
            else:
                dtc_value = dtc_hoverData["points"][0]["customdata"][0]
                #index_data = snapshot_hoverData
            
                dtc_filtered_df = df[df.columns[df.columns.str.contains(dtc_value)==True]]
                dtc_filtered_df =  dtc_filtered_df.dropna(thresh = dtc_filtered_df.shape[0]*0.7,how='all',axis=0)
                dtc_filtered_df =  dtc_filtered_df.dropna(thresh = dtc_filtered_df.shape[0]*0.7,how='all',axis=1)

                trace_data, carindex = plot_snapshots_30(dtc_filtered_df,did_information, dtc_value,did_value, signal,snapshot_hoverData)
                fig = go.Figure(trace_data)
                return fig
                
        except IndexError:
            raise PreventUpdate
