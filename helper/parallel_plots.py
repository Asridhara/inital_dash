
import re
import os
import json


import numpy as np
import pandas as pd

from dash import Input, Output, html, dcc
from jupyter_dash import JupyterDash
import plotly.express as px
import plotly.graph_objects as go
import dash_mantine_components as dmc
import dash_bootstrap_components  as dbc

from natsort import natsorted, index_natsorted , order_by_index

def rotate_list(list):
    list_length = len(list)
    rearranged_list = list[list_length-1:]+ list[:list_length-1]
    return rearranged_list 


def plot_label(iter_number, sample, raster):

    if (iter_number % 5 == 0):
        time_in_sec = round((39-iter_number)* raster, 2)
        label_value =  ' -{} s'.format(time_in_sec)

    elif sample == 'S40':
    
        label_value = '{} s'.format(0)
    else:
        label_value = ' '

    return label_value
       
def create_lookup_table_stringdf(df):
    sorted_list = rotate_list(natsorted(np.unique(df)))
    lookup_dict =  {value: i for i, value in enumerate(sorted_list, start=0)}
    return lookup_dict

def modify_stringdf(df):
    modfied_df = pd.DataFrame(columns=df.columns)
    lookup_table = create_lookup_table_stringdf(df)

    for col in df.keys():
        modfied_df[col] = df[col].apply(lambda x: lookup_table[x])
        
    modfied_df.columns = modfied_df.columns.str.extract('\d+/\w+/\d+/\w+/Tr\d+_(S\d+)_\w+')[0]
    return modfied_df


def tick_text_stringdf(column_name, lookupd_table, length ):
    if column_name =='S01' :
        text_name =  [' < '.join([i for i in re.split('(?<![0-9])[ ](?<![a-z])', x) if i]) for x in list(lookupd_table.keys()) ]
    else:
        text_name  = ['']*length
    return text_name 


def parallelplot_dimension_stringdf(df, raster):
    parallelplot_df = modify_stringdf(df)
    lookup_table = create_lookup_table_stringdf(df)
    length =  len(natsorted(np.unique(df)))

    column_list = []

    for i, column in enumerate(parallelplot_df.keys()):
        column_dict = dict(
            range=(0,length+1),
            values= list(parallelplot_df[column]),
            tickvals = list(range(0,length+1)),
            ticktext = tick_text_stringdf(column, lookup_table, length),
            label = plot_label(i, column,  raster),
            multiselect= True,
            )
        column_list.append(column_dict)
    return column_list
       

def modify_floatdf(df):
    modfied_df = df.copy()
    modfied_df.columns = modfied_df.columns.str.extract('\d+/\w+/\d+/\w+/Tr\d+_(S\d+)_\w+')[0]
    return modfied_df



def tick_text_floatdf(column_name, lookupd_table, length):
    if column_name =='S01' :
        text_name =  list(lookupd_table.values()) 
    else:
        text_name  = ['']*length
    return text_name 

def tick_text_floatdf_timeseries(column_name, df):
    upper_range = int(df.to_numpy().max()+5)

    if column_name =='S01' or column_name =='S1':
        text_name = [str(i) for i in list(range(0,upper_range,10))]
    else:
        text_name = ['']*len(list(range(0, upper_range,10)))
    return text_name


def create_lookup_table_floatdf(did_df):

    try:
        if did_df['No. of bits'].unique()[0]== 1:
            unit_value = did_df['Compare Value'].unique().tolist()
            if pd.isna(unit_value[0])==True or np.isnan(unit_value[0])==True:
                lookup_dict = {}
            else:
                lookup_dict = dict(did_df[['Compare Value', 'Unit']].values)
        else:
            lookup_dict = dict(did_df[['Compare Value', 'Unit']].values)
            
    except :
        lookup_dict = {}

    return lookup_dict



