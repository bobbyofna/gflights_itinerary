import json
import os
from airport import Airport
from city import City
from country import Country
from region import Region
from utilities import Utilities, create_id

origin = None

def load_json_from_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    else:
        return None

def get_data(_json):
    _countries = []
    for country in _json:
        _country = Country(create_id(), country['country'], country['grp_a'], country['train_cost'], [])
        for city in country['cities']:
            _city = City(create_id(), city['city'], city['grp_b'], city['min_full_days'], city['priority'], city['train'], [], _country)
            for airport in city['airports']:
                _airport = Airport(create_id(), airport['airport'], airport['domestic_only'], airport['origin_travel'], airport['disallowed'], _city, [])
                _city.airports.append(_airport)
            _country.cities.append(_city)
        _countries.append(_country)
    return _countries

def main():
    ojson = load_json_from_file(f"{os.getcwd()}\\f_config.json")
    origin_city = City(create_id(), 'Philadelphia', -1, -1, -1, False, [])
    global origin
    origin = Airport(create_id(), "PHL", False, True, [], origin_city, [])
    regions = Airport.construct_blacklists(Utilities.split_into_groups(get_data(ojson['destinations'])), origin)
    utils = Utilities(origin, ojson, [], [], regions)
    utils.prep().construct_trips()
    
if __name__ == "__main__":
    main()
