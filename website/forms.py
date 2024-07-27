from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SubmitField
from wtforms.validators import InputRequired, Email, Length, ValidationError, DataRequired

class CheckoutForm(FlaskForm):
    firstname = StringField('First Name', validators=[InputRequired(), Length(min=2, max=50)])
    lastname = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    address = StringField('Address', validators=[InputRequired()])
    city = StringField('City', validators=[InputRequired()])
    name_on_card = StringField('Name on Card', validators=[InputRequired(), Length(min=2, max=50)])
    expiration_date = DateField('Expiration Date (MM/YYYY)', format='%m/%Y', validators=[InputRequired()])
    card_number = IntegerField('Card Number', validators=[InputRequired()])
    cvc = IntegerField('CVC', validators=[InputRequired()])

    def validate_card_number(self, card_number):
        if len(str(card_number.data)) != 16:
            raise ValidationError('Invalid card number')

    def validate_cvc(self, cvc):
        if len(str(cvc.data)) != 3:
            raise ValidationError('Invalid CVC')
        
class EditBookingForm(FlaskForm):
    attraction_id = StringField('Attraction ID', validators=[DataRequired()])
    booked_at = DateField('Booked At', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Update Booking')
