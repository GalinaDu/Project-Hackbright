"""Server for project app."""

from flask import Flask, render_template, request, flash, session, redirect
import requests
from sqlalchemy import true
from model import User, connect_to_db, db
from flask_sqlalchemy import SQLAlchemy
import crud
import model 
import datetime
# from bootstrap import "bootstrap"

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
    print (email, password, name)
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


@app.route("/map", methods=["POST"])
def view_basic_map():
    """Demo of basic map-related code.

    - Programmatically adding markers, info windows, and event handlers to a
      Google Map
    - Showing polylines, directions, etc.
    """
    session['city'] = request.form.get("city")
    return redirect("/users") 

    
@app.route("/users")
def all_users():
    """View all users."""
    
    return render_template("user_page.html")


@app.route("/restaurants")
def show_allrestaurants():
    location = request.form.get("city")
    print("city", location)

    API_KEY = 'x5IxVg51C5iiYs2PF5lK9dpr6Ifb74aqoHFisSCIIXWOU3B3K4mji6zheFBII41jow3Leccl22uF-epWurn8THx4GK74AGHQRawTKxLBhD_YvHGOx3XCd_44BQipYnYx'
    ENDPOINT ='https://api.yelp.com/v3/businesses/search'
    HEADERS = {'Authorization': 'bearer %s' % API_KEY}

# Define parameters

    PARAMETERS = {'term': 'apartments',
               'limit': 10,
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
    return render_template("restaurant.html")  

@app.route("/parks")
def show_allparks():
    location = request.form.get("city")
    print("city", location)

    API_KEY = 'x5IxVg51C5iiYs2PF5lK9dpr6Ifb74aqoHFisSCIIXWOU3B3K4mji6zheFBII41jow3Leccl22uF-epWurn8THx4GK74AGHQRawTKxLBhD_YvHGOx3XCd_44BQipYnYx'
    ENDPOINT ='https://api.yelp.com/v3/businesses/search'
    HEADERS = {'Authorization': 'bearer %s' % API_KEY}

# Define parameters

    PARAMETERS = {'term': 'parks',
               'limit': 10,
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

@app.route("/test") 
def test():
    return render_template("user_page.html")

@app.route("/apartments")
def show_yelpsearch():
    
    location = session['city']
    print("city", location)

    API_KEY = 'x5IxVg51C5iiYs2PF5lK9dpr6Ifb74aqoHFisSCIIXWOU3B3K4mji6zheFBII41jow3Leccl22uF-epWurn8THx4GK74AGHQRawTKxLBhD_YvHGOx3XCd_44BQipYnYx'
    ENDPOINT ='https://api.yelp.com/v3/businesses/search'
    HEADERS = {'Authorization': 'bearer %s' % API_KEY}

# Define parameters

    PARAMETERS = {'term': 'apartments',
               'limit': 10,
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
def show_crime_rate():
    return render_template("crime.html")

@app.route("/show-crime-rate", methods=["POST"]) 
def call_crime_api():
    lat = request.form.get("lat-input")
    lng = request.form.get("lng-input")
    print(lng, lat)

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
    print (data_token)
    make_api_call_crime(data_token)
    return "Hello"


def make_api_call_crime(token):
    HEADERS ={'Authorization': 'Bearer ' + token}
    ENDPOINT = 'https://api.precisely.com/risks/v1/crime/bylocation?latitude=35.0118&longitude=-81.9571&type=all&includeGeometry=N'
    response = requests.get(url = ENDPOINT, headers= HEADERS)
    data =response.json()
    print(data)
    return data
    #crime_data = response.json


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)