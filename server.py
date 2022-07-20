"""Server for project app."""

from flask import Flask, render_template, request, flash, session, redirect
import requests
from sqlalchemy import true
from model import User, connect_to_db, db
from flask_sqlalchemy import SQLAlchemy
import crud
import model 
import datetime
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
app.config["SESSION_PERMANENT"] = True 

db = SQLAlchemy(app)


@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")


@app.route("/account", methods=["POST"])
def create_account():

    email = request.form.get("email")
    password = request.form.get("password")
    name = request.form.get("name")
    print ("user",email, password, name)
    user = crud.get_user_by_email(email)
    if user:
        return redirect("/users")
    else:
        user = crud.create_user(email, password, name)
        db.session.add(user)
        db.session.commit()
        print("Account created! Please log in.")
        return redirect("/map")

    

@app.route("/login", methods=["POST"])
def login_page():
    """ Load login user page"""
    email = request.form.get("email_exist")
    password = request.form.get("password_exist")

    user= crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you enetered is incorrect.")
        return redirect("/")
    else: 
        session["user_email"] = user.email
        flash(f"Welcome back, {user.name}!")

    return redirect("/map")


@app.route("/map")
def view_basic_map():

    return render_template("map.html") 
@app.route("/mapdata", methods=["POST"])
def map_data():

    formdata = request.json
    print("Post values", type(formdata))
    session['city'] = formdata['city']
    session['latitude'] = formdata['lat']
    session['longitude'] = formdata['lng']
    
    for key, vallue in formdata.items():
        print (key, vallue)
    
    return formdata
    
# @app.route("/users")
# def all_users():
#     """View all users."""
    
#     return render_template("user_page.html")


@app.route("/restaurants")
def show_allrestaurants():
    location = session['city']
    print("city", location)

    API_KEY = 'x5IxVg51C5iiYs2PF5lK9dpr6Ifb74aqoHFisSCIIXWOU3B3K4mji6zheFBII41jow3Leccl22uF-epWurn8THx4GK74AGHQRawTKxLBhD_YvHGOx3XCd_44BQipYnYx'
    ENDPOINT ='https://api.yelp.com/v3/businesses/search'
    HEADERS = {'Authorization': 'bearer %s' % API_KEY}

# Define parameters

    PARAMETERS = {'term': "restaurants",
               'limit': 12,
               'radius': 5000,
               'location': location}

# make request to the yelp API 
    response = requests.get(url = ENDPOINT, params = PARAMETERS, headers = HEADERS)

#convert JSON to Dict
    yelp_data= response.json()
    restaurants = []
    for biz in yelp_data["businesses"]:
        restaurant = biz
        restaurants.append(restaurant)
     
        for res in restaurants:
            coordinates = res['coordinates']
    print (yelp_data)        
    return render_template("restaurant.html", restaurants=restaurants, coordinates=coordinates)  

@app.route("/parks")
def show_allparks():
    location = session['city']
    print("city", location)

    API_KEY = 'x5IxVg51C5iiYs2PF5lK9dpr6Ifb74aqoHFisSCIIXWOU3B3K4mji6zheFBII41jow3Leccl22uF-epWurn8THx4GK74AGHQRawTKxLBhD_YvHGOx3XCd_44BQipYnYx'
    ENDPOINT ='https://api.yelp.com/v3/businesses/search'
    HEADERS = {'Authorization': 'bearer %s' % API_KEY}

# Define parameters

    PARAMETERS = {'term': 'parks',
               'limit': 12,
               'radius': 5000,
               'location': location}

# make request to the yelp API 
    response = requests.get(url = ENDPOINT, params = PARAMETERS, headers = HEADERS)

#convert JSON to Dict
    yelp_data= response.json()
    parks = []
    for biz in yelp_data["businesses"]:
        park = biz
        parks.append(park)
    return render_template("park.html", parks=parks) 


@app.route("/school")
def show_schools_e():
    lat= session['latitude']
    lon = session['longitude']
    API_KEY ="hWPvgeHUij6CJ8dS4BKzU3Gm0dPuMTwu4ai0AuOQ" 
    ENDPOINT_E ='https://gs-api.greatschools.org/nearby-schools'
    HEADERS_E = {'x-api-key':'hWPvgeHUij6CJ8dS4BKzU3Gm0dPuMTwu4ai0AuOQ'}
    PARAMETERS_E= {'lat': lat,
               'lon': lon,
               'distance': 5,
               'maximum': 5,
               'level_codes':'e'}


               
    response = requests.get(url = ENDPOINT_E, headers= HEADERS_E, params=PARAMETERS_E)
    school_data = response.json()
    schools = []
    for i in school_data["schools"]:
        school = i
        schools.append(school)
        website = []
        for school in schools:
            web_site = school["web-site"] 
            website.append(web_site)
    print (schools)

    return render_template("school.html", schools=schools, website=website)

