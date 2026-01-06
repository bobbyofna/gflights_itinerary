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
    def construct_blacklists(regions, origin):
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