def parallelplot_dimension_floatdf(df,did_df, raster):
    parallelplot_df = modify_floatdf(df)
    lookup_table = create_lookup_table_floatdf(did_df)
    length =  len(lookup_table.keys())
    upper_range = parallelplot_df.to_numpy().max()

    column_list = []

    for i, column in enumerate(parallelplot_df.keys()):
        column_dict = dict(
            range= [0, upper_range],
            values= list(parallelplot_df[column]),
            tickvals = list(lookup_table.keys()),
            ticktext = tick_text_floatdf(column, lookup_table, length),
            label = plot_label(i, column,  raster),
            multiselect= True,
            )
        column_list.append(column_dict)
    return column_list
       

def parallelplot_dimension_floatdf_timeseris(df, raster):
    parallelplot_df = modify_floatdf(df)
    upper_range  = int(parallelplot_df.to_numpy().max())+3
    column_list = []

    for i, column in enumerate(parallelplot_df.keys()):
        column_dict = dict(
            range= [0, upper_range],
            values= list(parallelplot_df[column]),
            tickvals = list(range(0,upper_range,10)),
            ticktext = tick_text_floatdf_timeseries(column, parallelplot_df),
            label = plot_label(i, column,  raster),
            multiselect= True,
            )
        column_list.append(column_dict)
    return column_list

def histogram_xlabel(label):
    if label == None:
        label = ' '
    else:
        label = label
    return label





def plot_count_histogram(df):
    fig_histogram = go.Figure()
    fig_histogram = fig_histogram.add_trace(go.Bar(x = df['DTC'],
                        y = df['Count']
                            )
                        )
    fig_histogram.update_traces(customdata = np.stack(
                            (df['DTC'],
                            df['Percentage'],
                            df['Count'],
                            df['Unique']), axis= -1))
                            
    fig_histogram.update_traces(marker_color='rgb(255, 140,0)', 
                    hovertemplate=('<b>Diagnostic Trouble Code:%{x}<br>'+
                                    'Total Cars:%{y}<br>'+
                                    'Unique cars:%{customdata[2]}<br>'+
                                    'Percentage of DTC:%{customdata[1]:.2f}%<br><br> <extra></extra>')
                    )
    fig_histogram.update_layout(xaxis=dict(
                        title = 'DTC',
                        color = 'white', 
                        showgrid=False,
                        zeroline=False),
                    yaxis=dict(showgrid=False ,
                        title = 'Counts',
                        color = 'white'),
                    clickmode = 'event+select',
                    title = dict(text = 'Histogram of DTC counts',
                        font = dict(color = 'white', size = 18)),
                    legend = dict(bgcolor  = 'black'),  
                    plot_bgcolor='#0a0a0a',
                    paper_bgcolor = '#0a0a0a' ,
                    hovermode = 'x',
                    height = 500, 
                    autosize=False,
                    
                )
    return fig_histogram



def plot_px_histogram(df, signal_name, plt_title = None, xlabel = None):
    fig_px_histogram = px.histogram(x=df[signal_name],
                    marginal='violin',
                    histnorm= 'percent',
                    nbins = 100,
                    title= plt_title,
                    labels = {'x' : histogram_xlabel(xlabel)}
                )
    fig_px_histogram.update_traces(customdata = np.stack(
                            df.index))
    fig_px_histogram.update_layout(xaxis=dict(color = 'white', 
                        title = dict(font = dict(size = 10)),
                        tickfont = dict(size = 8),
                        showgrid=False,
                        zeroline=False),
                    yaxis=dict(showgrid=False ,
                        title = dict(font = dict(size = 10)),
                        tickfont = dict(size = 8),
                        color = 'white'),
                    clickmode = 'event+select',
                    dragmode="select",
                    title = dict(
                        pad = dict(t = 20),
                        font = dict(color = 'white', size = 14)),
                    legend = dict(bgcolor  = 'black'),  
                    plot_bgcolor='#0a0a0a',
                    paper_bgcolor = '#0a0a0a' ,
                    hovermode = 'x',  
                    margin = dict(
                        b = 20, 
                        t = 25, 
                        l = 15,
                        r = 10
                    ),
                )
    return fig_px_histogram.to_dict()




