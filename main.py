
import re
import sys
import time
import json
import os
import random
import math
import datetime
from itertools import product, permutations, combinations

ids = []
origin = None

def create_id():
    unique = False
    new_id = 0
    while unique == False:
        new_id = random.randint(1000000, 9999999)
        unique = True
        for _id in ids:
            if _id == new_id:
                unique = False
                break
    ids.append(new_id)
    return new_id

class Airport:
    def __init__(self, _id, _name, _domestic, _origin, _disallowed_strs, _city, _blacklisted=None, _connects=None):
        self._id = _id
        self.name = _name
        self.domestic_only = _domestic
        self.origin_travel = _origin
        self.disallowed_strs = _disallowed_strs
        self.city = _city
        self.blacklisted = [] if _blacklisted is None else _blacklisted
        self.connects = [] if _connects is None else _connects
    
    @property
    def _str(self):
        sttr = []
        sttr.append('  ----------{}----------\n'.format(self.name))
        sttr.append('  ID:           {}\n'.format(self._id))
        sttr.append('  Domestic?:    {}\n'.format('True' if self.domestic_only == True else 'False'))
        sttr.append('  Origin?:      {}\n'.format('True' if self.origin_travel == True else 'False'))
        sttr.append('  Disallowed:   {}\n'.format(self.disallowed_strs))
        sttr.append('  City:         {}\n'.format(self.city.name))
        sttr.append('  Blacklisted:  {}\n\n'.format(self.blacklisted))
        return ''.join(sttr)
    
    @property
    def is_origin(self):
        return True if self._id == origin._id else False
    
    @property
    def _type(self):
        return 1
    
    def is_blacklisted(self, connect):
        for blacklisted in self.blacklisted:
            if connect._id == blacklisted._id:
                return True
        return False
    
    def same(self, connect):
        return True if self._id == connect._id else False
    
    def same_city(self, connect):
        return True if self.city._id == connect.city._id else False
    
    def same_country(self, connect):
        return True if self.is_origin == False and connect.is_origin == False and self.city.country._id == connect.city.country._id else False
    
    def same_region(self, connect):
        return True if self.is_origin == False and connect.is_origin == False and self.city.country.region._id == connect.city.country.region._id else False
    
    def is_valid(self, connect):
        if self.same(connect) == False and self.same_city(connect) == False:
            if connect.is_origin == True or self.is_origin == True:
                if connect.is_origin == True:
                    return True if self.origin_travel == True and self.is_blacklisted(connect) == False else False
                else:
                    return True if connect.origin_travel == True and connect.is_blacklisted(self) == False else False
            
            if self.is_blacklisted(connect) == True or connect.is_blacklisted(self) == True:
                return False
            if self.same_country(connect) == False and (self.domestic_only == True or connect.domestic_only == True):
                return False
            return True
        return False
    
    @property
    def optional(self):
        return self.city.optional
    
    @staticmethod
    def construct_blacklists(regions):
        airports = []
        airports.append(origin)
        for region in regions:
            for country in region.countries:
                for city in country.cities:
                    for airport in city.airports:
                        airports.append(airport)
        r = 0
        c = 0
        y = 0
        a = 0
        for region in regions:
            c = 0
            for country in regions[r].countries:
                y = 0
                for city in regions[r].countries[c].cities:
                    a = 0
                    for airport in regions[r].countries[c].cities[y].airports:
                        for disallowed in regions[r].countries[c].cities[y].airports[a].disallowed_strs:
                            for _airport in airports:
                                if disallowed == _airport.name:
                                    regions[r].countries[c].cities[y].airports[a].blacklisted.append(_airport)
                                else:
                                    regions[r].countries[c].cities[y].airports[a].connects.append(_airport)
                        a = a + 1
                    y = y + 1
                c = c + 1
            r = r + 1
        return regions
        

