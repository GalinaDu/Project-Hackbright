from flask import Flask, render_template, request
import json 
import os
import requests

Authorization: Basic {base64Value} 
Content-Type: application/x-www-form-urlencoded 
POST https://api.precisely.com/oauth/token
grant_type=client_credentials 

API_KEY = 'UmzJbXXIi9G4qotzqkExEWROIPgvHSla'
SECRET = 'BFAYef1EJTJHFiAG'
ENDPOINT ='https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'bearer %s' % API_KEY}

# Define parameters

PARAMETERS = {'term': 'apartments',
               'limit': 1,
               'radius': 5000,
               'location': 'San Carlos'}

# make request to the yelp API 
response = requests.get(url = ENDPOINT, params = PARAMETERS, headers = HEADERS)
crime_data = response.json

#convert JSON to Dict
yelp_data= response.json()

print(yelp_data)







https://api.precisely.com/risks/v1/crime/bylocation?latitude=35.0118&longitude=-81.9571&type=all&includeGeometry=N