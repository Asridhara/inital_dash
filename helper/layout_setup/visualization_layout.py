from dash import dcc, html
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import dash_table




report_table_columns=[{'name': 'value', 'id': 'value'},
         {'name': '%', 'id': 'percentage'}, ]



# def create_graph_cards(number):
#     graph_name = 'Snapshot 20/40 plot'
#     snapshot_id = 'select-snapshot-'+ str(number)
#     did_id = 'select-did-'+ str(number)
#     signal_id = 'select-signal-'+ str(number)

#     graph_card = dbc.Card(
#         [
#           dbc.CardHeader(graph_name),
#           dbc.CardBody([
#             dbc.Row([
#                  dbc.Col([
#                     dmc.RadioGroup(
#                         id= snapshot_id,
#                         data=[
#                             {"value": "20", "label": "20"},
#                             {"value": "40", "label": "40"},
#                         ],
#                         orientation = 'vertical',
#                         value="20",
#                         size="sm",
#                         ),
#                     ], width=2),
#                 # dbc.Col([html.Label(['Snapshots'], 
#                 #     style={'font-weight': 'bold', "text-align": "center"}),
#                 #     dcc.Dropdown(id = snapshot_id )], width={"size": 1}),
#                 dbc.Col([html.Label(['DID'], 
#                     style={'font-weight': 'bold', "text-align": "center"}),
#                     dcc.Dropdown(id = did_id, optionHeight = 50)], width={"size": 3}),
#                 dbc.Col([html.Label(['Signal'], 
#                     style={'font-weight': 'bold', "text-align": "center"}),
#                     dcc.Dropdown(id = signal_id, optionHeight = 50)], width={"size": 7})
#                 ]),
#             ]),
#         ], 
#     )
#     return graph_card


def create_graph_cards(number):
    graph_name = 'Snapshot 20/40 plot'
    snapshot_id = 'select-snapshot-'+ str(number)
    did_id = 'select-did-'+ str(number)
    signal_id = 'select-signal-'+ str(number)

    graph_card = dbc.Card(
        [
          dbc.CardHeader(graph_name),
          dbc.CardBody([
            dbc.Row([
                 dbc.Col([
                    dmc.RadioGroup(
                        id= snapshot_id,
                        data=[
                            {"value": "20", "label": "20"},
                            {"value": "40", "label": "40"},
                        ],
                        orientation = 'vertical',
                        value="20",
                        size="sm",
                        ),
                    ], width=2),
                    dbc.Col([
                        dmc.Select(
                            label="DID",
                            id= did_id,
                        ),
                    ], width={"size": 3}),
                dbc.Col([
                        dmc.Select(
                        label="Signals",
                        id= signal_id,
                    ),
                    ], width={"size": 7})
                ]),
            ]),
        ], 
    )
    return graph_card


# def create_filter_cards(number):
#     graph_name = 'Snapshot 30 time series plot'
#     snapshot_id = 'select-30-snapshot-'+ str(number)
#     did_id = 'select-30-did-'+ str(number)
#     signal_id = 'select-30-signal-'+ str(number)

#     graph_card =     dbc.Card(
#         [
#             dbc.CardHeader(graph_name),
#             dbc.CardBody([
#             dbc.Row([
#                 dbc.Col([html.Label(['DID'], 
#                     style={'font-weight': 'bold', "text-align": "center"}),
#                     dcc.Dropdown(id = did_id, optionHeight = 50)],  width={"size": 3}),
#                 dbc.Col([html.Label(['Signal'], 
#                     style={'font-weight': 'bold', "text-align": "center"}),
#                     dcc.Dropdown(id = signal_id, optionHeight = 50)])
#                 ]),
#             ]),
#         ],
#     )
#     return graph_card