class City:        
    def __init__(self, _id, _name, _grp, _full_days, _priority, _train, _airports=None, _country=None):
        self._id = _id
        self.name = _name
        self.grp = _grp
        self.min_full_days = _full_days
        self.priority = _priority
        self.train = _train
        self.airports = [] if _airports is None else _airports
        self.country = _country
    
    @property
    def connects(self):
        connectz = []
        for airport in self.airports:
            for connect_ in airport.connects:
                found = False
                for connect in connectz:
                    if connect._id == airport._id:
                        found = True
                        break
                if found == False:
                    connectz.append(airport)
        return connectz
    
    @property
    def _type(self):
        return 2

    def same(self, connect):
        return True if self._id == connect._id else False
        
    def same_country(self, connect):
        return True if self.airport.is_origin == False and connect.is_origin == False and self.country._id == connect.country._id else False
    
    def same_region(self, connect):
        return True if self.airport.is_origin == False and connect.is_origin == False and self.country.region._id == connect.country.region._id else False

    @property
    def origin_travel_airport(self):
        for airport in airports:
            if airport.origin_travel == True:
                return airport
        return None

    @property
    def origin_travel(self):
        for airport in self.airports:
            if airport.origin_travel == True:
                return True
        return False

    @property
    def optional(self):
        return True if self.min_full_days == 0 else False

class Country:        
    def __init__(self, _id, _name, _grp, _train_cost, _cities=None, _region=None):
        self._id = _id
        self.name = _name
        self.grp = _grp
        self.train_cost = _train_cost
        self.cities = [] if _cities is None else _cities
        self.region = _region
    
    @property
    def _type(self):
        return 3
    
    def same(self, connect):
        return True if self._id == connect._id else False
    
    def same_region(self, connect):
        return True if self.region._id == connect.region._id else False
    
    @property
    def has_origin_travel(self):
        for city in self.cities:
            if city.origin_travel == True:
                return True
        return False
                
    @property
    def all_airports(self):
        airports = []
        for city in self.cities:
            for airport in city.airports:
                airports.append(airport)
        return airports
    
    @property
    def origin_airports(self):
        airports = []
        for city in self.cities:
            for airport in city.airports:
                if airport.origin_travel:
                    airports.append(airport)
        return airports
    
    @property
    def required_airports(self):
        airports = []
        for city in self.cities:
            if city.optional == False:
                for airport in city.airports:
                    airports.append(airport)
        return airports
    
    @property
    def optional_airports(self):
        airports = []
        for city in self.cities:
            if city.optional == True:
                for airport in city.airports:
                    airports.append(airport)
        return airports
    
    @property
    def optional(self):
        return all(city.optional for city in self.cities)

class Region:
    def __init__(self, _id, _grp, _countries=[]):
        self._id = _id
        self.grp = _grp
        self.countries = _countries
    
    @property
    def _type(self):
        return 4
    
    def same(self, connect):
        return True if self._id == connect._id else False
    
    @property
    def has_origin_travel(self):
        for country in self.countries:
            if country.has_origin_travel == True:
                return True
        return False
    
    @property
    def all_airports(self):
        airports = []
        for country in self.countries:
            for city in country.cities:
                for airport in city.airports:
                    airports.append(airport)
        return airports
    
    @property
    def origin_airports(self):
        airports = []
        for country in self.countries:
            for city in country.cities:
                for airport in city.airports:
                    if airport.origin_travel:
                        airports.append(airport)
        return airports
    
    @property
    def required_airports(self):
        airports = []
        for country in self.countries:
            for city in country.cities:
                if city.optional == False:
                    for airport in city.airports:
                        airports.append(airport)
        return airports
    
    @property
    def optional_airports(self):
        airports = []
        for country in self.countries:
            for city in country.cities:
                if city.optional == True:
                    for airport in city.airports:
                        airports.append(airport)
        return airports
    
    @property
    def optional(self):
        for country in self.countries:
            if country.optional == False:
                return False
        return True
    
    @staticmethod
    def _all_airports(regions):
        airports = []
        for region in regions:
            for country in region.countries:
                for city in country.cities:
                    for airport in city.airports:
                        airports.append(airport)
        return airports
    
    @staticmethod
    def split_into_groups(countries):
        grouped = []
        for country in countries:
            grp_index = 0
            unique = True
            for group in grouped:
                if country.grp == grouped[grp_index][0].grp:
                    grouped[grp_index].append(country)
                    unique = False
                    break
                grp_index = grp_index + 1
            if unique == True:
                grouped.append([country])
        
        regions = []
        for group in grouped:
            regions.append(Region(create_id(), group[0].grp, group))
        
        r = 0
        c = 0
        for region in regions:
            c = 0
            for country in regions[r].countries:
                regions[r].countries[c].region = regions[r]
                c = c + 1
            r = r + 1
        
        return regions

