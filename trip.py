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