def create_filter_cards(number):
    graph_name = 'Snapshot 30 time series plot'
    snapshot_id = 'select-30-snapshot-'+ str(number)
    did_id = 'select-30-did-'+ str(number)
    signal_id = 'select-30-signal-'+ str(number)

    graph_card =     dbc.Card(
        [
            dbc.CardHeader(graph_name),
            dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dmc.Select(
                            label="DID",
                            id= did_id,
                        ),
                ],  width={"size": 3}),
                dbc.Col([
                     dmc.Select(
                            label="Signal",
                            id= signal_id,
                    ),
                ])
                ]),
            ]),
        ],
    )
    return graph_card  



def create_store_for_graph(number):
    x_id = 'x-values-graph-'+str(number)
    y_id = 'y-values-graph-'+str(number)
    customdata_id = 'customdata-graph-'+str(number)

    return html.Div([
        dcc.Store(id = x_id),
        dcc.Store(id = y_id),
        dcc.Store(id = customdata_id)
    ])


def create_dtc_plot_with_summary():
    dtc_graph_layout = html.Div([
        dbc.Row([
            dbc.Col([dcc.Graph(id='dtc-plot')], width = 9,  style = {"heights":600}),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5('Software label'),
                        html.Pre(id='hover-data')
                        ],style = {"heights":150}), 
                    ]),
                html.Br(),
                dbc.Card(
                    dbc.CardBody([
                        html.H5('DTC Description'),
                        html.Pre(id='click-data')
                    ])
                ),
                html.Br(),
                dbc.Card(
                    dbc.CardBody([
                        html.H5('Count'),
                        html.Pre(id='Count-data')
                    ])
                ),
                html.Br(),
                dbc.Card(
                    dbc.CardBody([
                        html.H5('Percentage'),
                        html.Pre(id='Percentage-data')
                    ])
                ),
            ], width = 3)
        ]),

        dcc.Store(id='selected-dtc',  storage_type = 'local'),
        dcc.Store(id = 'dtc-graph-data'),

    ])
    return dtc_graph_layout

def create_snapshot_graph_layout(number):
    snapshot_plot_id = 'snapshot-plot-'+str(number)
    snapshot_30_plot_id = 'snapshot-30-plot-'+str(number)
    snapshot_display_id = 'snapshot-display-'+str(number)

    both_filter_graph_layout = html.Div([
            dbc.Row([
                dbc.Col(
                    [
                        dbc.Row([ 
                            dbc.Col(create_graph_cards(number), width={"size": 5 }, style={'margin-right': '0px', 'margin-left': '0px'}),
                            dbc.Col(create_filter_cards(number), width={"size": 7}, style={'margin-right': '0px', 'margin-left': '0px'}),
                            ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col(dcc.Graph(id = snapshot_plot_id,className="h-100") , width = {"size": 5}, style={'margin-right': '0px', 'margin-left': '0px','height': 240}),
                            dbc.Col(dcc.Graph(id = snapshot_30_plot_id, className="h-100") , width = {"size": 7}, style={'margin-right': '0px', 'margin-left': '0px','height': 240})
                            ]),
                    ], width={ "offset": 0}, style = {"heights":350})
                ]),

            create_store_for_graph(number),

            html.Hr(),
        ], id = snapshot_display_id, style= {'display': 'block'})

    return both_filter_graph_layout


def create_report_each_signal(number):
    snapshot_id = 'snapshot-value-report-'+str(number)
    did_id = 'did-value-report-'+str(number)
    signal_id = 'signal-value-report-'+str(number)
    plot_id = 'graph-report-'+str(number)
    table_id = 'table-report-'+str(number)

    filter =  dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([dmc.Text("Snapshot: ")]),
                        dbc.Col([html.Pre(id = snapshot_id)], width = {"size": 8}),
                    ],style = {'height':'20px'}),
                    dbc.Row([
                        dbc.Col([dmc.Text("DID: ")]),
                        dbc.Col([html.Pre(id = did_id )], width = {"size": 8}),
                    ],style = {'height':'20px'}),
                    dbc.Row([
                        dbc.Col([dmc.Text("Signal: ")]),
                        dbc.Col([html.Pre(id =signal_id)], width = {"size": 8}),
                    ],style = {'height':'20px'}),
                    
                    dcc.Graph(id= plot_id,  style={'height': 200, "marginLeft": 20, "marginTop": 15 ,"marginBottom": 15}),

                    html.Div([
                        dash_table.DataTable(
                            id= table_id,
                            columns= report_table_columns,
                            data = [],
                            page_current=0,
                            page_size=2,
                            style_table={'overflowX': 'auto'},
                            style_header={
                                'color': 'black',
                                'fontWeight': 'bold'
                                },
                            style_as_list_view=True,
                            ),
                    ]),  

                ]),
            ])

    return filter