class SubTrip:
    def __init__(self, _id, _orig, _dest, _depart_time=None, _trip_time=None, _flight=True, _unconnectables=None, _connectables=None):
        self._id = _id
        self.origin = _orig
        self.destination = _dest
        self.depart_time = _depart_time
        self.trip_time = _trip_time
        self.flight = _flight
        self.unconnectables = [] if _unconnectables is None else _unconnectables
        self.connectables = [] if _connectables is None else _connectables
    
    @property
    def origin_flight(self):
        return True if self.origin.is_origin or self.destination.is_origin else False
    
    @property
    def initial_flight(self):
        return True if self.origin.is_origin else False
    
    @property
    def final_flight(self):
        return True if self.destination.is_origin else False
    
    @property
    def is_domestic(self):
        return True if self.origin_flight == False and self.origin.same_country(self.destination) == True else False
    
    @property
    def is_within_region(self):
        return True if self.origin_flight == False and self.origin.same_region(self.destination) == True else False
    
    @property
    def _type(self):
        return 5
    
    @property
    def o_grp(self):
        if self.initial_flight == True:
            return None
        else:
            return self.origin.grp
    
    @property
    def d_grp(self):
        if self.final_flight == True:
            return None
        else:
            return self.origin.grp
    
    @property
    def grp(self):
        if self.initial_flight == True:
            return self.destination.grp
        elif self.final_flight == True:
            return self.origin.grp
        elif self.is_within_region == True:
            return self.origin.grp
        else:
            return None
    
    @property
    def domestic_connectables(self):
        domestic = []
        for connect in self.connectables:
            if self.final_flight == False:
                if self.destination.same_country(connect.origin) == True:
                    domestic.append(connect)
        return domestic
    
    @property
    def regional_connectables(self):
        regional = []
        for connect in self.connectables:
            if self.final_flight == False:
                if self.destination.same_region(connect.origin) == True and self.destination.same_country(connect.origin) == False:
                    regional.append(connect)
        return regional
    
    @property
    def interregional_connectables(self):
        regional = []
        for connect in self.connectables:
            if self.final_flight == False:
                if self.destination.same_region(connect.origin) == False and self.destination.same_country(connect.origin) == False:
                    regional.append(connect)
        return regional
    
    @property
    def final_connectables(self):
        origin = []
        for connect in self.connectables:
            if self.final_flight == True:
                if self.destination.same_city(connect.origin) == True:
                    origin.append(connect)
        return origin
    
    @property
    def optional(self):
        return self.destination.optional
    
    @property
    def is_valid(self):
        return True if self.origin.is_valid(self.destination) else False
    
    @property
    def has_domestic_connectable(self):
        return True if len(self.domestic_connectables) > 0 else False
    
    @property
    def has_inner_regional_connectable(self):
        return True if len(self.regional_connectables) > 0 else False
    
    def has_airport(self, airport):
        return self.origin.same_city(airport) == True or self.destination.same_city(airport) == True
    
    def is_repetitive(self, _subtrips):
        if self.origin_flight == True:
            return False
        else:
            for _subtrip in _subtrips:
                if _subtrip.has_airport(self.destination) == True:
                    return True
            return False
    
    def is_connectable(self, connect):
        return True if self.destination.same_city(connect.origin) == True and self.origin.same_city(connect.destination) == False and self._id != connect._id else False
    
    def generate_connectables(self, _subtrips):
        for _subtrip in _subtrips:
            if self.is_connectable(_subtrip) == False:
                self.unconnectables.append(_subtrip)
            else:
                self.connectables.append(_subtrip)
    
    @property
    def _str(self):
        sttr = []
        sttr.append('{} -> {}'.format(self.origin.name, self.destination.name))
        return ''.join(sttr)
        
    @staticmethod
    def cross_regional_filter(subtrips):
        crossed = []
        for subtrip in subtrips:
            if subtrip.origin_flight == False and subtrip.is_within_region == False and subtrip.is_domestic == False:
                crossed.append(subtrip)            
        return crossed
        
    @staticmethod
    def inter_regional_filter(subtrips):
        grouped = []
        for subtrip in subtrips:
            g = 0
            unique = True
            for group in grouped:
                if subtrip.origin_flight == False and subtrip.is_domestic == False and subtrip.is_within_region == True:
                    if subtrip.grp == grouped[g][0].grp:
                        grouped[g].append(subtrip)
                        unique = False
                        break
                g = g + 1
            if unique == True:
                grouped.append([subtrip])
        return grouped
    
    @staticmethod
    def inner_regional_filter(subtrips):
        grouped = []
        for subtrip in subtrips:
            g = 0
            unique = True
            for group in grouped:
                if subtrip.origin_flight == False and subtrip.is_domestic == True and subtrip.is_within_region == False:
                    if subtrip.grp == grouped[g][0].grp:
                        grouped[g].append(subtrip)
                        unique = False
                        break
                g = g + 1
            if unique == True:
                grouped.append([subtrip])
        return grouped

