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