def create_report_selected_signal(number):
    snapshot_report_id = "snapshot-value-report-"+str(number)
    did_value_id = "did-value-report-"+str(number)
    signal_value_id = "signal-value-report-"+str(number)
    graph_report_id =  "graph-report-"+str(number)
    table_report_id = "table-report-"+str(number)

    report_graph_layout = html.Div([
        dbc.Row([
            dbc.Col([dmc.Text("Snapshot: ")]),
            dbc.Col([html.Pre(id = snapshot_report_id)], width = {"size": 8}),
        ],style = {'height':'20px'}),
        dbc.Row([
            dbc.Col([dmc.Text("DID: ")]),
            dbc.Col([html.Pre(id = did_value_id )], width = {"size": 8}),
        ],style = {'height':'20px'}),
        dbc.Row([
            dbc.Col([dmc.Text("Signal: ")]),
            dbc.Col([html.Pre(id = signal_value_id, className="no-scrollbars")], width = {"size": 8}),
        ],style = {'height':'20px'}),

        dcc.Graph(id= graph_report_id, figure= dict(data = [], layout = []), style={'height': 200, "marginLeft": 10, "marginTop": 15 ,"marginBottom": 15}),

        html.Div([
            dash_table.DataTable(
                id= table_report_id,
                columns= [{'name': 'value', 'id': 'value'},
                            {'name': '%', 'id': 'percentage'}],
                data = [],
                page_current=0,
                page_size=2,
                style_table={'overflowX': 'auto'},
                style_header={
                    'color': 'black',
                    'fontWeight': 'bold'
                    },
                style_as_list_view=True,
                ),
        ]),  
    ])
    return report_graph_layout


def graph_layout_header():
    report_header = html.Div([
        dbc.Row([
                    dbc.Col([html.H3("Fault Report"),],  width={"size": 4, "offset": 5})
                ],align="end",
            className="pad-row",
            style= {
                "marginTop": 20,
            }),  

            dmc.Divider(size="lg"),

            dmc.Space(h =20),

            dbc.Row([
                dbc.Col([html.H6("Model")], width = {"size": 3}),
                dbc.Col([html.H6("DTC")], width = {"size": 3}),
                dbc.Col([html.H6("Count")], width = {"size": 3}),
                dbc.Col([html.H6("Percentage")], width = {"size": 3}),
            ]),

            dbc.Row([
                dbc.Col([html.Pre(id ="report-model")], width = {"size": 3}),
                dbc.Col([html.Pre(id ="report-dtc")], width = {"size": 3}),
                dbc.Col([html.Pre(id ="report-count")], width = {"size": 3}),
                dbc.Col([html.Pre(id ="report-percentage")], width = {"size": 3}),       
            ]),
    ])
    return report_header


def filtered_cars_report_layout():

    filtred_cars_output = html.Div([
                            html.H6('Filtered Cars and VINs'),
                            dbc.Row(
                                [
                                    dbc.Col([
                                        dbc.Card([
                                            dbc.CardBody([
                                                html.Pre(id='filterdcars-count',
                                                style = {"height": 20, 
                                                        "overflow-y": "scroll"},
                                                className="no-scrollbars")
                                            ])
                                        ]),
                                    ],
                                    width = {"size": 2},
                                    ),

                                    dbc.Col([
                                        dbc.Card([
                                            dbc.CardBody([
                                                html.Pre(id='vin-list',
                                                style = {"height": 20, 
                                                        "overflowY": "scroll"},
                                                className="no-scrollbars")
                                                ])
                                            ]),
                                    ],
                                    width = {"size": 9}),
                                ]),
                            ])

    return filtred_cars_output


