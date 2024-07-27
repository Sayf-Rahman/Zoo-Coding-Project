# stores database models

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# this model stores information about users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    cart = db.relationship('Cart', backref='user', lazy=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)
    has_free_tour = db.Column(db.Boolean, default=False) 
    has_made_booking = db.Column(db.Boolean, default=False)   

# this model represents attractions that users can add to their cart and book
class Attraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
   
# this model represenets hotel reservations that users can add to their cart and book
class HotelReservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hotel_name = db.Column(db.String(100), nullable=False)
    check_in_date = db.Column(db.DateTime, nullable=False)
    check_out_date = db.Column(db.DateTime, nullable=False)
    room_type = db.Column(db.String(50))
    num_guests = db.Column(db.Integer)
    total_price = db.Column(db.Float)   
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    cart = db.relationship('Cart', back_populates='hotel_reservations')
    
#this model represents a user's cart, containing attractions and hotel reservations
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    attractions = db.relationship('Attraction', secondary='cart_attraction', backref=db.backref('carts', lazy=True))
    quantity = db.Column(db.Integer, nullable=False, default=1) 
    price = db.Column(db.Float, nullable=False)
    hotel_reservations = db.relationship('HotelReservation', backref='cart', lazy=True)
    hotel_reservations = db.relationship('HotelReservation', back_populates='cart', lazy=True)

# this model is a join table between carts and attractions
class CartAttraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    attraction_id = db.Column(db.Integer, db.ForeignKey('attraction.id'), nullable=False)

# this model represents bookings made by users for attractions
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    attraction_id = db.Column(db.Integer, db.ForeignKey('attraction.id'), nullable=False)
    booked_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# this model stores card details for users
class CardDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    card_number = db.Column(db.String(16), nullable=False)  
    expiration_date = db.Column(db.String(10), nullable=False)
    cvc = db.Column(db.String(3), nullable=False)
    user = db.relationship('User', backref=db.backref('card_details', lazy=True))





