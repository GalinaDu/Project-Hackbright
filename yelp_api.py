from flask import Flask, render_template, request
import json 
import os
import requests

# app = Flask(__name__)
# app.secret_key = 'SECRETSECRETSECRET'

# # This configuration option makes the Flask interactive debugger
# # more useful (you should remove this line in production though)
# app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


API_KEY = 'x5IxVg51C5iiYs2PF5lK9dpr6Ifb74aqoHFisSCIIXWOU3B3K4mji6zheFBII41jow3Leccl22uF-epWurn8THx4GK74AGHQRawTKxLBhD_YvHGOx3XCd_44BQipYnYx'

# @app.route('/afterparty/search')
# def find_afterparties():
#     """Search for afterparties on Eventbrite"""

#     keyword = request.args.get('keyword', '')
#     postalcode = request.args.get('zipcode', '')
#     radius = request.args.get('radius', '')
#     unit = request.args.get('unit', '')
#     sort = request.args.get('sort', '')

#     url = 'https://app.ticketmaster.com/discovery/v2/events'
#     payload = {'apikey': API_KEY,
#                'keyword': keyword,
#                'postalCode': postalcode,
#                'radius': radius,
#                'unit': unit,
#                'sort': sort}

ENDPOINT ='https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'bearer %s' % API_KEY}

# Define parameters

PARAMETERS = {'term': 'restaurant',
               'limit': 50,
               'radius': 5000,
               'location': 'San Carlos'}

# make request to the yelp API 
response = requests.get(url = ENDPOINT, params = PARAMETERS, headers = HEADERS)

#convert JSON to Dict
yelp_data= response.json()

print(yelp_data)


# if __name__ == '__main__':
#     app.debug = True
#     app.run(host='0.0.0.0')

