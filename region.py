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
