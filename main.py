import argparse
from hotel import KEYS, HOTEL_ID, DESTINATION_ID, Hotel
from supplier import *
import matching as MatchingMachine
import json

def LoadData(hotel_manager):
    suppliers = [AcmeSupplier(), 
                 PatagoniaSupplier(), 
                 PaperFliesSupplier()]
    
    
    for supplier in suppliers:
        supplier_flattened_keys = supplier.get_flattened_keys()
        
        # Automatic key mapping
        key_mapping = MatchingMachine.match(KEYS, supplier_flattened_keys)
        # Manual key mapping from supplier
        key_mapping.update(supplier.get_key_mapping())
        
        if HOTEL_ID not in key_mapping or DESTINATION_ID not in key_mapping:
            continue

        for hotel_data in supplier.get_flattened_data():
            id = hotel_data[key_mapping[HOTEL_ID]]
            des_id = hotel_data[key_mapping[DESTINATION_ID]]
            hotel_manager.setdefault((id, des_id), Hotel())
            hotel_manager[(id, des_id)].add_data(hotel_data, key_mapping)

    for hotel in hotel_manager.values():
        hotel.clean()

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("hotel_ids", type=str, help="Hotel IDs")
    parser.add_argument("destination_ids", type=str, help="Destination IDs")
    
    args = parser.parse_args()
    
    hotel_ids_input = args.hotel_ids
    destination_ids_input = args.destination_ids

    hotel_ids = None
    destination_ids = None

    if hotel_ids_input != 'none':
        hotel_ids = list(hotel_ids_input.split(','))
    
    if destination_ids_input != 'none':
        destination_ids = list(map(int, destination_ids_input.split(',')))

    hotel_manager = dict()
    LoadData(hotel_manager)

    # filtering
    hotels = [hotel for key, hotel in hotel_manager.items() if (hotel_ids is None or key[0] in hotel_ids) and (destination_ids is None or key[1] in destination_ids)]
    results = json.dumps([hotel.get_json() for hotel in hotels], indent=4)
    print(results)

if __name__ == "__main__":
    main()