def create_report_selected_signal(number):
    snapshot_report_id = "snapshot-value-report-"+str(number)
    did_value_id = "did-value-report-"+str(number)
    signal_value_id = "signal-value-report-"+str(number)
    graph_report_id =  "graph-report-"+str(number)
    table_report_id = "table-report-"+str(number)

    report_graph_layout = html.Div([
        dbc.Row([
            dbc.Col([dmc.Text("Snapshot: ")]),
            dbc.Col([html.Pre(id = snapshot_report_id)], width = {"size": 8}),
        ],style = {'height':'20px'}),
        dbc.Row([
            dbc.Col([dmc.Text("DID: ")]),
            dbc.Col([html.Pre(id = did_value_id )], width = {"size": 8}),
        ],style = {'height':'20px'}),
        dbc.Row([
            dbc.Col([dmc.Text("Signal: ")]),
            dbc.Col([html.Pre(id = signal_value_id, className="no-scrollbars")], width = {"size": 8}),
        ],style = {'height':'20px'}),

        dcc.Graph(id= graph_report_id, figure= dict(data = [], layout = []), style={'height': 200, "marginLeft": 10, "marginTop": 15 ,"marginBottom": 15}),

        html.Div([
            dash_table.DataTable(
                id= table_report_id,
                columns= [{'name': 'value', 'id': 'value'},
                            {'name': '%', 'id': 'percentage'}],
                data = [],
                page_current=0,
                page_size=2,
                style_table={'overflowX': 'auto'},
                style_header={
                    'color': 'black',
                    'fontWeight': 'bold'
                    },
                style_as_list_view=True,
                ),
        ]),  
    ])
    return report_graph_layout



def filtered_cars_report_layout():

    filtred_cars_output = html.Div([
                            html.H6('Filtered Cars and VINs'),
                            dbc.Row(
                                [
                                    dbc.Col([
                                        dbc.Card([
                                            dbc.CardBody([
                                                html.Pre(id='filterdcars-count',
                                                style = {"height": 20, 
                                                        "overflow-y": "scroll"},
                                                className="no-scrollbars")
                                            ])
                                        ] ,
                                        ),
                                    ],
                                    width = {"size": 2},
                                    ),

                                    dbc.Col([
                                        dbc.Card([
                                            dbc.CardBody([
                                                html.Pre(id='vin-list',
                                                style = {"height": 20, 
                                                        "overflowY": "scroll"},
                                                className="no-scrollbars")
                                                ])
                                            ]),
                                    ],
                                    width = {"size": 9}),
                                ]),
                            ])

    return filtred_cars_output

    

def graph_layout_header():
    report_header = html.Div([
        dbc.Row([
                    dbc.Col([html.H3("Fault Report"),],  width={"size": 4, "offset": 5})
                ],align="end",
            className="pad-row",
            style= {
                "marginTop": 20,
            }),  

            dmc.Divider(size="lg"),

            dmc.Space(h =20),

            dbc.Row([
                dbc.Col([html.H6("Model")], width = {"size": 3}),
                dbc.Col([html.H6("DTC")], width = {"size": 3}),
                dbc.Col([html.H6("Count")], width = {"size": 3}),
                dbc.Col([html.H6("Percentage")], width = {"size": 3}),
            ]),

            dbc.Row([
                dbc.Col([html.Pre(id ="report-model")], width = {"size": 3}),
                dbc.Col([html.Pre(id ="report-dtc")], width = {"size": 3}),
                dbc.Col([html.Pre(id ="report-count")], width = {"size": 3}),
                dbc.Col([html.Pre(id ="report-percentage")], width = {"size": 3}),       
            ]),
    ])
    return report_header

def graph_layout_one_filter():
    graph_layout = html.Div([
                    dbc.Row([
                        dbc.Col([
                            create_report_selected_signal(1),
                        ])
                    ], style={'margin-right': '20px', 'margin-left': '20px'}),
                    html.Br(),
                    dmc.Divider(size="lg"),             
            ])
    return graph_layout
    


