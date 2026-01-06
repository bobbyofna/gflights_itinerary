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

