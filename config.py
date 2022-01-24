### Basic config

# Countries for which the merging is performed and data saved

COUNTRIES = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Czechia', 'Denmark', 'Estonia', 'Finland',
    'France', 'Germany', 'Greece', 'Ireland', 'Hungary', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
    'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Switzerland',
    'Sweden', 'United Kingdom']


TYPES = ['WindOn', 'WindOff', 'RoofTopPV', 'OpenFieldPV']

SUBTYPES = {'WindOn': [80, 90, 100, 110, 120],
            'WindOff': [100, 120, 130, 150],
            'RoofTopPV': [0],
            'OpenFieldPV': [0]}

YEARS = [2019]

DEFAULT_YEAR = 2019

def PATH_TO_FILE(type, subtype, country, year = DEFAULT_YEAR):
    country = country.replace(" ", "")
    return f'..\\Files {country}\\Renewable Energy\\Regional Analysis\\{country}_level0\\{country}_level0_{type}_{subtype}_TS_{year}.csv'