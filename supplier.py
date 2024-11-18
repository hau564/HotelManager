import requests
import hotel

class Supplier:
    def __init__(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Fail getting data from {url}")
        self.data = response.json()
    
    # dfs through all the key paths, creating new dictionary {"key_path": value}
    # in each hotel, dicts contained in a list are not iterated, assuming the json data structure is not too complex 
    def deep_iterate(self, data, key_path = ""): 
        for key in data:
            if type(data[key]) == type(dict()):
                self.deep_iterate(data[key], key_path + key + ".")
            else:
                self.iterated_data[key_path + key] = data[key]
    
    # return a list of all the keys after flattening
    def get_flattened_keys(self):
        self.iterated_data = dict()
        self.deep_iterate(self.data[0])
        return list(key for key in self.iterated_data)
        
    # return a list of dicts, each with the keys flattened
    def get_flattened_data(self):
        for hotel_data in self.data:
            self.iterated_data = dict()
            self.deep_iterate(hotel_data)
            yield self.iterated_data
    
    # manual mapping standard keys to supplier's keys
    def get_key_mapping(self):
        return dict()

    def __str__(self):
        return str(self.data)
    

class AcmeSupplier(Supplier):
    def __init__(self):
        super().__init__("https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/acme")

    def get_key_mapping(self):
        return {
            hotel.AMENITIES_GENERAL: 'Facilities',
        }
    

class PatagoniaSupplier(Supplier):
    def __init__(self):
        super().__init__("https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/patagonia")

    def get_key_mapping(self):
        return {
            hotel.DESCRIPTION: 'info',
            hotel.LATITUDE: 'lat',
            hotel.LONGITUDE: 'lng'
        }


class PaperFliesSupplier(Supplier):
    def __init__(self):
        super().__init__("https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/paperflies")

    def get_key_mapping(self):
        return {
            hotel.DESCRIPTION: 'details',
        }