def plot_px_histogram_catogeries(df, signal_name, plot_title = None):
    fig_px_histogram_catogeries = px.histogram(x=df['Unit'],
                    y = df[signal_name],
                    marginal='violin',
                    histnorm= 'percent',
                    nbins = 100,
                    title= plot_title,
                    labels = {'x' : 'Catagories'}
                )
    fig_px_histogram_catogeries.update_traces(customdata = np.stack(
                             df.index))
    fig_px_histogram_catogeries.update_layout(xaxis=dict(color = 'white', 
                        title = dict(font = dict(size = 10)),
                        tickfont = dict(size = 8),
                        showgrid=False,
                        zeroline=False),
                    yaxis=dict(showgrid=False ,
                        title = dict(font = dict(size = 10)),
                        tickfont = dict(size = 8),
                        color = 'white'),
                    clickmode = 'event+select',
                    dragmode="select",
                    title = dict(
                        pad = dict( t = 20),
                        font = dict(color = 'white', size = 12)),
                    legend = dict(bgcolor  = 'black'),  
                    plot_bgcolor='#0a0a0a',
                    paper_bgcolor = '#0a0a0a' ,
                    hovermode = 'x',  
                    margin = dict( 
                        b = 20, 
                        t = 25, 
                        l = 20,
                        r = 20
                    ),
                )
    return fig_px_histogram_catogeries.to_dict()


def plot_parallel_stringdf(df, raster, timeseries_signal_name):
    fig_parallel_stringdf = go.Figure(data=
                    go.Parcoords(
                        line = dict(
                            color = df.index,
                            colorscale = [[0,'red'],[0.5,'lightseagreen'],[1,'yellow']],
                            cauto = True,
                            showscale = False,
                            colorbar = dict(
                                tickfont = dict(size = 1)
                                )
                            ),
                        labelfont = dict(color = '#e5e4e2', size = 9),
                        labelside = 'bottom',
                        tickfont = dict(color = '#e5e4e2',size = 10),
                        rangefont = dict(color ='#e5e4e2'),
                        dimensions = parallelplot_dimension_stringdf(df, raster),
                        )
                    )
    #fig_parallel_stringdf.update_traces(customdata = np.stack(
                            # df.index))
    fig_parallel_stringdf.update_layout(title = dict(
                            font = dict(color = '#e5e4e2'), 
                            text = timeseries_signal_name),
                    legend = dict(bgcolor  = 'white'),  
                    plot_bgcolor='#353839',
                    paper_bgcolor = '#0a0a0a' ,
                    hovermode = 'x',
                    height = 240,  
                    clickmode = 'event+select',
                    margin = dict( 
                        b = 40, 
                        t = 20, 
                        l = 120,
                        r = 20,
                        ),
                    # shapes=[
                    #     {   
                    #         'type': 'line',
                    #         'x0': 1,
                    #         'y0': 0, # use absolute value or variable here
                    #         'x1': 1,
                    #         'y1': 1, # ditto
                    #         'visible': True, 
                    #         'line': {
                    #             'color': 'red',
                    #             'width': 5,
                    #             'dash': 'dash',
                    #         },
                    #     },],
                    )
    return fig_parallel_stringdf.to_dict()