def graph_layout_two_filter():
    graph_layout = html.Div([
                    dbc.Row([
                        create_report_selected_signal(1),  
                    ],  style={'margin-right': '20px', 'margin-left': '0px'}),

                    html.Br(),
                    
                    dmc.Divider(size="lg"),

                    html.Br(),

                    dbc.Row([
                        create_report_selected_signal(2), 
                    ],  style={ 'margin-left': '0px'}), 
                    html.Br(), 
            ])
    return graph_layout



def graph_layout_three_filter():
    graph_layout = html.Div([
                    dbc.Row([
                        dbc.Col([
                            create_report_selected_signal(1),
                        ],width = {"size": 5}, style={'margin-right': '0px', 'margin-left': '0px'}),
                        dbc.Col([
                            create_report_selected_signal(2),
                        ],width = {"size": 5}, style={'margin-right': '0px', 'margin-left': '0px'}),
                    ], style = { 'margin-left': '20px'}),

                    html.Br(),
                    
                    dmc.Divider(size="lg"),

                    html.Br(),

                    dbc.Row([
                        dbc.Col([
                            create_report_selected_signal(3),
                        ])
                    ], style={'margin-right': '20px', 'margin-left': '20px'}),
                ])
    return graph_layout

def graph_layout_four_filter():
    graph_layout = html.Div([
                    dbc.Row([
                        dbc.Col([
                            create_report_selected_signal(1),
                        ],width = {"size": 5}, style={'margin-right': '0px', 'margin-left': '0px'}),
                        dbc.Col([
                            create_report_selected_signal(2),
                        ],width = {"size": 5}, style={'margin-right': '0px', 'margin-left': '0px'}),
                    ], style = { 'margin-left': '20px'}),
                    html.Br(),
                    dmc.Divider(size="lg"),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            create_report_selected_signal(3),
                        ],width = {"size": 5}, style={'margin-right': '0px', 'margin-left': '0px'}),
                        dbc.Col([
                            create_report_selected_signal(4),
                        ],width = {"size": 5}, style={'margin-right': '0px', 'margin-left': '0px'}),
                    ], style = { 'margin-left': '20px'}),
                ])
    return graph_layout


def snapshot_30_graph_item(graph_index):

    get_layout = html.Div([
        dcc.Graph( 
            id = {
            'type': 'graph-pertrack',
            'index': graph_index}),
    ], style={'display':'None'})
    return  get_layout
   

##old

# children=[ 
#                     dmc.Container([
#                         html.Div([
#                           dbc.Row([
#                                 dbc.Col([
#                                     html.H3("Fault Report"),
#                                 ],  width={"size": 4, "offset": 5})
#                             ],
#                             align="end",
#                             className="pad-row",
#                             style= {
#                                 "marginTop": 20,
#                             }),  

#                             dmc.Divider(size="lg"),

#                             dmc.Space(h =20),

#                             dbc.Row([
#                                 dbc.Col([html.H6("Model")], width = {"size": 3}),
#                                 dbc.Col([html.H6("DTC")], width = {"size": 3}),
#                                 dbc.Col([html.H6("Count")], width = {"size": 3}),
#                                 dbc.Col([html.H6("Percentage")], width = {"size": 3}),
#                             ]),

#                             dbc.Row([
#                                 dbc.Col([html.Pre(id ="report-model")], width = {"size": 3}),
#                                 dbc.Col([html.Pre(id ="report-dtc")], width = {"size": 3}),
#                                 dbc.Col([html.Pre(id ="report-count")], width = {"size": 3}),
#                                 dbc.Col([html.Pre(id ="report-percentage")], width = {"size": 3}),

                                
#                             ]),

#                             dmc.Space(),

#                             html.H6("Selected Signals"),
                            
#                             dmc.Divider(size="lg"),

