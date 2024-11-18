HOTEL_ID = 'hotel_id'
DESTINATION_ID = 'destination_id'
NAME = 'name'
LATITUDE = 'latitude'
LONGITUDE = 'longitude'
ADDRESS = 'address'
CITY = 'city'
COUNTRY = 'country'
DESCRIPTION = 'description'
AMENITIES_GENERAL = 'amenities.gen'
AMENITIES_ROOM = 'amenities.room'
IMAGES_ROOMS = 'images.rooms'
IMAGES_SITES = 'images.sites'
IMAGES_AMENITIES = 'images.amenities'
CONDITIONS = 'conditions'
KEYS = [HOTEL_ID, DESTINATION_ID, NAME, LATITUDE, LONGITUDE, ADDRESS, CITY, COUNTRY, DESCRIPTION, AMENITIES_GENERAL, AMENITIES_ROOM, IMAGES_ROOMS, IMAGES_SITES, IMAGES_AMENITIES, CONDITIONS]

class Hotel:
    def __init__(self):
        self.hotel = dict()


    def add_data(self, data, key_mapping):
        try:
            # required fields (keys), if any of these fields missed, the progress should be stopped:
            for key in [HOTEL_ID, DESTINATION_ID]:
                self.hotel[key] = data[key_mapping[key]]
            
            # optional (single-value) fields, preferring longer data
            for key in [NAME, LATITUDE, LONGITUDE, ADDRESS, CITY, COUNTRY]:
                if key in key_mapping and (key not in self.hotel or len(str(self.hotel[key])) < len(str(data[key_mapping[key]]))):
                    self.hotel[key] = data[key_mapping[key]]

            # description can be merged from multiple data sources
            if DESCRIPTION in key_mapping:
                if DESCRIPTION not in self.hotel:
                    self.hotel[DESCRIPTION] = data[key_mapping[DESCRIPTION]]
                else:
                    self.hotel[DESCRIPTION] += ' ' + data[key_mapping[DESCRIPTION]]

            # list-of-single-values fields:
            for key in [AMENITIES_GENERAL, AMENITIES_ROOM, CONDITIONS]:
                if key in key_mapping:
                    self.hotel.setdefault(key, [])
                    self.hotel[key] += list(data[key_mapping[key]])
            
            # list-of-dicts ("link":, "description":) fields:
            for key in [IMAGES_ROOMS, IMAGES_SITES, IMAGES_AMENITIES]:
                if key in key_mapping:
                    for info in list(data[key_mapping[key]]):
                        link = list(info.values())[0]
                        description = list(info.values())[-1]
                        if 'https' in description[:5]:
                            link, description = description, link
                        self.hotel.setdefault(key, [])
                        self.hotel[key].append({'link': link, 'description': description})

        except Exception as e:
            # raise error or warning
            return False
        return True
    

    def raw_text(self, data):
        return ''.join(data.lower().strip().split())    

    def clean_text(self, data):
        return data.lower().strip()    

    def clean_list(self, data):
        existed = set()
        result = []
        for item in data:
            if self.raw_text(item) not in existed:
                existed.add(self.raw_text(item))
                result.append(self.clean_text(item))
        return result
    

    def clean(self):

        # add missing fields
        for key in [AMENITIES_GENERAL, AMENITIES_ROOM, IMAGES_ROOMS, IMAGES_SITES, IMAGES_AMENITIES, CONDITIONS]:
            self.hotel.setdefault(key, [])        
        for key in KEYS:
            self.hotel.setdefault(key, None)

        self.hotel[AMENITIES_GENERAL] = self.clean_list(self.hotel[AMENITIES_GENERAL])
        self.hotel[AMENITIES_ROOM] = self.clean_list(self.hotel[AMENITIES_ROOM])
        
        # one exists in rooms should not exist in general
        amenities_room = set([self.raw_text(amenity) for amenity in self.hotel[AMENITIES_ROOM]])
        self.hotel[AMENITIES_GENERAL] = [amenity for amenity in self.hotel[AMENITIES_GENERAL] if self.raw_text(amenity) not in amenities_room]


    def get_json(self):
        return {
            "id": self.hotel[HOTEL_ID],
            "destination_id": self.hotel[DESTINATION_ID],
            "name": self.hotel[NAME],
            "location": {
                "lat": self.hotel[LATITUDE],
                "lng": self.hotel[LONGITUDE],
                "address": self.hotel[ADDRESS],
                "city": self.hotel[CITY],
                "country": self.hotel[COUNTRY]
            },
            "description": self.hotel[DESCRIPTION],
            "amenities": {
                "general": self.hotel[AMENITIES_GENERAL],
                "room": self.hotel[AMENITIES_ROOM]
            },
            "images": {
                "rooms": self.hotel[IMAGES_ROOMS],
                "site": self.hotel[IMAGES_SITES],
                "amenities": self.hotel[IMAGES_AMENITIES]
            },
            "booking_conditions": self.hotel[CONDITIONS]
        }