def plot_parallel_floatdf(df,did_df, raster, timeseries_signal_name):
    fig_parallel_floatdf = go.Figure(data=
                    go.Parcoords(
                        line = dict(
                            color = df.index,
                            colorscale = [[0,'red'],[0.5,'lightseagreen'],[1,'yellow']],
                            cauto = True,
                            showscale = False,
                            colorbar = dict(
                                tickfont = dict(size = 1)
                                )
                            ),
                        labelfont = dict(color = '#e5e4e2', size = 9),
                        labelside = 'bottom',
                        tickfont = dict(color = '#e5e4e2',size = 10),
                        rangefont = dict(color ='#e5e4e2'),
                        dimensions = parallelplot_dimension_floatdf(df, did_df, raster),
                        )
                    )
    #fig_parallel_floatdf.update_traces(customdata = np.stack(
                            # df.index))
    fig_parallel_floatdf.update_layout(title = dict(
                            font = dict(color = '#e5e4e2'), 
                            text = timeseries_signal_name),
                    legend = dict(bgcolor  = 'white'),  
                    plot_bgcolor='#353839',
                    paper_bgcolor = '#0a0a0a' ,
                    hovermode = 'x',
                    height = 240,  
                    clickmode = 'select',
                    margin = dict( 
                        b = 40, 
                        t = 60, 
                        l = 20,
                        r = 20,
                        ),
                    # shapes=[
                    #     {   
                    #         'type': 'line',
                    #         'x0': 1,
                    #         'y0': 0, # use absolute value or variable here
                    #         'x1': 1,
                    #         'y1': 1, # ditto
                    #         'visible': True, 
                    #         'line': {
                    #             'color': 'red',
                    #             'width': 5,
                    #             'dash': 'dash',
                    #         },
                    #     },],
                    )
    return fig_parallel_floatdf.to_dict()

def plot_parallel_floatdf_timeseries(df, raster, timeseries_signal_name):
    fig_parallel_floatdf_timeseries = go.Figure(data=
                    go.Parcoords(
                        line = dict(
                            color = df.index,
                            colorscale = [[0,'red'],[0.5,'lightseagreen'],[1,'yellow']],
                            cauto = True,
                            showscale = False,
                            colorbar = dict(
                                tickfont = dict(size = 1)
                                )
                            ),
                        labelfont = dict(color = '#e5e4e2', size = 9),
                        labelside = 'bottom',
                        tickfont = dict(color = '#e5e4e2',size = 10),
                        rangefont = dict(color ='#e5e4e2'),
                        dimensions = parallelplot_dimension_floatdf_timeseris(df, raster),
                        )
                    )
    #fig_parallel_floatdf_timeseries.update_traces(customdata = np.stack(
                        # df.index))
    fig_parallel_floatdf_timeseries.update_layout(title = dict(
                            font = dict(color = '#e5e4e2'), 
                            text = timeseries_signal_name),
                    legend = dict(bgcolor  = 'white'),  
                    plot_bgcolor='#353839',
                    paper_bgcolor = '#0a0a0a' ,
                    hovermode = 'x',
                    height = 240,  
                    clickmode = 'select',
                    margin = dict( 
                        b = 40, 
                        t = 60, 
                        l = 40,
                        r = 10,
                        ),
                    # shapes=[
                    #     {   
                    #         'type': 'line',
                    #         'x0': 1,
                    #         'y0': 0, # use absolute value or variable here
                    #         'x1': 1,
                    #         'y1': 1, # ditto
                    #         'visible': True, 
                    #         'line': {
                    #             'color': 'red',
                    #             'width': 5,
                    #             'dash': 'dash',
                    #         },
                    #     },],
                    )
    return fig_parallel_floatdf_timeseries.to_dict()


