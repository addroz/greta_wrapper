from statistics import mean
import config
import pandas as pd

def str_comma_to_float(x):
    if isinstance(x, str):
        return float(x.replace(',', '.'))
    return x

def fetch_and_summarise_data_by_type_country(type, subtype, country):
    try:
        data_input_ts = pd.read_csv(config.PATH_TO_TS_FILE(type, subtype, country), sep=';', skiprows=1)
        data_input_ts = data_input_ts.applymap(str_comma_to_float)

        data_input_stats = pd.read_csv(config.PATH_TO_STATS_FILE(type, subtype, country), sep=';')
        data_input_stats = data_input_stats[['Power_Potential_GW', 'Power_Potential_Weighted_GW']]
        data_input_stats = data_input_stats.applymap(str_comma_to_float)

        return {'type': type, 'subtype': subtype, 'country': country,
            'FLH_q90': sum(data_input_ts['q90']), 'FLH_q70': sum(data_input_ts['q70']),
            'FLH_q50': sum(data_input_ts['q50']), 'FLH_q30': sum(data_input_ts['q30']),
            'Power_Potential_GW': mean(data_input_stats['Power_Potential_GW']),
            'Power_Potential_Weighted_GW': mean(data_input_stats['Power_Potential_Weighted_GW'])}
    except FileNotFoundError:
        print(f'No data for: {type}, {subtype}, {country}, {config.YEAR}')
        return None
    except KeyError:
        print(f'Malformed data for: {type}, {subtype}, {country}, {config.YEAR}')
        print(data_input_ts.head())

def fetch_and_summarise_data():
    data = pd.DataFrame(columns=['type', 'subtype', 'country', 'FLH_q90', 'FLH_q70', 'FLH_q50',
        'FLH_q30', 'Power_Potential_GW', 'Power_Potential_Weighted_GW'])

    for type in config.TYPES:
        for subtype in config.SUBTYPES[type]:
            for country in config.COUNTRIES:
                data = data.append(fetch_and_summarise_data_by_type_country(type, subtype, country), ignore_index=True)

    return data

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

    print('Results saved to: greta_summary.xlsx')
    writer.save()