class Trip:
    def __init__(self, _id, _utilities, _subtrips=None, _trip_length=2, _destinations=[]):
        self._id = _id
        self.utility = _utilities
        self.subtrips = [] if _subtrips is None else _subtrips
        self.trip_length = _trip_length
        self.destinations = [] if _destinations is None else _destinations
    
    def __str__(self):
        strs = []
        subinfo = ['  Something']
        strs.append('TRIP {}  |  {} Days  |  {} Cities'.format(self._id, self.trip_length, len(self.destinations)))
        for destination in self.destinations:
            subinfo.append('  ')
        return '\n'.join(strs)
    
    @property
    def completed(self):
        return self.subtrips[-1].final_flight
    
    def filter_to_fit_in_trip_length(self, _subtrips):
        sts = []
        for subtrip in _subtrips:
            if (self.trip_length + 1 + subtrip.destination.city.min_full_days) <= self.utility.length_range[1]:
                sts.append(subtrip)
        return sts
    
    def filter_out_duplicates(self, _subtrips, _all):
        sts = []
        for subtrip in _subtrips:
            if subtrip.is_repetitive(_all) == False:
                sts.append(subtrip)
        return sts
    
    @property
    def connectablez(self):
        if self.completed == False:
            if self.trip_length >= (self.utility.length_range[0] - 1):
                self.trip_length = self.trip_length + 1
                return self.subtrips[-1].final_connectables
            else:
                connects = []
                if self.subtrips[-1].has_domestic_connectable == True:
                    connects = self.filter_out_duplicates(self.filter_to_fit_in_trip_length(self.subtrips[-1].domestic_connectables), self.subtrips)
                if self.subtrips[-1].has_inner_regional_connectable == True and len(connects) == 0:
                    _regionals = self.subtrips[-1].regional_connectables
                    _lengthed = self.filter_to_fit_in_trip_length(_regionals)
                    connects = self.filter_out_duplicates(_lengthed, self.subtrips)
                if len(connects) == 0:
                    connects = self.filter_out_duplicates(self.filter_to_fit_in_trip_length(self.subtrips[-1].interregional_connectables), self.subtrips)
                return self.subtrips[-1].final_connectables if len(connects) == 0 else connects
        return []
    
    def calc_trip_len(self):
        _total = 1
        for dest in self.destinations:
            _total = _total + 1 + dest.city.min_full_days
        self.trip_length = _total
        return self
            
    def addST(self, st):
        self.subtrips.append(st)
        self.destinations.append(st.destination)
        return self.calc_trip_len()
    
    @property
    def _type(self):
        return 6
        
