### Basic config

# Countries for which the merging is performed and data saved

COUNTRIES = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Czechia', 'Denmark', 'Estonia', 'Finland',
    'France', 'Germany', 'Greece', 'Ireland', 'Hungary', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
    'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Switzerland',
    'Sweden', 'United Kingdom']


TYPES = ['WindOn', 'WindOff', 'RoofTopPV', 'OpenFieldPV']

SUBTYPES = {'WindOn': [80, 90, 100, 110, 120, 130, 140, 150],
            'WindOff': [90, 100, 120, 130, 150, 160, 170],
            'RoofTopPV': [0],
            'OpenFieldPV': [0]}

YEAR = 2019

def PATH_TO_TS_FILE(type, subtype, country, year = YEAR):
    country = country.replace(" ", "")
    return f'..\\Files {country}\\Renewable Energy\\Regional Analysis\\{country}_level0\\{country}_level0_{type}_{subtype}_TS_{year}.csv'


def PATH_TO_STATS_FILE(type, subtype, country, year = YEAR):
    country = country.replace(" ", "")
    return f'..\\Files {country}\\Renewable Energy\\Regional Analysis\\{country}_level0\\{country}_level0_{type}_{subtype}_Region_stats_{year}.csv'