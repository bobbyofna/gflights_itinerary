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