#                             dbc.Row([
#                                 dbc.Col([
#                                     html.Div([
#                                          dbc.Row([
#                                             dbc.Col([dmc.Text("Snapshot: ")]),
#                                             dbc.Col([html.Pre(id = 'snapshot-value-report-1')], width = {"size": 8}),
#                                         ],style = {'height':'20px'}),
#                                         dbc.Row([
#                                             dbc.Col([dmc.Text("DID: ")]),
#                                             dbc.Col([html.Pre(id = 'did-value-report-1' )], width = {"size": 8}),
#                                         ],style = {'height':'20px'}),
#                                         dbc.Row([
#                                             dbc.Col([dmc.Text("Signal: ")]),
#                                             dbc.Col([html.Pre(id = 'signal-value-report-1' , className="no-scrollbars")], width = {"size": 8}),
#                                         ],style = {'height':'20px'}),
#                                     ]),
                                    
#                                     dcc.Graph(id= 'graph-report-1', figure= dict(data = [], layout = []), style={'height': 200, "marginLeft": 10, "marginTop": 15 ,"marginBottom": 15}),

#                                     html.Div([
#                                         dash_table.DataTable(
#                                             id= 'table-report-1',
#                                             columns= [{'name': 'value', 'id': 'value'},
#                                                         {'name': '%', 'id': 'percentage'}],
#                                             data = [],
#                                             page_current=0,
#                                             page_size=2,
#                                             style_table={'overflowX': 'auto'},
#                                             style_header={
#                                                 'color': 'black',
#                                                 'fontWeight': 'bold'
#                                                 },
#                                             style_as_list_view=True,
#                                             ),
#                                     ]),  

#                                 ],  width = {"size": 5}, style={'margin-right': '20px', 'margin-left': '0px'}),
                            
#                                 dbc.Col([
#                                     html.Div([
#                                          dbc.Row([
#                                             dbc.Col([dmc.Text("Snapshot: ")]),
#                                             dbc.Col([html.Pre(id = 'snapshot-value-report-2')], width = {"size": 8}),
#                                         ],style = {'height':'20px'}),
#                                         dbc.Row([
#                                             dbc.Col([dmc.Text("DID: ")]),
#                                             dbc.Col([html.Pre(id = 'did-value-report-2' )], width = {"size": 8}),
#                                         ],style = {'height':'20px'}),
#                                         dbc.Row([
#                                             dbc.Col([dmc.Text("Signal: ")]),
#                                             dbc.Col([html.Pre(id = 'signal-value-report-2')], width = {"size": 8}),
#                                         ],style = {'height':'20px'}),
#                                     ]),
                                    
#                                     dcc.Graph(id= 'graph-report-2', figure= dict(data = [], layout = []),  style={'height': 200, "marginLeft": 10, "marginTop": 15 ,"marginBottom": 15}),

#                                     html.Div([
#                                         dash_table.DataTable(
#                                             id= 'table-report-2',
#                                             columns= [{'name': 'value', 'id': 'value'},
#                                                         {'name': '%', 'id': 'percentage'}],
#                                             data = [],
#                                             page_current=0,
#                                             page_size=2,
#                                             style_table={'overflowX': 'auto'},
#                                             style_header={
#                                                 'color': 'black',
#                                                 'fontWeight': 'bold'
#                                                 },
#                                             style_as_list_view=True,
#                                             ),
#                                     ]),  
#                                 ], width = {"size": 5}, style={'margin-right': '0px', 'margin-left': '0px'})
#                             ], style = { 'margin-left': '20px'}),

#                             html.Br(),

#                             dmc.Divider(size="lg"),

#                             html.Br(),

#                             dbc.Row([
#                                 dbc.Col([
#                                     html.Div([
#                                          dbc.Row([
#                                             dbc.Col([dmc.Text("Snapshot: ")]),
#                                             dbc.Col([html.Pre(id = 'snapshot-value-report-3')], width = {"size": 8}),
#                                         ],style = {'height':'20px'}),
#                                         dbc.Row([
#                                             dbc.Col([dmc.Text("DID: ")]),
#                                             dbc.Col([html.Pre(id = 'did-value-report-3' )], width = {"size": 8}),
#                                         ],style = {'height':'20px'}),
#                                         dbc.Row([
#                                             dbc.Col([dmc.Text("Signal: ")]),
#                                             dbc.Col([html.Pre(id = 'signal-value-report-3')], width = {"size": 8}),
#                                         ],style = {'height':'20px'}),
#                                     ]),
                                    
