### Basic config

# Countries for which the merging is performed and data saved

COUNTRIES = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Czechia', 'Denmark', 'Estonia', 'Finland',
    'France', 'Germany', 'Greece', 'Ireland', 'Hungary', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
    'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Switzerland',
    'Sweden', 'United Kingdom']

COUNTRIES_TO_ABBR = {'Austria':'AT', 'Belgium':'BE', 'Bulgaria':'BG', 'Croatia':'HR', 'Czechia':'CZ',
    'Denmark':'DK', 'Estonia':'EE', 'Finland':'FI', 'France':'FR', 'Germany':'DE', 'Greece':'EL',
    'Ireland':'IE', 'Hungary':'HU', 'Italy':'IT', 'Latvia':'LV', 'Lithuania':'LT', 'Luxembourg':'LU',
    'Malta':'MT', 'Netherlands':'NL', 'Norway':'NO', 'Poland':'PL', 'Portugal':'PT', 'Romania':'RO',
    'Slovakia':'SK', 'Slovenia':'SI', 'Spain':'ES', 'Sweden':'SE', 'United Kingdom':'UK',
    'Switzerland': 'CH'}

ABBR = [COUNTRIES_TO_ABBR[country] for country in COUNTRIES]

TYPES = ['RoofTopPV', 'OpenFieldPV', 'WindOn', 'WindOff']

TYPES_CLASS = ['RoofPV', 'OpenPV', 'WindOn', 'WindOff']

TYPES_TO_CLASS = {'RoofTopPV': 'RoofPV', 'OpenFieldPV': 'OpenPV', 'WindOn': 'WindOn', 'WindOff': 'WindOff'}

YEARS = [[2020, 1960],
        [2020, 1965],
        [2020, 1970],
        [2020, 1975],
        [2020, 1980],
        [2020, 1985],
        [2020, 1990],
        [2020, 1995],
        [2020, 2000],
        [2020, 2005],
        [2020, 2010],
        [2020, 2015],
        [2020, 2020],
        [2025, 2025],
        [2030, 2030],
        [2035, 2035],
        [2040, 2040],
        [2045, 2045],
        [2050, 2050],
        [2055, 2055],
        [2060, 2060],
        [2065, 2065],
        [2070, 2070],
        [2075, 2075],
        [2080, 2080],
        [2085, 2085],
        [2090, 2090],
        [2095, 2095],
        [2100, 2100]]

YEAR_TO_SUBTYPE = {'WindOn': {2000: 80, 2005: 80, 2010: 80, 2015: 80, 2020: 90, 2025: 100, 2030: 110, 2035: 120,
                    2040: 130, 2045: 140, 2050: 150, 2055: 150, 2060: 150, 2065: 150, 2070: 150, 2075: 150,
                    2080: 150, 2085: 150, 2090: 150, 2095: 150, 2100: 150},
                    'WindOff': {2000: 100, 2005: 100, 2010: 100, 2015: 110, 2020: 110, 2025: 120, 2030: 130, 2035: 140,
                    2040: 150, 2045: 160, 2050: 170, 2055: 170, 2060: 170, 2065: 170, 2070: 170, 2075: 170,
                    2080: 170, 2085: 170, 2090: 170, 2095: 170, 2100: 170},
                    'RoofPV': {2000: 0, 2005: 0, 2010: 0, 2015: 0, 2020: 0, 2025: 0, 2030: 0, 2035: 0,
                    2040: 0, 2045: 0, 2050: 0, 2055: 0, 2060: 0, 2065: 0, 2070: 0, 2075: 0,
                    2080: 0, 2085: 0, 2090: 0, 2095: 0, 2100: 0},
                    'OpenPV': {2000: 0, 2005: 0, 2010: 0, 2015: 0, 2020: 0, 2025: 0, 2030: 0, 2035: 0,
                    2040: 0, 2045: 0, 2050: 0, 2055: 0, 2060: 0, 2065: 0, 2070: 0, 2075: 0,
                    2080: 0, 2085: 0, 2090: 0, 2095: 0, 2100: 0}}

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