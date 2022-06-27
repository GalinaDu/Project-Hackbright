from datetime import datetime
from enum import unique
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String)

    neighborhood = db.relationship("Neighborhood", secondary="pneighborhoods",backref="users")

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email} user name {self.name}>"

    @classmethod
    def create(cls, email, password, name):
       """Create and return a new user."""

       return cls(email=email, password=password, name=name)

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter(User.email == email).first()

    @classmethod
    def all_users(cls):
        return cls.query.all()

class School(db.Model):
    """A school."""

    __tablename__ = "schools"

    school_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    rating = db.Column(db.Integer)
    private = db.Column(db.Boolean)
    name = db.Column(db.String)
    neighborhood_id = db.Column(db.Integer, db.ForeignKey("neighborhoods.neighborhood_id"))

   

    def __repr__(self):
        return f"<School school_id={self.school_id} school name {self.name}>"

class Apartment(db.Model):
    """Apartment."""

    __tablename__ = "apartments"

    apartment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score = db.Column(db.Integer)
    address = db.Column(db.String)
    name = db.Column(db.String)
    neighborhood_id = db.Column(db.Integer, db.ForeignKey("neighborhoods.neighborhood_id"))

    #Child of NEighborhoods

    def __repr__(self):
        return f"<Apartment apartmentl_id={self.apartment_id} apartment name {self.name}>"

class Restaurant(db.Model):
    """ Restaurant."""

    __tablename__ = " restaurants"

    restaurant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    rating = db.Column(db.Integer)
    address = db.Column(db.String)
    name = db.Column(db.String)
    cuisine_type = db.Column(db.String) 
    neighborhood_id = db.Column(db.Integer, db.ForeignKey("neighborhoods.neighborhood_id"))

     #Child of NEighborhoods

    def __repr__(self):
        return f"<Restaurant restaurant_id={self.restaurant_id} restaurant name {self.name}>"

class Park(db.Model):
    """ Parks."""

    __tablename__ = "parks"

    park_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    address = db.Column(db.String)
    dog_friendly = db.Column(db.Boolean)
    bbq = db.Column(db.Boolean)
    playground = db.Column(db.Boolean) 
    neighborhood_id = db.Column(db.Integer, db.ForeignKey("neighborhoods.neighborhood_id"))

     #Child of NEighborhoods


    def __repr__(self):
        return f"<Park park_id={self.park_id} park address {self.address}>"

class Gym(db.Model):
    """ Gyms."""

    __tablename__ = "gyms"

    gym_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    address = db.Column(db.String)
    name = db.Column(db.String)
    neighborhood_id = db.Column(db.Integer, db.ForeignKey("neighborhoods.neighborhood_id"))

  
     #Child of NEighborhoods

    def __repr__(self):
        return f"<Park park_id={self.park_id} park address {self.address}>"

class Neighborhood(db.Model):
    """A neighborhood."""

    __tablename__ = "neighborhoods"

    neighborhood_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    zipcode = db.Column(db.Integer, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    # Comments attributes
    #neighborhood = db.relationship("Pneighborhood", secondary="neighborhoods")
    schools = db.relationship("School", backref="neighborhood")
    apartments = db.relationship("Apartment", backref="neighborhood")
    restaurants = db.relationship("Restaurant", backref="neighborhood")
    gyms = db.relationship("Gym", backref="neighborhood")
    parks = db.relationship("Park", backref="neighborhood")



    def __repr__(self):
        return f"<Neighborhood neighborhood_id={self.neighborhood_id} zip ={self.zipcode}>"


class Pneighborhood(db.Model):
    """Prefered neighborhood."""

    __tablename__ = "pneighborhoods"

    pneighborhood = db.Column(db.Integer, autoincrement=True, primary_key=True)
    neighborhood_id = db.Column(db.Integer, db.ForeignKey("neighborhoods.neighborhood_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
 

     

    def __repr__(self):
        return f"< Prefered neighborhood pneighborhood_id={self.pneighborhood_id}>"


def connect_to_db(flask_app, db_uri="postgresql:///project", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