#                                     dcc.Graph(id= 'graph-report-3', figure= dict(data = [], layout = []),  style={'height': 200, "marginLeft": 10, "marginTop": 15 ,"marginBottom": 15}),

#                                     html.Div([
#                                         dash_table.DataTable(
#                                             id= 'table-report-3',
#                                             columns= [{'name': 'value', 'id': 'value'},
#                                                         {'name': '%', 'id': 'percentage'}],
#                                             data = [],
#                                             page_current=0,
#                                             page_size=2,
#                                             style_table={'overflowX': 'auto'},
#                                             style_header={
#                                                 'color': 'black',
#                                                 'fontWeight': 'bold'
#                                                 },
#                                             style_as_list_view=True,
#                                             ),
#                                     ]),  
#                                 ],  width = {"size": 5}, style={'margin-right': '20px', 'margin-left': '0px'}),
                            
#                                 dbc.Col([
#                                     html.Div([
#                                          dbc.Row([
#                                             dbc.Col([dmc.Text("Snapshot: ")]),
#                                             dbc.Col([html.Pre(id = 'snapshot-value-report-4')], width = {"size": 8}),
#                                         ],style = {'height':'20px'}),
#                                         dbc.Row([
#                                             dbc.Col([dmc.Text("DID: ")]),
#                                             dbc.Col([html.Pre(id = 'did-value-report-4' )], width = {"size": 8}),
#                                         ],style = {'height':'20px'}),
#                                         dbc.Row([
#                                             dbc.Col([dmc.Text("Signal: ")]),
#                                             dbc.Col([html.Pre(id = 'signal-value-report-4')], width = {"size": 8}),
#                                         ],style = {'height':'20px'}),
#                                     ]),
                                    
#                                     dcc.Graph(id= 'graph-report-4', figure= dict(data = [], layout = []), style={'height': 200, "marginLeft": 10, "marginTop": 15 ,"marginBottom": 15}),

#                                     html.Div([
#                                         dash_table.DataTable(
#                                             id= 'table-report-4',
#                                             columns= [{'name': 'value', 'id': 'value'},
#                                                         {'name': '%', 'id': 'percentage'}],
#                                             data = [],
#                                             page_current=0,
#                                             page_size=2,
#                                             style_table={'overflowX': 'auto'},
#                                             style_header={
#                                                 'color': 'black',
#                                                 'fontWeight': 'bold'
#                                                 },
#                                             style_as_list_view=True,
#                                             ),
#                                     ]),  
#                                 ], width = {"size": 5},
#                                     style={'margin-right': '0px', 
#                                             'margin-left': '0px'})
#                             ], style = { 'margin-left': '20px'}),

#                             html.Br(),

#                             html.Div([
#                                 html.H6('Filtered Cars and VINs'),
#                                 dbc.Row(
#                                     [
#                                         dbc.Col([
#                                             dbc.Card([
#                                                 dbc.CardBody([
#                                                     html.Pre(id='filterdcars-count',
#                                                     style = {"height": 20, 
#                                                             "overflow-y": "scroll"},
#                                                     className="no-scrollbars")
#                                                 ])
#                                             ] ,
#                                             ),
#                                         ],
#                                         width = {"size": 2},
#                                         ),

#                                         dbc.Col([
#                                             dbc.Card([
#                                                 dbc.CardBody([
#                                                     html.Pre(id='vin-list',
#                                                     style = {"height": 20, 
#                                                              "overflowY": "scroll"},
#                                                     className="no-scrollbars")
#                                                     ])
#                                                 ]),
#                                         ],
#                                         width = {"size": 9}),
#                                     ]),
#                             ]),
