from model import db, User, Neighborhood, School, Park, Gym, Apartment, Restaurant, Pneighborhood, connect_to_db
from flask import Flask, render_template, request, flash, session, redirect

def create_user(email, password, name):
    """Create and return a new user."""

    user = User(email=email, password=password, name=name)

    return user


def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""
    
    return User.query.filter(User.email == email).first()


# def create_neighborhood(zipcode):
#     """Create and return a new neighborhood."""

   
#         zipcode=zipcode
#     )

#     return 


# def get_neighborhoods():
#     """Return all neighborhoods."""

#     return Neighborhood.query.all()


# def get_neighborhood_by_id(neighborhood_id):
#     """Return a movie by primary key."""

#     return Neighborhood.query.get(neighborhood_id)


# def create_school(rating, private, name):
#     """Create and return a new rating."""

#     school = School(rating=rating, private=private, name=name)

#     return school


# def update_rating(rating_id, new_score):
#     """ Update a rating given rating_id and the updated score. """
#     rating = Rating.query.get(rating_id)
#     rating.score = new_score

if __name__ == "__main__":
    from server import app

    connect_to_db(app)