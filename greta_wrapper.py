from copy import copy
from statistics import mean
import config
import pandas as pd
from ast import literal_eval
import numpy as np

def str_comma_to_float(x):
    if isinstance(x, str):
        return float(x.replace(',', '.'))
    return x

quantiles = [99, 97, 95, 93, 91, 90, 85, 75, 70, 50, 30, 10]

def fetch_and_summarise_data_by_type_country(type, subtype, country):
    try:
        data_input_ts = pd.read_csv(config.PATH_TO_TS_FILE(type, subtype, country), sep=';', skiprows=1)
        data_input_ts = data_input_ts.applymap(str_comma_to_float)

        data_input_stats = pd.read_csv(config.PATH_TO_STATS_FILE(type, subtype, country), sep=';')
        data_input_stats = data_input_stats[['Power_Potential_Weighted_GW', 'FLH_Mean_Masked',
                'FLH_Median_Masked', 'Energy_Potential_Weighted_TWh']]
        data_input_stats = data_input_stats.applymap(str_comma_to_float)

        return {'type': type, 'subtype': subtype, 'country': country,
            'FLH_q99': sum(data_input_ts['q99']), 'FLH_q97': sum(data_input_ts['q97']),
            'FLH_q95': sum(data_input_ts['q95']), 'FLH_q93': sum(data_input_ts['q93']),
            'FLH_q91': sum(data_input_ts['q91']), 'FLH_q90': sum(data_input_ts['q90']),
            'FLH_q85': sum(data_input_ts['q85']), 'FLH_q75': sum(data_input_ts['q75']),
            'FLH_q70': sum(data_input_ts['q70']), 'FLH_q50': sum(data_input_ts['q50']),
            'FLH_q30': sum(data_input_ts['q30']), 'FLH_q10': sum(data_input_ts['q10']),
            'Power_Potential_Weighted_GW': mean(data_input_stats['Power_Potential_Weighted_GW']),
            'Energy_Potential_By_FLH_Mean_Weighted':
                mean(data_input_stats['Energy_Potential_Weighted_TWh'])/
                    mean(data_input_stats['FLH_Mean_Masked'])*1000,
            'Energy_Potential_By_FLH_Median_Weighted':
                mean(data_input_stats['Energy_Potential_Weighted_TWh'])/
                    mean(data_input_stats['FLH_Median_Masked'])*1000}
    except FileNotFoundError:
        print(f'No data for: {type}, {subtype}, {country}, {config.YEAR}')
        return None
    except KeyError:
        print(f'Malformed data for: {type}, {subtype}, {country}, {config.YEAR}')
        print(data_input_ts.head())

def fetch_and_summarise_data():
    data = pd.DataFrame(columns=['type', 'subtype', 'country', 'FLH_q99', 'FLH_q97', 'FLH_q95',
        'FLH_q93', 'FLH_q91', 'FLH_q90', 'FLH_q85', 'FLH_q75', 'FLH_q70', 'FLH_q50', 'FLH_q30',
        'FLH_q10', 'Power_Potential_Weighted_GW', 'Energy_Potential_By_FLH_Mean_Weighted',
        'Energy_Potential_By_FLH_Median_Weighted'])

    for type in config.TYPES:
        for subtype in config.SUBTYPES[type]:
            for country in config.COUNTRIES:
                data = data.append(fetch_and_summarise_data_by_type_country(type, subtype, country), ignore_index=True)

    return data

def generate_class_irnw(data):
    data = data.copy()
    data = data[['country', 'type', 'Power_Potential_Weighted_GW']]
    data = data.drop_duplicates()
    data.replace(config.COUNTRIES_TO_ABBR, inplace = True)
    data_pivoted = data.pivot(index = 'country', columns = 'type', values = 'Power_Potential_Weighted_GW')
    data_pivoted.rename(columns = {'OpenFieldPV': 'OpenPV', 'RoofTopPV': 'RoofPV'}, inplace = True)
    data_pivoted.index.names = ['Site']
    data_pivoted.to_excel('class_irnw.xlsx', index = True)
    print('Results saved to: class_irnw.xlsx')