class Utilities:
    def __init__(self, _origin, _json, _trips=None, _all_subtrips=None, _regions=None, _nonorigin_sts=None, _domestic_sts=None, _inner_regional_sts=None, _inter_regional_sts=None, _origin_sts=None, _init_sts=None, _final_sts=None):
        self.origin_airport = _origin
        self.start_search_range = datetime.datetime(_json['start_search_range']['year'], _json['start_search_range']['month'], _json['start_search_range']['day'])
        self.end_search_range = datetime.datetime(_json['end_search_range']['year'], _json['end_search_range']['month'], _json['end_search_range']['day'])
        self.length_range = sorted(_json['length_range'])
        self.departure_weekdays = _json['departure_weekdays']
        self.return_weekdays = _json['return_weekdays']
        self.origin_airports = _json['origin_airports']
        self.origin_max_stops = _json['origin_max_stops']
        self.origin_max_layover_time = _json['origin_max_layover_time']
        self.intermediate_max_stops = _json['intermediate_max_stops']
        self.intermediate_max_layover_time = _json['intermediate_max_layover_time']
        self.trips = [] if _trips is None else _trips
        self.all_subtrips = [] if _all_subtrips is None else _all_subtrips
        self.regions = [] if _regions is None else _regions
        
        self.nonorigin_subtrips = [] if _nonorigin_sts is None else _nonorigin_sts
        self.domestic_subtrips = [] if _domestic_sts is None else _domestic_sts
        self.inner_regional_subtrips = [] if _inner_regional_sts is None else _inner_regional_sts
        self.inter_regional_subtrips = [] if _inter_regional_sts is None else _inter_regional_sts
        self.origin_subtrips = [] if _origin_sts is None else _origin_sts
        self.initial_subtrips = [] if _init_sts is None else _init_sts
        self.final_subtrips = [] if _final_sts is None else _final_sts
        
    def prep(self):
        airports = Region._all_airports(self.regions)
        airports.append(self.origin_airport)
        _subtrips = []
        for _origin_ in airports:
            for _dest in airports:
                if _origin_.is_valid(_dest) == True:
                    _subtrips.append(SubTrip(create_id(), _origin_, _dest))        
        for _subtrip in _subtrips:
            _subtrip.generate_connectables(_subtrips)
            self.all_subtrips.append(_subtrip)
            if _subtrip.origin_flight == True:
                self.origin_subtrips.append(_subtrip)
                if _subtrip.initial_flight == True:
                    self.initial_subtrips.append(_subtrip)
                else:
                    self.final_subtrips.append(_subtrip)
            else:
                self.nonorigin_subtrips.append(_subtrip)
                if _subtrip.is_domestic == True:
                    self.domestic_subtrips.append(_subtrip)
                elif _subtrip.is_within_region == True:
                    self.inner_regional_subtrips.append(_subtrip)
                else:
                    self.inter_regional_subtrips.append(_subtrip)
        print('TOTAL Subtrips Generated:  {}'.format(len(self.all_subtrips)))
        return self
    
    def construct_trips(self):
        self.trips = []
        for initial_st in self.initial_subtrips:
            self.trips.append(Trip(create_id(), self, [initial_st], (2+initial_st.destination.city.min_full_days), [initial_st.destination]).calc_trip_len())
        
        #DOESNT SEEM TO WORK AS INTENDED, NEEDS CHECKS SIMILAR TO CONNECTABLEZ
        added = True
        while added == True:
            t = 0
            new_trips = []
            added = False
            for trip in self.trips:
                first = True
                for connectable in trip.connectablez:
                    added = True
                    if first == True:
                        if connectable.optional == True:
                            new_trips.append(Trip(create_id(), self, trip.subtrips, trip.trip_length, trip.destinations).calc_trip_len())
                        self.trips[t].addST(connectable)
                    else:
                        if connectable.optional == True:
                            new_trips.append(Trip(create_id(), self, trip.subtrips, trip.trip_length, trip.destinations).calc_trip_len())
                        new_trips.append(Trip(create_id(), self, trip.subtrips, trip.trip_length, trip.destinations).calc_trip_len().addST(connectable))
                    first = False
                t = t + 1
            for _trip in new_trips:
                self.trips.append(_trip)
        print('TOTAL Trips Generated:     {}'.format(len(self.trips)))
        for _trip in self.trips:
            print(_trip)
    
    @property
    def _type(self):
        return 7

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
    regions = Airport.construct_blacklists(Region.split_into_groups(get_data(ojson['destinations'])))
    utils = Utilities(origin, ojson, [], [], regions)
    utils.prep().construct_trips()
    
if __name__ == "__main__":
    main()
