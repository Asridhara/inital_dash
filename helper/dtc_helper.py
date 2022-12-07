
import pandas as pd
import re

def dropdown_list_for_filtering(df):

    """ 
    This function creates the dropdown menus of the snaphot, did and signal contained in the data file
    
    Input@df: A input raw dataframe of DTC from MyQ
    type@df: Pandas dataframe

    Output: A dictinory to be used dropdown menu to filter singal for data visualization
    type: A nested dictonary

       {'407168': -> #DTC
            {'20': -> #snapshot
                {'0330': ->#DID
                    ['Svt_ActAng_A'], -># list of signals
            '30': ,
            '40': }}}
    """ 
    list_of_dtcs = df.columns.str.extract(r'\d+/(\w+)/(\d+)/(\w+)/(\w+)').dropna()[0].unique().tolist()
    nested_dropdown_data = {}
    nested_dropdown_data = nested_dropdown_data.fromkeys(list_of_dtcs )

    for i, dtc in enumerate(nested_dropdown_data.keys()):

        single_dtc_df = df[df.columns[df.columns.str.contains(dtc)==True]]
        single_dtc_df = single_dtc_df.dropna(thresh = single_dtc_df.shape[0]*0.7,how='all', axis=0)
        single_dtc_df = single_dtc_df.dropna(thresh = single_dtc_df.shape[0]*0.7,how='all', axis=1)

        list_of_snapshot_in_dtc =  single_dtc_df.columns.str.extractall(rf'\d+/{dtc}/(\d+)/\w+/\w+')[0].unique().tolist()

        nested_dropdown_data[dtc] = {}
        nested_dropdown_data[dtc] = nested_dropdown_data[dtc].fromkeys(list_of_snapshot_in_dtc)

        for snapshot in list_of_snapshot_in_dtc:
            list_of_did_in_dtc = single_dtc_df.columns.str.extract(rf'\d+/{dtc}/{snapshot}/(\w+)/\w+').dropna()[0].unique().tolist()

            nested_dropdown_data[dtc][snapshot] = {}
            nested_dropdown_data[dtc][snapshot] = nested_dropdown_data[dtc][snapshot].fromkeys(list_of_did_in_dtc)
            for did in list_of_did_in_dtc:
                if snapshot != '30':
                    nested_dropdown_data[dtc][snapshot][did] = single_dtc_df.columns.str.extractall(rf'\d+/{dtc}/{snapshot}/{did}/(\w+)')[0].unique().tolist()

                else:
                    signal_30_df = single_dtc_df.columns.str.extractall(rf'\d+/{dtc}/{snapshot}/{did}/(\w+)')[0].str.extract(r'(Tr\d+)_(S\d+)_(\w+)').groupby([0,2]).count().reset_index().dropna()
                    signal_30_df ['combine'] = signal_30_df[[0,2]].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
                    nested_dropdown_data[dtc][snapshot][did] = signal_30_df ['combine'].tolist()
    
    return nested_dropdown_data


def count_dtc_in_df(df):

    list_of_dtcs = df.columns.str.extract(r'\d+/(\w+)/(\d+)/(\w+)/(\w+)').dropna()[0].unique().tolist()
    count_df = pd.DataFrame(columns=['DTC', 'Count', 'Unique', 'Cars'])

    for i, dtc in enumerate(list_of_dtcs):

        single_dtc_df = df[df.columns[df.columns.str.contains(dtc)==True]]
        count_single_dtc = single_dtc_df.dropna(thresh = single_dtc_df.shape[0]*0.7, how='all', axis=0).shape[0]
        cars_id = list(df.loc[single_dtc_df.dropna(thresh = single_dtc_df.shape[0]*0.7,how='all', axis=0).index].vin.unique())
        unique_count_single_dtc = len(cars_id)

        #unique_count_single_dtc = df.loc[single_dtc_df.dropna(thresh = single_dtc_df.shape[0]*0.7,how='all',axis=0).index].vin.nunique()
        count_df.loc[i,'DTC'], count_df.loc[i,'Count'], count_df.loc[i,'Unique'], count_df.loc[i,'Cars']=  dtc, count_single_dtc, unique_count_single_dtc, cars_id

    total = count_df['Count'].sum()
    count_df['Percentage'] = count_df.loc[:,'Count'].apply(lambda x: x/total*100)

    return count_df


def get_did_information(df):

    did_information_modified = df.copy()
    did_info_index = did_information_modified[~did_information_modified['Compare Value'].str.contains(r'(=\d)x(\w+)')]['Compare Value'].str.replace(r'[\\=><]','').index
    did_information_modified.loc[did_info_index,'Compare Value'] = pd.to_numeric(did_information_modified[~did_information_modified['Compare Value'].str.contains(r'(=\d)x(\w+)')]['Compare Value'].str.replace(r'[\\=><]',''), downcast="integer", errors='coerce')
    did_information_modified['Parameter Name'] = did_information_modified['Parameter Name'].apply(lambda x:'_'.join([i for i in re.split('(?<![0-9])[\_ /\[ \]\()-](?![0-9])', x) if i])).str.lower()
    return did_information_modified


