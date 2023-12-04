import json
from datetime import datetime, timedelta

def filter_offers(checkin_date, input_file="input.json", output_file="output.json"):
    with open(input_file, 'r') as file:
        data = json.load(file)

    checkin_date = datetime.strptime(checkin_date, '%Y-%m-%d')

    filtered_offers = []
    selected_categories_map = {}

    valid_categories = {1, 2, 4}

    for offer in data['offers']:
        # Kiểm tra category có nằm trong valid_categories và ngày hết hạn có lớn hơn ngày checkin + 5 ngày
        if (
            offer['category'] in valid_categories and
            datetime.strptime(offer['valid_to'], '%Y-%m-%d') >= checkin_date + timedelta(days=5)
        ):
            offer['merchants'] = sorted(offer['merchants'], key=lambda x: x['distance'])
            selected_merchant = offer['merchants'][0]

            # Kiểm tra category đã được chọn trước đó chưa, nếu chưa thì thêm vào filtered_offers
            # Nếu đã được chọn thì kiểm tra khoảng cách của merchant hiện tại có nhỏ hơn merchant đã chọn trước đó không
            if (
                offer['category'] not in selected_categories_map or
                selected_merchant['distance'] < selected_categories_map[offer['category']]['distance']
            ):
                filtered_offers.append({
                    'id': offer['id'],
                    'title': offer['title'],
                    'description': offer['description'],
                    'category': offer['category'],
                    'merchants': [selected_merchant],
                    'valid_to': offer['valid_to']
                })
                selected_categories_map[offer['category']] = {
                    'distance': selected_merchant['distance'],
                    'id': selected_merchant['id']
                }

    # Sắp xếp lại filtered_offers theo thứ tự tăng dần của khoảng cách
    # Chọn ra 2 offer có khoảng cách nhỏ nhất
    selected_offers = sorted(filtered_offers, key=lambda x: x['merchants'][0]['distance'])[:2]

    output_data = {'offers': selected_offers}
    with open(output_file, 'w') as file:
        json.dump(output_data, file, indent=2)

if __name__ == "__main__":
    filter_offers('2019-12-25')
    print("Filtered offers saved to output.json.")