def generate_process_irnw_flh(data):
    data = data.copy()
    data = data[['country', 'type', 'subtype', 'FLH_q99', 'FLH_q97', 'FLH_q95',
       'FLH_q93', 'FLH_q91', 'FLH_q90', 'FLH_q85', 'FLH_q75', 'FLH_q70',
       'FLH_q50', 'FLH_q30', 'FLH_q10']]
    data.replace(config.COUNTRIES_TO_ABBR, inplace = True)
    data.replace(config.TYPES_TO_CLASS, inplace = True)

    columns = []
    for t in config.TYPES_CLASS:
        for q in ['q99', 'q97', 'q95', 'q93', 'q91', 'q90', 'q85', 'q75', 'q70', 'q50', 'q30', 'q10']:
            columns.append(t + '_' + q)

    columns = ['year', 'ID-year'] + columns
    writer = pd.ExcelWriter('process_irnw_flh.xlsx', engine='xlsxwriter')
    data_all = data.drop(columns=['country'])
    data_all = data_all.groupby(by = ['type', 'subtype']).sum().reset_index()
    result = pd.DataFrame(columns=columns)
    for year in config.YEARS:
        row = year
        for t in config.TYPES_CLASS:
            for q in ['q99', 'q97', 'q95', 'q93', 'q91', 'q90', 'q85', 'q75', 'q70', 'q50', 'q30', 'q10']:
                value = (data_all[data_all['type'] == t])[['subtype', 'FLH_' + q]]
                try:
                    subtype = config.YEAR_TO_SUBTYPE[t][year[1]]
                    row = row + [list(value[value['subtype'] == subtype]['FLH_' + q])[0]]
                except:
                    row = row + [np.NaN]
        result = result.append(pd.Series(row, index=columns), ignore_index=True)
    result.to_excel(writer, sheet_name = 'ALL', index = False)

    for country in config.ABBR:
        result = pd.DataFrame(columns=columns)
        for year in config.YEARS:
            row = year
            for t in config.TYPES_CLASS:
                for q in ['q99', 'q97', 'q95', 'q93', 'q91', 'q90', 'q85', 'q75', 'q70', 'q50', 'q30', 'q10']:
                    value = (data[(data['type'] == t) & (data['country'] == country)])[['subtype', 'FLH_' + q]]
                    try:
                        subtype = config.YEAR_TO_SUBTYPE[t][year[1]]
                        row = row + [list(value[value['subtype'] == subtype]['FLH_' + q])[0]]
                    except:
                        row = row + [np.NaN]
            result = result.append(pd.Series(row, index=columns), ignore_index=True)
        result.to_excel(writer, sheet_name = country, index = False)
    writer.save()
    print('Results saved to: process_irnw_flh.xlsx')

if __name__ == '__main__':
    print('Gathering and processing data')

    data = fetch_and_summarise_data()

    writer = pd.ExcelWriter('greta_summary.xlsx', engine='xlsxwriter')
    for type in config.TYPES:
        data_by_type = (data[data['type'] == type]).copy()
        data_by_type.drop(columns=['type'], inplace=True)
        data_by_type.sort_values(by=['country', 'subtype'], inplace=True)

        if len(config.SUBTYPES[type]) <= 1:
            data_by_type.drop(columns=['subtype'], inplace=True)
        elif type in ('WindOn', 'WindOff'):
            data_by_type.rename(columns={'subtype': 'height'}, inplace=True)

        print(f'Saving data for {type}')
        data_by_type.to_excel(writer, sheet_name = type, index = False)

    writer.save()
    print('Results saved to: greta_summary.xlsx')

    generate_class_irnw(data)
    generate_process_irnw_flh(data)