# @app.route("/schoolm")
# def show_schools_m():
#     lat= session['latitude']
#     lon = session['longitude']
#     ENDPOINT_M ='https://gs-api.greatschools.org/nearby-schools'
#     HEADERS_M = {'x-api-key':'hWPvgeHUij6CJ8dS4BKzU3Gm0dPuMTwu4ai0AuOQ'}
#     PARAMETERS_M= {'lat': lat,
#                'lon': lon,
#                'distance': 5,
#                'maximum': 5,
#                'level_codes':'m'}

          
#     response = requests.get(url = ENDPOINT_M, headers= HEADERS_M, params=PARAMETERS_M)
#     school_data = response.json()
#     schools_m = []
#     for i in school_data["schools"]:
#         school = i
#         schools_m.append(school)
#     print (schools_m[0])

#     return render_template("school.html", schools_m=schools_m)

# @app.route("/schoolh")
# def show_schools_h():
#     lat= session['latitude']
#     lon = session['longitude']
#     ENDPOINT_H ='https://gs-api.greatschools.org/nearby-schools'
#     HEADERS_H = {'x-api-key':'hWPvgeHUij6CJ8dS4BKzU3Gm0dPuMTwu4ai0AuOQ'}
#     PARAMETERS_H= {'lat': lat,
#                'lon':lon,
#                'distance': 5,
#                'maximum': 5,
#                'level_codes':'h'}


#     response = requests.get(url = ENDPOINT_H, headers= HEADERS_H, params=PARAMETERS_H)
#     school_data = response.json()
#     schools_h = []
#     for i in school_data["schools"]:
#         school = i
#         schools_h.append(school)
#     print (schools_h[0])

#     return render_template("school.html", schools_h=schools_h)


@app.route("/apartments")
def show_yelpsearch():
    
    location = session['city']
    print("city", location)

    API_KEY = 'x5IxVg51C5iiYs2PF5lK9dpr6Ifb74aqoHFisSCIIXWOU3B3K4mji6zheFBII41jow3Leccl22uF-epWurn8THx4GK74AGHQRawTKxLBhD_YvHGOx3XCd_44BQipYnYx'
    ENDPOINT ='https://api.yelp.com/v3/businesses/search'
    HEADERS = {'Authorization': 'bearer %s' % API_KEY}

# Define parameters

    PARAMETERS = {'term': 'apartments',
               'limit': 12,
               'radius': 5000,
               'location': location}

# make request to the yelp API 
    response = requests.get(url = ENDPOINT, params = PARAMETERS, headers = HEADERS)

#convert JSON to Dict
    yelp_data= response.json()
    apartments = []
    for biz in yelp_data["businesses"]:
        apartment = biz
        apartments.append(apartment)


    return render_template("apartments.html", apartments=apartments) 




@app.route("/crime")
def call_crime_api():
   

    # call to generate token api
    BASE64val = 'VW16SmJYWElpOUc0cW90enFrRXhFV1JPSVBndkhTbGE6QkZBWWVmMUVKVEpIRmlBRw=='
    ENDPOINT ='https://api.precisely.com/oauth/token'
    HEADERS = {
        'Authorization': 'Basic VW16SmJYWElpOUc0cW90enFrRXhFV1JPSVBndkhTbGE6QkZBWWVmMUVKVEpIRmlBRw==', 
        'Content-Type': 'application/x-www-form-urlencoded'
    }


# make request to the crime API 
    response = requests.post(url = ENDPOINT, data={'grant_type': 'client_credentials'}, headers = HEADERS)
    data = response.json()
    data_token =data["access_token"]
    # print(data_token)
    return make_api_call_crime(data_token)
    

def make_api_call_crime(token):
    lat = session['latitude']
    lng = session['longitude']
    print(lng, lat)
    HEADERS ={'Authorization': 'Bearer ' + token}
    ENDPOINT = 'https://api.precisely.com/risks/v1/crime/bylocation?'
    PARAMETERS = {'latitude': lat,
               'longitude': lng,
               'type': 'all',
               }
    response = requests.get(url = ENDPOINT, headers= HEADERS, params=PARAMETERS)
    data =response.json()
    data_loop = data['themes'][0]['crimeIndexTheme']['indexVariable']
    names = []
    scores = []
    categories = []
    states = []
    for i in data_loop:
        names.append(i['name'])
        scores.append(i['score'])
        categories.append(i['category'])
        states.append(i['stateScore'])
    print(data)
    return render_template("crime1.html", names=names, scores=scores, categories=categories, states=states)     





if __name__ == "__main__":
  
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)