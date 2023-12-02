import json
from datetime import datetime, timedelta

def filter_offers(checkin_date, input_file="input.json", output_file="output.json"):

    with open(input_file, 'r') as file:
        data = json.load(file)

    checkin_date = datetime.strptime(checkin_date, '%Y-%m-%d')

    filtered_offers = []
    selected_categories_map = {}
    

    for offer in data['offers']:
        if (
            offer['category'] in {1, 2, 4} and 
            datetime.strptime(offer['valid_to'], '%Y-%m-%d') >= checkin_date + timedelta(days=5)
        ):
            # Sort merchants by distance and select the closest
            offer['merchants'] = sorted(offer['merchants'], key=lambda x: x['distance'])
            selected_merchant = offer['merchants'][0]

            if offer['category'] not in selected_categories_map:
                filtered_offers.append({
                    'id': offer['id'],
                    'title': offer['title'],
                    'description': offer['description'],
                    'category': offer['category'],
                    'merchants': [selected_merchant],
                    'valid_to': offer['valid_to']
                })
                selected_categories_map[offer['category']] = {selected_merchant['distance'], selected_merchant['id']}
            else:
                category_info = selected_categories_map[offer['category']]
                if selected_merchant['distance'] < next(iter(category_info)):
                    filtered_offers.append({
                        'id': offer['id'],
                        'title': offer['title'],
                        'description': offer['description'],
                        'category': offer['category'],
                        'merchants': [selected_merchant],
                        'valid_to': offer['valid_to']
                    })
                    filtered_offers = [offer for offer in filtered_offers if offer['id'] != selected_categories_map[offer['category']]['id']]
                    selected_categories_map[offer['category']] = {selected_merchant['distance'], selected_merchant['id']}
            
    
    selected_offers = sorted(filtered_offers, key=lambda x: x['merchants'][0]['distance'])[:2]

    output_data = {'offers': selected_offers}
    with open(output_file, 'w') as file:
        json.dump(output_data, file, indent=2)

if __name__ == "__main__":

    filter_offers('2019-12-25')
    print("Filtered offers saved to output.json.")
