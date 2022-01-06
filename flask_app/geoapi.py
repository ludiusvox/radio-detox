

import requests
from flask_app import routes as r
URL = "https://geocode.search.hereapi.com/v1/geocode"
location = r.predict.City #taking user input
api_key = 'cOP71wQ1CXuAVUcNVnoy' # Acquire from developer.here.com
PARAMS = {'apikey':api_key,'q':location}

# sending get request and saving the response as response object
r = requests.get(url = URL, params = PARAMS)
data = r.json()

latitude = data['items'][0]['position']['lat']
longitude = data['items'][0]['position']['lng']
