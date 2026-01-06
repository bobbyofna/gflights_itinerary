import datetime
import random
from region import Region
from subtrip import SubTrip
from trip import Trip

ids = []

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
                recent = trip.subtrips[-1]
                connectables = recent.connectables
                
                
                
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
    
    @property
    def _type(self):
        return 7