def plot_snapshots_2040(df,did_information, did_value,signal):
    plotting_df = df.copy() 
    did_information_df = did_information.copy()
    plotting_df = plotting_df.rename(columns = {plotting_df.columns[0]: signal})
       
    if plotting_df[signal].dtype == float or plotting_df[signal].dtype == int:
        lower_case_signal_name = signal.lower()
        did_signal_df = did_information_df[(did_information_df['Parameter Name'].str.contains(lower_case_signal_name)) & (did_information_df['Identifier']== did_value)].copy()
        
        try:
            if did_signal_df.shape[0] > 1:
                single_compare_value = did_signal_df['Compare Value'].unique().tolist()

                if pd.isna(single_compare_value[0]) == True or np.isnan(single_compare_value[0]) == True:

                    plot_title = did_signal_df['DID Name'].unique()[0] 
                    plt_figure =  plot_px_histogram(plotting_df,signal, plot_title, 'Catagories')

                
                else: 
                    new_plot_df = plotting_df.copy()
                    left_did_df = did_signal_df[['Compare Value', 'Unit']]
                    convert_float_to_string_catogeries = dict(zip(left_did_df['Compare Value'], left_did_df['Unit']))
                    new_plot_df[signal] = new_plot_df[signal].apply(lambda x: convert_float_to_string_catogeries[x])
                    plot_title = did_signal_df['DID Name'].unique()[0] 
                    plt_figure =  plot_px_histogram(new_plot_df,signal, plot_title, 'Catagories')

            else:
                unit_value = did_signal_df['Unit'].values[0]
                if unit_value != 'NaN' or unit_value != '':
                    plot_units = unit_value
                    plot_title = did_signal_df['DID Name'].values[0]
                else:
                    plot_units = 'No units'
                    plot_title = did_signal_df['DID Name'].values[0]

                plt_figure = plot_px_histogram(plotting_df,signal, plot_title,plot_units)
             
        except IndexError:
            plt_figure = plot_px_histogram(plotting_df, signal)

          
    else: 
        lower_case_signal_name = signal.lower()
        did_signal_df = did_information_df[(did_information_df['Parameter Name'].str.contains(lower_case_signal_name)) & (did_information_df['Identifier']== did_value)]
        plot_title = did_signal_df['DID Name'].unique()[0]
        plotting_df[signal] = plotting_df[signal].apply(lambda x:' < '.join([i for i in re.split('(?<![0-9])[ ](?<![a-z])', str(x)) if i]))
        plt_figure = plot_px_histogram(plotting_df, signal, plot_title, 'Catagories')
        
    return plt_figure
  
def plot_snapshots_30(df,did_information, dtc_value, did_value,signal, filter_index):
    snapshot_value = '30'
    try:
        track, timeseries_signal = re.split('(?<=\w\d)[_](?=[0-9A-Za-z])', signal)
    except :
        string_split = re.split('(?<=\w\d)[_](?=[0-9A-Za-z])', signal)
        track = string_split[0]
        timeseries_signal = '_'.join(string_split[1:])


    plot_signal_df =  df[df.columns[(df.columns.str.contains(rf'\d+/{dtc_value}/{snapshot_value}/{did_value}/(\w+)'))]].dropna()
    frequency_df = plot_signal_df.loc[:,plot_signal_df.columns.str.contains('Sample_rate_Ts')== True].mode()
    sample_rate = list(frequency_df.values[0])[0]/1000
    total_plotting_df = plot_signal_df.loc[:,plot_signal_df.columns.str.contains(timeseries_signal)== True]

    if len(filter_index) <= 1 or None:
        plotting_df = total_plotting_df.copy()
    else:
        plotting_df = total_plotting_df.filter(items=filter_index, axis = 0)

    if plotting_df.iloc[1,:].dtype == float or plotting_df.iloc[1,:].dtype == int:
        
        if len(np.unique(plotting_df)) > 16:
            plt_fig_30 = plot_parallel_floatdf_timeseries(plotting_df[natsorted(plotting_df.columns)],sample_rate, signal)
           
        else:
            lower_timeseries_signal= timeseries_signal.lower()
            did_signal_df = did_information[(did_information['Parameter Name'].str.contains(lower_timeseries_signal)) & (did_information['Identifier']== did_value)]
            plt_fig_30 = plot_parallel_floatdf(plotting_df[natsorted(plotting_df.columns)], did_signal_df, sample_rate, signal)
        
    else:
        plt_fig_30 = plot_parallel_stringdf(plotting_df[natsorted(plotting_df.columns)], sample_rate, signal)
       

    return plt_fig_30, plotting_df.index


