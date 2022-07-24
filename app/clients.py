import requests

HOST = 'http://127.0.0.1:5000'

# test post
response = requests.post(f'{HOST}/advertisement/', json={'title': 'new1 auction', 'description': '1st day ',
                                                         'owner': 'Ivan'})
print(response.text)

# test get
# response = requests.get(f'{HOST}/advertisement/1')
# print(response.text)

# test patch
# response = requests.patch(f'{HOST}/advertisement/3', json={'title': 'story', 'description': '2nd day'})
# print(response.text)

# test delete
# response = requests.delete(f'{HOST}/advertisement/1')
# print(response.text)
