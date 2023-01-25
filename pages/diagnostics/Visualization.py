from turtle import width
from unittest.mock import call
import numpy as np
import pandas as pd
from uuid import uuid4
import dash
from dash.exceptions import PreventUpdate
from dash import dcc, html, Input, Output,  callback, register_page, State
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from dash import MATCH, ALL, ALLSMALLER,ctx

import plotly.express as px
import plotly.graph_objects as go
from natsort import natsorted, index_natsorted , order_by_index
import pathlib
from dash import dash_table
from helper.dtc_helper import *
from helper.parallel_plots import *
from helper.layout_setup.visualization_layout import *



register_page(__name__, icon = 'carbon:data-1',  external_stylesheets= [dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)




carmodel =  pd.read_excel(r'data\car_models.xlsx', header = 0 , na_filter = False, engine='openpyxl', convert_float= False)
dtc_description  = pd.read_excel(r'data\dtc_info.xlsx',sheet_name= 'DTC', header=1, na_filter = False )

df =  pd.read_csv(r'data\dtc_data.csv', sep = ';', low_memory=False)
part_numbers = df['diagnostic_part_number'].unique()

did_info =  pd.read_excel(r'data\32360447 AC.xlsx',sheet_name= 'DID', header = 1 , na_filter = False, engine='openpyxl')


dtc_list = dropdown_list_for_filtering(df)
did_information = get_did_information(did_info)

layout = html.Div([

    html.H4(
        children='DTC Data Visualization',
        style={
            'textAlign': 'center'
        }
    ),

    html.Br(),

    dmc.Space(h=10),

    html.Div(children = [
        html.Label('Choose a model'),
        dmc.Space(h=10),
        dmc.Chips(
            id="model-type",
            data=[ 
                {"value":i , "label":i} for i in carmodel[carmodel['Part Number'].isin(part_numbers)]['Model'].to_list()
            ],
            value= "521H PP2",
        ),
        
    ]),

    dcc.Store(id='Car_model',  storage_type = 'local'),

    html.Hr(),

    create_dtc_plot_with_summary(),
 
    html.Br(),

    dmc.Accordion(
        children =
        [
            dmc.AccordionItem(
                label = 'Selection', 
                children=[
                
                    dmc.Header(
                        height=60, 
                        children=[
                                    dbc.Row([
                                        dbc.Col([dmc.Text("Snapshot Analysis",style={"fontSize": 35})]),
                                        dbc.Col([dmc.Text("Filters")],  width={"size": 1, "offset":4}),
                                        dbc.Col([
                                            dcc.Dropdown(
                                            id ="filter-number",
                                            options = [
                                                {"value": 1, "label": "1"},
                                                {"value": 2, "label": "2"},
                                                {"value": 3, "label": "3"},
                                                {"value": 4, "label": "4"},
                                                ]
                                            ),
                                        ], width={"size": 1 })
                                    ]
                        )], style={"backgroundColor": "#FFFFFF"}
                    ),

                    create_snapshot_graph_layout(1),
                    

                    create_snapshot_graph_layout(2),
                    

                    create_snapshot_graph_layout(3),
                    

                    create_snapshot_graph_layout(4),

                    html.Br(), 
                    
                    html.Div(
                        [
                        dbc.Row([
                        #     dbc.Card(
                        #         dbc.CardBody([
                        #             html.H5('Filtered Cars'),
                        #             html.Pre(id='clickdata-data1')
                        #     ])
                        # ),
                        #     dbc.Card(
                        #         dbc.CardBody([
                        #             html.H5('Filtered Cars'),
                        #             html.Pre(id='clickdata-data2')
                        #     ])
                        # ),

                         
                        #     dbc.Card(
                        #         dbc.CardBody([
                        #             html.H5('Filtered Cars'),
                        #             html.Pre(id='clickdata-data3')
                        #     ])
                        # ),
                        
                            dbc.Card(
                                dbc.CardBody([
                                    html.H5('Filtered Cars'),
                                    html.Pre(id='filtered-vin')
                            ])
                        ),
                    ]),

                    html.Br(),   
                    dcc.Store(id = 'filterd_data'),

                    html.Div([
                        dmc.Button("Download Excel",  id="excel_download", fullWidth=True, variant="outline"),
                        dcc.Download(id="download-dataframe-xlsx"),
                        ]),

                    ]),
                ]
            ),

            dmc.AccordionItem(
                label = "Report",
                children=[ 
                 html.Div([
                    dmc.Container(
                        [
                        graph_layout_header(),

                        dmc.Space(),

                        html.H6("Selected Signals"),
            
                        dmc.Divider(size="lg"),

                        html.Div( id = "update-layout-with-filters", children =[]),

                        html.Br(),

                        filtered_cars_report_layout(),

                        ],style={"marginTop": 20,
                                "marginBottom": 20,
                                "marginLeft" : 40 ,
                                "marginRight" : 30  }),

                    ],style={"position": "centre",
                            "padding": 0,
                            "width": "210mm",
                            "height":"300mm",
                            "marginTop": 20,
                            "marginBottom": 20,
                            "border-radius": 5,
                            "background":"white",
                            "border": f"2px solid"}),
                    
            ]),

           dmc.AccordionItem(
                label = "Snapshot Visualization",
                children=[
                    dmc.RadioGroup(
                        id= 'tracks-list',
                        data=[],
                        orientation = 'horizontal',
                        value="20",
                        size="sm",
                    ),
                    html.Br(),
                    
                    html.Div(id = 'all-graphs-30', children =[]),
                ]),

        ]),
   
])


@callback(
    Output(component_id = 'dtc-plot', component_property= 'figure'), 
    Input(component_id = 'model-type', component_property= 'value')
)
def update_plot(selected_model):
    if selected_model is None:
        raise dash.exceptions.PreventUpdate
    else:
        part_number = carmodel[carmodel['Model'] == selected_model]['Part Number'].values[0]
        filter_df = df[df['diagnostic_part_number'].isin([part_number])]
    
        plot_dtc_count_df  = count_dtc_in_df(filter_df).sort_values(by='Count', ascending = False)
        fig = plot_count_histogram(plot_dtc_count_df)
         
        # dtc_data_path = pathlib.Path().resolve().joinpath("data").resolve()
        # folder_path =  os.path.join(part_number+'.xlsx')
        # did_info = pd.read_excel(dtc_data_path.joinpath(folder_path), sheet_name= 'DID', header = 1 , na_filter = False, engine='openpyxl') 

        # global did_information
        # did_information = get_did_information(did_info)
       

        return fig

@callback(
    Output(component_id = 'Car_model', component_property= 'data'), 
    Input(component_id = 'model-type', component_property= 'value'))
def store_model_year(selected_model):
    if selected_model is None:
        raise dash.exceptions.PreventUpdate
    else:
        return selected_model

@callback(
    Output(component_id ='selected-dtc', component_property = 'data'),
    Input(component_id ='dtc-plot', component_property = 'selectedData'))
def store_dtc_value(selectData):
    if selectData is None:
        raise PreventUpdate
    else:
        dtc_value = selectData["points"][0]["x"]
        return dtc_value


@callback(
    Output(component_id ='hover-data', component_property = 'children'),
    Input(component_id ='dtc-plot', component_property = 'selectedData'))
def display_software_label(selectData):
    if selectData is None:
        raise PreventUpdate
    else:
        dtc_value = selectData["points"][0]["x"]
        return dtc_description[dtc_description['Identifier'].isin([dtc_value])]['Software label'].values[0]



@callback(
    Output('click-data', 'children'),
    Input('dtc-plot', 'selectedData'))
def display_dtc_discription(selectData):
    if selectData is None:
        raise PreventUpdate
    else:
        dtc_value = selectData["points"][0]["x"]
        return dtc_description[dtc_description['Identifier'].isin([dtc_value])]['Description'].values[0]


@callback(
    Output('Count-data', 'children'),
    Input('dtc-plot', 'selectedData'))
def display_total_cars_number_in_dtc(selectData):
    if selectData is None:
        raise PreventUpdate
    else:
        count_value = selectData["points"][0]["customdata"][2]
        return count_value


@callback(
    Output('Percentage-data', 'children'),
    Input('dtc-plot', 'selectedData'))
def display_cars_percentage(selectedData):
    if selectedData is None:
        raise PreventUpdate
    else:
        percentage_value = selectedData["points"][0]["customdata"][1]
        return round(percentage_value, 3)

@callback(
    Output("snapshot-display-1", "style"),
    Output("snapshot-display-2", "style"),
    Output("snapshot-display-3", "style"),
    Output("snapshot-display-4", "style"),
    Input("filter-number", "value")
)
def select_value(value):
    if value == 1:
        return {'display':'block'},{'display':'none'},{'display':'none'},{'display':'none'}
    elif value ==2:
        return {'display':'block'},{'display':'block'},{'display':'none'},{'display':'none'}
    elif value == 3:
        return {'display':'block'},{'display':'block'},{'display':'block'},{'display':'none'}
    else:
        return {'display':'block'},{'display':'block'},{'display':'block'},{'display':'block'}

@callback(
    Output("update-layout-with-filters", "children"),
    Input("filter-number", "value"),
    Input("update-layout-with-filters", "children")
)
def display_report(selected_value, update_children):
    if selected_value == 1:
        update_children = graph_layout_one_filter()
    elif selected_value == 2:
        update_children = graph_layout_two_filter()
    elif selected_value == 3:
       update_children= graph_layout_three_filter()
    else:
        update_children  = graph_layout_four_filter()
    return update_children

    
@callback(
    Output('select-did-1', 'data'),
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
    Output('select-signal-1', 'data'),
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
    Output('snapshot-value-report-1',  'children'),
    Output('did-value-report-1', 'children'),
    Output('signal-value-report-1','children'),
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
            fig = fig.update_layout( 
                            height = 240, 
                        )
            return fig, snapshot_value, did_value, signal
            
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
        selected_x_values = [selectData["points"][0]["x"]]
        selected_y_values = [selectData["points"][0]["y"]]
        selected_index = [selectData["points"][0]["customdata"]]
    return selected_x_values,selected_y_values,selected_index


@callback(
    Output('select-30-did-1', 'data'),
    Input('dtc-plot','selectedData')
)
def update_30_did_dp_list(selectData):
    if selectData is None:
        raise PreventUpdate
    else:
        dtc_value = selectData["points"][0]["customdata"][0]
        return [{'label': i, 'value': i} for i in list(dtc_list[dtc_value]['30'].keys())]

@callback(
    Output('select-30-signal-1', 'data'),
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
        if signal is None  or snapshot_hoverData is None:
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

    
@callback(
    Output('select-did-2', 'data'),
    Input('select-snapshot-2','value'),
    Input('dtc-plot','selectedData')
)
def update_2040_did_dp_list(snapshot_value, selectedData):
    if snapshot_value is None or selectedData is None:
        raise PreventUpdate
    else:
        dtc_value = selectedData["points"][0]["customdata"][0]
        return [{'label': i, 'value': i} for i in list(dtc_list[dtc_value][snapshot_value].keys())]


@callback(
    Output('select-signal-2', 'data'),
    Input('select-did-2','value'),
    Input('select-snapshot-2','value'),
    Input('dtc-plot','selectedData')
)
def update_2040_signal_dp_list(did_value, snapshot_value, selectedData):
    if snapshot_value is None or did_value is None:
        raise PreventUpdate
    else:
        dtc_value = selectedData["points"][0]["customdata"][0]
        return [{'label': i, 'value': i} for i in dtc_list[dtc_value][snapshot_value][did_value]]

        
@callback(
    Output('snapshot-plot-2', 'figure'),
    Output('snapshot-value-report-2',  'children'),
    Output('did-value-report-2', 'children'),
    Output('signal-value-report-2','children'),
    [Input('select-snapshot-2', 'value'),
    Input('select-did-2',  'value'),
    Input('select-signal-2',  'value'),
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
            fig.update_layout( 
                        height = 240,  
                    )
            return fig, snapshot_value, did_value, signal
            
    except IndexError:
        raise PreventUpdate


@callback(
    Output('x-values-graph-2','data'),
    Output('y-values-graph-2','data'),
    Output('customdata-graph-2','data'),
    Input('snapshot-plot-2', 'selectedData'),  
)
def update_select_data(selectData):
    selected_x_values = []
    selected_y_values = []
    selected_index = []
    if selectData is None or len(selectData["points"]) == 0:
        raise PreventUpdate
    elif len(selectData["points"]) > 1:
        for i in range(len(selectData["points"])):
            selected_x_values.append(selectData["points"][i]["x"])
            selected_y_values.append(selectData["points"][i]["y"])
            selected_index.extend(selectData["points"][i]["customdata"])
    else:
        selected_x_values = [selectData["points"][0]["x"]]
        selected_y_values = [selectData["points"][0]["y"]]
        selected_index = [selectData["points"][0]["customdata"]]
    return selected_x_values,selected_y_values,selected_index


@callback(
    Output('select-30-did-2', 'data'),
    Input('dtc-plot','selectedData')
)
def update_30_did_dp_list(selectData):
    if selectData is None:
        raise PreventUpdate
    else:
        dtc_value = selectData["points"][0]["customdata"][0]
        return [{'label': i, 'value': i} for i in list(dtc_list[dtc_value]['30'].keys())]

@callback(
    Output('select-30-signal-2', 'data'),
    Input('select-30-did-2','value'),
    State('dtc-plot','selectedData')
)
def update_30_signal_dp_list(did_value, selectData):
    if selectData is None or did_value is None:
        raise PreventUpdate
    else:
        dtc_value = selectData["points"][0]["customdata"][0]
        return [{'label': i, 'value': i} for i in dtc_list[dtc_value]['30'][did_value]]


@callback(
    Output('snapshot-30-plot-2','figure'),
    [Input('select-30-did-2', 'value'),
    Input('select-30-signal-2',  'value'),
    Input('dtc-plot', 'selectedData'),
    Input('customdata-graph-2','data')]
)
def update_snapshot_graph( did_value, signal, dtc_hoverData, snapshot_hoverData):
    try:
        if signal is None or snapshot_hoverData is None:
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



@callback(
    Output('select-did-3', 'data'),
    Input('select-snapshot-3','value'),
    Input('dtc-plot','selectedData')
)
def update_2040_did_dp_list(snapshot_value, selectedData):
    if snapshot_value is None or selectedData is None:
        raise PreventUpdate
    else:
        dtc_value = selectedData["points"][0]["customdata"][0]
        return [{'label': i, 'value': i} for i in list(dtc_list[dtc_value][snapshot_value].keys())]


@callback(
    Output('select-signal-3', 'data'),
    Input('select-did-3','value'),
    Input('select-snapshot-3','value'),
    Input('dtc-plot','selectedData')
)
def update_2040_signal_dp_list(did_value, snapshot_value, selectedData):
    if snapshot_value is None or did_value is None:
        raise PreventUpdate
    else:
        dtc_value = selectedData["points"][0]["customdata"][0]
        return [{'label': i, 'value': i} for i in dtc_list[dtc_value][snapshot_value][did_value]]

        
@callback(
    Output('snapshot-plot-3', 'figure'),
    Output('snapshot-value-report-3',  'children'),
    Output('did-value-report-3', 'children'),
    Output('signal-value-report-3','children'),
    [Input('select-snapshot-3', 'value'),
    Input('select-did-3',  'value'),
    Input('select-signal-3',  'value'),
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
            fig.update_layout( 
                    height = 240,  
                )
            return fig, snapshot_value, did_value, signal
            
    except IndexError:
        raise PreventUpdate

@callback(
    Output('x-values-graph-3','data'),
    Output('y-values-graph-3','data'),
    Output('customdata-graph-3','data'),
    Input('snapshot-plot-3', 'selectedData'),  
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
        selected_x_values = [selectData["points"][0]["x"]]
        selected_y_values = [selectData["points"][0]["y"]]
        selected_index = [selectData["points"][0]["customdata"]]
    return selected_x_values,selected_y_values,selected_index


@callback(
    Output('select-30-did-3', 'data'),
    Input('dtc-plot','selectedData')
)
def update_30_did_dp_list(selectData):
    if selectData is None:
        raise PreventUpdate
    else:
        dtc_value = selectData["points"][0]["customdata"][0]
        return [{'label': i, 'value': i} for i in list(dtc_list[dtc_value]['30'].keys())]

@callback(
    Output('select-30-signal-3', 'data'),
    Input('select-30-did-3','value'),
    State('dtc-plot','selectedData')
)
def update_30_signal_dp_list(did_value, selectData):
    if selectData is None or did_value is None:
        raise PreventUpdate
    else:
        dtc_value = selectData["points"][0]["customdata"][0]
        return [{'label': i, 'value': i} for i in dtc_list[dtc_value]['30'][did_value]]


@callback(
    Output('snapshot-30-plot-3','figure'),
    [Input('select-30-did-3', 'value'),
    Input('select-30-signal-3',  'value'),
    Input('dtc-plot', 'selectedData'),
    Input('customdata-graph-3','data'),]
)
def update_snapshot_graph( did_value, signal, dtc_hoverData, snapshot_hoverData):
    try:
        if signal is None  or snapshot_hoverData is None:
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


@callback(
    Output('select-did-4', 'data'),
    Input('select-snapshot-4','value'),
    Input('dtc-plot','selectedData')
)
def update_2040_did_dp_list(snapshot_value, selectedData):
    if snapshot_value is None or selectedData is None:
        raise PreventUpdate
    else:
        dtc_value = selectedData["points"][0]["customdata"][0]
        return [{'label': i, 'value': i} for i in list(dtc_list[dtc_value][snapshot_value].keys())]


@callback(
    Output('select-signal-4', 'data'),
    Input('select-did-4','value'),
    Input('select-snapshot-4','value'),
    Input('dtc-plot','selectedData')
)
def update_2040_signal_dp_list(did_value, snapshot_value, selectedData):
    if snapshot_value is None or did_value is None:
        raise PreventUpdate
    else:
        dtc_value = selectedData["points"][0]["customdata"][0]
        return [{'label': i, 'value': i} for i in dtc_list[dtc_value][snapshot_value][did_value]]

        
@callback(
    Output('snapshot-plot-4', 'figure'),
    Output('snapshot-value-report-4',  'children'),
    Output('did-value-report-4', 'children'),
    Output('signal-value-report-4','children'),
    [Input('select-snapshot-4', 'value'),
    Input('select-did-4',  'value'),
    Input('select-signal-4',  'value'),
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
            return fig, snapshot_value, did_value, signal
            
    except IndexError:
        raise PreventUpdate

@callback(
    Output('x-values-graph-4','data'),
    Output('y-values-graph-4','data'),
    Output('customdata-graph-4','data'),
    Input('snapshot-plot-4', 'selectedData'),  
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
        selected_x_values = [selectData["points"][0]["x"]]
        selected_y_values = [selectData["points"][0]["y"]]
        selected_index = [selectData["points"][0]["customdata"]]
    return selected_x_values,selected_y_values,selected_index


@callback(
    Output('select-30-did-4', 'data'),
    Input('dtc-plot','selectedData')
)
def update_30_did_dp_list(selectData):
    if selectData is None:
        raise PreventUpdate
    else:
        dtc_value = selectData["points"][0]["customdata"][0]
        return [{'label': i, 'value': i} for i in list(dtc_list[dtc_value]['30'].keys())]

@callback(
    Output('select-30-signal-4', 'data'),
    Input('select-30-did-4','value'),
    State('dtc-plot','selectedData')
)
def update_30_signal_dp_list(did_value, selectData):
    if selectData is None or did_value is None:
        raise PreventUpdate
    else:
        dtc_value = selectData["points"][0]["customdata"][0]
        return [{'label': i, 'value': i} for i in dtc_list[dtc_value]['30'][did_value]]


@callback(
    Output('snapshot-30-plot-4','figure'),
    [Input('select-30-did-4', 'value'),
    Input('select-30-signal-4',  'value'),
    Input('dtc-plot', 'selectedData'),
    Input('customdata-graph-4','data')]
)
def update_snapshot_graph( did_value, signal, dtc_hoverData, snapshot_hoverData):
    try:
        if signal is None  or snapshot_hoverData is None:
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


# @callback(
#     Output('clickdata-data1','children'),
#     Input('customdata-graph-1','data'),
#     Input('customdata-graph-2','data'),
#     Input('dtc-plot', 'selectedData'),
# )
# def update_select_data(vin_1,vin_2,selected_dtc):
#     check_list = [vin_1,vin_2,selected_dtc]
#     if None in check_list:
#         raise PreventUpdate
#     else:
#         dtc_value = selected_dtc["points"][0]["x"]
#         dtc_filtered_df = df[df.columns[df.columns.str.contains(dtc_value)==True]]
#         filter_data_df_1 =  dtc_filtered_df.filter(items= vin_1, axis = 0)
#         filter_data_df_2 = filter_data_df_1.filter(items= vin_2, axis = 0)
#         return json.dumps(list(filter_data_df_2.index))
  

@callback(
    [Output('filtered-vin','children'),
    Output('filterdcars-count','children'),
    Output('vin-list','children')],
    Input('dtc-plot', 'selectedData'),
    Input('customdata-graph-1','data'),
    Input('customdata-graph-2','data'),
    Input('customdata-graph-3','data'),
    Input('customdata-graph-4','data'),
)
def update_select_data(selected_dtc, vin_from_graph_1,vin_from_graph_2,vin_from_graph_3,vin_from_graph_4):
    
    if selected_dtc is None or vin_from_graph_1 is None or vin_from_graph_2 is None or vin_from_graph_3 is None or vin_from_graph_4 is None :
        raise PreventUpdate
    else:
        dtc_value = selected_dtc["points"][0]["x"]
        dtc_filtered_df = df[df.columns[df.columns.str.contains(dtc_value)==True]].copy()
        filter_data_df_1 =  dtc_filtered_df.filter(items= vin_from_graph_1, axis = 0)
        filter_data_df_2 = filter_data_df_1.filter(items= vin_from_graph_2, axis = 0)
        filter_data_df_3 = filter_data_df_2.filter(items= vin_from_graph_3, axis = 0)
        filter_data_df_4 = filter_data_df_3.filter(items= vin_from_graph_4, axis = 0)
        vin_publish =  list(df.loc[filter_data_df_4.index,:]['vin'])
        
        return json.dumps(vin_publish),  json.dumps(len(vin_publish)), json.dumps(vin_publish)
  
@callback(
    Output('filterd_data', 'data'),
    Input('dtc-plot', 'selectedData'),
    Input('customdata-graph-1','data'),
    Input('customdata-graph-2','data'),
    Input('customdata-graph-3','data'),
    Input('customdata-graph-4','data'),
)
def update_select_data(selected_dtc, vin_from_graph_1,vin_from_graph_2,vin_from_graph_3,vin_from_graph_4):
    none_check_list = [selected_dtc, vin_from_graph_1,vin_from_graph_2,vin_from_graph_3,vin_from_graph_4]
    if any(x is None for x in  none_check_list):
        raise PreventUpdate
    else:
        dtc_value = selected_dtc["points"][0]["x"]
        dtc_filtered_df = df[df.columns[df.columns.str.contains(dtc_value)==True]].copy()
        filter_data_df_1 =  dtc_filtered_df.filter(items= vin_from_graph_1, axis = 0)
        filter_data_df_2 = filter_data_df_1.filter(items= vin_from_graph_2, axis = 0)
        filter_data_df_3 = filter_data_df_2.filter(items= vin_from_graph_3, axis = 0)
        filter_data_df_4 = filter_data_df_3.filter(items= vin_from_graph_4, axis = 0)
        save_filtered_data = df.loc[filter_data_df_4.index,:]
        return save_filtered_data.to_dict('records')

@callback(
    Output("download-dataframe-xlsx", "data"),
    Input("excel_download", "n_clicks"),
    State('filterd_data','data'),
    prevent_initial_call=True,
)
def func(n_clicks, dataframe_filtered):
    df_fill = pd.DataFrame(dataframe_filtered)
    return dcc.send_data_frame(df_fill.to_excel, "mydf.xlsx", sheet_name="Sheet_name_1", index='False')


@callback(
    Output('report-model', 'children'),
    Output('report-dtc', 'children'),
    Output('report-count', 'children'),
    Output('report-percentage', 'children'),
    [Input('Car_model', 'data'),
    Input('selected-dtc','data'),
    State('dtc-plot', 'selectedData'),]

)
def update_report(car_model, dtc_value,selectData):
    if selectData is None:
        raise PreventUpdate
    else:
        count_value = selectData["points"][0]["customdata"][2]
        percentage = selectData["points"][0]["customdata"][1]
        return car_model, dtc_value, count_value, round(percentage,3)


@callback(
    Output('graph-report-1', 'figure'),
    Input('snapshot-plot-1', 'selectedData'),
    Input('snapshot-plot-1', 'relayoutData'),
    Input("filter-number", "value"),
    State('snapshot-plot-1', 'figure'),
)
def update_report_graph(selectData, releydatOut, track_value_width, figure_data):
    if figure_data is None:
        raise PreventUpdate
    else:
        fig = go.Figure(figure_data)
        if track_value_width in [1,2]:
            
            fig.update_layout(
                height = 170,
                width = 600,
                margin = dict(
                        autoexpand = False, 
                        b = 30, 
                        t = 25, 
                        l = 20,
                        r = 10
                    ),
            )
        else:
            fig.update_layout(
                height = 170,
                width = 250,
                margin = dict(
                        autoexpand = False, 
                        b = 30, 
                        t = 25, 
                        l = 20,
                        r = 10
                    ),
            )
        return fig

@callback(
    Output('table-report-1','data'),
    Input('x-values-graph-1','data'),
    Input('y-values-graph-1','data'),
)
def update_report_table(value_col, percentage_col):
    if value_col is None or percentage_col is None:
        raise PreventUpdate
    elif len([percentage_col])==1:
        if type(percentage_col) is  float:
            table_df = pd.DataFrame({"value":[value_col], "percentage": [percentage_col]}, index=[0]).round(3)
            return table_df.to_dict('records')
        else:
            table_df = pd.DataFrame({"value":value_col, "percentage": percentage_col}).sort_values(by="percentage",  ascending=False).round(3)
            displaydf = table_df.head(2)
            return displaydf.to_dict('records')


@callback(
    Output('graph-report-2', 'figure'),
    Input('snapshot-plot-2', 'selectedData'),
    Input('snapshot-plot-2', 'relayoutData'),
    Input("filter-number", "value"),
    State('snapshot-plot-2', 'figure'),
)
def update_report_graph(selectData, releydatOut, track_value_width, figure_data):
    none_check_list = [selectData, releydatOut, figure_data]
    if any(x is None for x in  none_check_list):
        raise PreventUpdate
    else:
        fig = go.Figure( figure_data)
        if track_value_width == 2:
            fig.update_layout(
                height = 170,
                width = 600,
                margin = dict(
                        autoexpand = False, 
                        b = 30, 
                        t = 25, 
                        l = 20,
                        r = 10
                    ),
            )
        else:
            fig.update_layout(
                height = 170,
                width = 250,
                margin = dict(
                        autoexpand = False, 
                        b = 30, 
                        t = 25, 
                        l = 20,
                        r = 10
                    ),
            )
        return fig

@callback(
    Output('table-report-2','data'),
    Input('x-values-graph-2','data'),
    Input('y-values-graph-2','data'),
)
def update_report_table(value_col, percentage_col):
    if value_col is None or percentage_col is None:
        raise PreventUpdate
    elif len([percentage_col])==1:
        if type(percentage_col) is  float:
            table_df = pd.DataFrame({"value":[value_col], "percentage": [percentage_col]}, index=[0]).round(3)
            return table_df.to_dict('records')
        else:
            table_df = pd.DataFrame({"value":value_col, "percentage": percentage_col}).sort_values(by="percentage",  ascending=False).round(3)
            displaydf = table_df.head(2)
            return displaydf.to_dict('records')

@callback(
    Output('graph-report-3', 'figure'),
    Input('snapshot-plot-3', 'selectedData'),
    Input('snapshot-plot-3', 'relayoutData'),
    Input("filter-number", "value"),
    State('snapshot-plot-3', 'figure'),
)
def update_report_graph(selectData, releydatOut, track_value_width, figure_data):
    none_check_list = [selectData, releydatOut, figure_data]
    if any(x is None for x in  none_check_list):
        raise PreventUpdate
    else:
        fig = go.Figure( figure_data)
        if track_value_width == 3:
            fig.update_layout(
                height = 170,
                width = 600,
                margin = dict(
                        autoexpand = False, 
                        b = 30, 
                        t = 25, 
                        l = 20,
                        r = 10
                    ),
            )
        else:
            fig.update_layout(
                height = 170,
                width = 250,
                margin = dict(
                        autoexpand = False, 
                        b = 30, 
                        t = 25, 
                        l = 20,
                        r = 10
                    ),
            )
        return fig
@callback(
    Output('table-report-3','data'),
    Input('x-values-graph-3','data'),
    Input('y-values-graph-3','data'),
)
def update_report_table(value_col, percentage_col):
    if value_col is None or percentage_col is None:
        raise PreventUpdate
    elif len([percentage_col])==1:
        if type(percentage_col) is  float:
            table_df = pd.DataFrame({"value":[value_col], "percentage": [percentage_col]}, index=[0]).round(3)
            return table_df.to_dict('records')
        else:
            table_df = pd.DataFrame({"value":value_col, "percentage": percentage_col}).sort_values(by="percentage",  ascending=False).round(3)
            displaydf = table_df.head(2)
            return displaydf.to_dict('records')


@callback(
    Output('graph-report-4', 'figure'),
    Input('snapshot-plot-4', 'selectedData'),
    Input('snapshot-plot-4', 'relayoutData'),
    State('snapshot-plot-4', 'figure'),
)
def update_report_graph(selectData, releydatOut, figure_data):
    none_check_list = [selectData, releydatOut, figure_data]
    if any(x is None for x in  none_check_list):
        raise PreventUpdate
    else:
        fig = go.Figure( figure_data)
        fig.update_layout(
                height = 180,
                width = 250,
                margin = dict(
                    autoexpand = False, 
                    b = 30, 
                    t = 25, 
                    l = 20,
                    r = 10
                ),
            )
        return fig

@callback(
    Output('table-report-4','data'),
    Input('x-values-graph-4','data'),
    Input('y-values-graph-4','data'),
)
def update_report_table(value_col, percentage_col):
    if value_col is None or percentage_col is None:
        raise PreventUpdate
    elif len([percentage_col])==1:
        if type(percentage_col) is  float:
            table_df = pd.DataFrame({"value":[value_col], "percentage": [percentage_col]}, index=[0]).round(3)
            return table_df.to_dict('records')
        else:
            table_df = pd.DataFrame({"value":value_col, "percentage": percentage_col}).sort_values(by="percentage",  ascending=False).round(3)
            displaydf = table_df.head(2)
            return displaydf.to_dict('records')

@callback(
    Output('tracks-list', 'data'),
    Input('dtc-plot','selectedData')
)
def update_30_did_dp_list(selectData):
    if selectData is None:
        raise PreventUpdate
    else:
        dtc_value = selectData["points"][0]["customdata"][0]
        return [{'label': i, 'value': i} for i in list(dtc_list[dtc_value]['30'].keys())]

@callback(
    Output('all-graphs-30', 'children'),
    Input('tracks-list', 'value'),
    Input('dtc-plot','selectedData'),
    Input('all-graphs-30', 'children'),

)
def update_layout(track_name, selectData, updated_graph_layout):
    if selectData is None or track_name is None:
        raise PreventUpdate
    else:
        dtc_value = selectData["points"][0]["customdata"][0]
        layout_length = len(dtc_list[dtc_value]['30'][track_name])
        updated_graph_layout =  html.Div([
            snapshot_30_graph_item(i) for i in range(layout_length)
        ])
        return updated_graph_layout

# @callback(
#     Output({'type': 'graph-pertrack','index': MATCH}, 'figure'),
#     Input({'type': 'graph-pertrack','index': MATCH}, 'id'),
#     State('tracks-list', 'value'),
#     State('dtc-plot','selectedData'),
# )
# def up_graph(figure_index,track_name, selectData):
#     if selectData is None or track_name is None or figure_index is None:
#         raise PreventUpdate
#     else:
#         dtc_value = selectData["points"][0]["customdata"][0]
#         signal_selected = dtc_list[dtc_value]['30'][track_name][figure_index['index']]
#         dtc_filtered_df = df[df.columns[df.columns.str.contains(dtc_value)==True]]
#         dtc_filtered_df =  dtc_filtered_df.dropna(thresh = dtc_filtered_df.shape[0]*0.7,how='all',axis=0)
#         dtc_filtered_df =  dtc_filtered_df.dropna(thresh = dtc_filtered_df.shape[0]*0.7,how='all',axis=1)

#         trace_data = plot_snapshots_30_all(dtc_filtered_df,did_information, dtc_value,track_name, signal_selected)
#         fig = go.Figure(trace_data)
#         fig.update_layout(
#                 height = 170,
#                 width = 700,
#             )
#         return fig
