"""Server for project app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import User, connect_to_db, db
from flask_sqlalchemy import SQLAlchemy
import crud
import model 

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# db_name = 'project.db'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# this variable, db, will be used for all SQLAlchemy commands
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

    user = crud.get_user_by_email(email)
    if user:
        flash("Account with this email adress already exists. Please log in.")
    else:
        user = crud.create_user(email, password, name)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return  render_template("login.html")


@app.route("/login")
def login_page():
    """ Load login user page"""
    email = request.form.get("email")
    password = request.form.get("password")

    user= crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you enetered is incorrect.")
    else: 
        session["user_email"] = user.email
        flash(f"Welcome back, {user.name}!")

        return redirect("/map")


@app.route("/map")
def view_basic_map():
    """Demo of basic map-related code.

    - Programmatically adding markers, info windows, and event handlers to a
      Google Map
    - Showing polylines, directions, etc.
    """

    return render_template("map.html")   

    
@app.route("/users")
def all_users():
    """View all users."""

    users = User.all_users()

    return render_template("all_users.html", users=users)

@app.route("/user_page")
def user_profile_page():

    return render_template("user_page.html")

@app.route("/restaurants")
def show_allrestaurants():
    return render_template("restaurant.html")  

@app.route("/parks")
def show_allparks():
    return render_template("park.html")   

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)