from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from .models import User, Attraction, HotelReservation, Cart, CartAttraction, Booking, CardDetails
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .forms import CheckoutForm, EditBookingForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  background_class = 'body-login'
  if request.method == 'POST':
     email = request.form.get('email') # gets the email from the database
     password = request.form.get('password') # gets the password from the database

     user = User.query.filter_by(email=email).first()
     if user:
        if check_password_hash(user.password, password):
           flash('Logged in successfully!', category='success')
           login_user(user, remember=True)
           return redirect(url_for('views.home'))
        else:
           flash('Incorrect password, try again.', category='error')
     else:
       flash('Email does not exist.', category='error')
      
  return render_template("login.html", background_class=background_class)

@auth.route('/logout')
@login_required
def logout():
   logout_user()
   return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    background_class = 'body-sign-up'
    if request.method == 'POST':
        firstname = request.form.get('firstname').strip()
        lastname = request.form.get('lastname').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()
        confirmpassword = request.form.get('confirmpassword').strip()

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(firstname) < 2:
            flash('First Name must be greater than 2 characters.', category='error')
        elif len(lastname) < 2:
            flash('Last Name must be greater than 2 characters.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(password) <= 7:
            flash('Password must be greater than 7 characters.', category='error')
        elif confirmpassword != password:
            flash('Passwords do not match.', category='error')
        else:
            new_user = User(first_name=firstname, last_name=lastname, email=email, password=generate_password_hash(password))
            
            # this logic grants customers with a free guided tour when signing up
            new_user.has_free_tour = True
            
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign-up.html", background_class=background_class)


@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    background_class = 'body-forgot-password'
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            email = email

            user = User.query.filter_by(email=email).first()
            if user:
                new_password = request.form.get('new_password')
                confirm_password = request.form.get('confirm_password')

                if new_password != confirm_password:
                    flash('Passwords do not match.', category='error')
                elif len(new_password) <= 7:
                    flash('Password must be greater than 7 characters.', category='error')
                else:
                    # Update user's password
                    user.password = generate_password_hash(new_password)
                    db.session.commit()

                    flash('Password reset successfully!', category='success')
                    return redirect(url_for('auth.login'))
            else:
                flash('Email does not exist.', category='error')
        else:
            flash('Email field is required.', category='error')

    return render_template("forgot-password.html", background_class=background_class)

@auth.route('/base')
def base2():
   return render_template("base.html")

@auth.route('/base2')
def base():
   return render_template("base2.html")

@auth.route('/discovery-cart-tour')
def discovery_cart_tour():
    background_class = 'body-discovery-cart-tour' #sets a background class for this page
    # This gets the attraction from the database
    attraction = Attraction.query.filter_by(name='Discovery Cart Tour').first()
    return render_template("discovery-cart-tour.html", background_class=background_class, attraction=attraction)

@auth.route('/animals-in-action')
def animals_in_action():
   background_class = 'body-animals-in-action' 
   attraction = Attraction.query.filter_by(name='Animals in Action').first()
   return render_template("animals-in-action.html", background_class=background_class)

@auth.route('/australian-outback-adventure')
def autralian_outback_adventure():
   background_class = 'body-australian-outback-adventure'
   attraction = Attraction.query.filter_by(name='Australian Outback Adventure').first()
   return render_template("australian-outback-adventure.html", background_class=background_class) 

@auth.route('/safari-trail')
def safari_trail():
   background_class = 'body-safari-trail'
   attraction = Attraction.query.filter_by(name='Safari Trail').first()
   return render_template("safari-trail.html", background_class=background_class)

@auth.route('/childrens-zoo')
def childrens_zoo():
   background_class = 'body-childrens-zoo'
   attraction = Attraction.query.filter_by(name='Childrens Zoo').first()
   return render_template("childrens-zoo.html", background_class=background_class)                

@auth.route('/exclusive-experiences')
def exclusive_experiences():
   background_class = 'body-exclusive-experiences'
   attraction = Attraction.query.filter_by(name='Exclusive Experiences').first()
   return render_template("exclusive-experiences.html", background_class=background_class)

@auth.route('/education')
def education():
   background_class = 'body-education'
   return render_template("education.html", background_class=background_class)

@auth.route('/guided-tours')
def guided_tours():
   background_class = 'body-guided-tours'
   attraction = Attraction.query.filter_by(name='Guided Tours').first()
   return render_template("guided-tours.html", background_class=background_class)

@auth.route('/help-center')
def help_center():
   background_class = 'body-help-center'
   return render_template("help-center.html", background_class=background_class)

@auth.route('/materials')
def materials():
   background_class = 'body-materials'
   return render_template("materials.html", background_class=background_class)

@auth.route('/plan-your-stay')
def plan_your_stay():
   background_class = 'body-plan-your-stay'
   return render_template("plan-your-stay.html", background_class=background_class)

@auth.route('/plan-your-visit')
def plan_your_visit():
   background_class = 'body-plan-your-visit'
   return render_template("plan-your-visit.html", background_class=background_class)

@auth.route('/rewards')
def rewards():
   background_class = 'body-rewards'
   return render_template("rewards.html", background_class=background_class)

@auth.route('/school-groups')
def school_groups():
   background_class = 'body-school-groups'
   return render_template("school-groups.html", background_class=background_class)

@auth.route('/things-to-do')
def things_to_do():
   background_class = 'body-things-to-do'
   return render_template("things-to-do.html", background_class=background_class)

@auth.route('/wildlife')
def wildlife():
   background_class = 'body-wildlife'
   return render_template("wildlife.html", background_class=background_class)

@auth.route('/my-cart')
@login_required
def my_cart():
    background_class = 'body-my-cart'
    cart = current_user.cart
    if cart:
        cart_items = [(attraction, cart.quantity, cart.price) for attraction in cart.attractions]
        return render_template("my-cart.html", background_class=background_class, cart_items=cart_items)
    else:
        flash('Cart is empty!', category='info')
        return redirect(url_for('views.home'))

@auth.route('/add-to-cart/<int:attraction_id>')
@login_required
def add_to_cart(attraction_id):
    attraction = Attraction.query.get(attraction_id)
    if attraction:
        cart = current_user.cart
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.session.add(cart)

        quantity = request.args.get('quantity', type=int, default=1)  # Get quantity from query parameters
        if quantity < 1:
            flash('Invalid quantity.', category='error')
            return redirect(url_for('views.home'))

        cart_item = CartAttraction.query.filter_by(cart_id=cart.id, attraction_id=attraction.id).first()
        if not cart_item:
            cart_item = CartAttraction(cart_id=cart.id, attraction_id=attraction.id, quantity=quantity, price=attraction.price)
            db.session.add(cart_item)
        else:
            cart_item.quantity += quantity

        db.session.commit()
        flash('Attraction added to cart successfully!', category='success')
        return redirect(url_for('auth.my_cart'))
    else:
        flash('Attraction not found!', category='error')
        return redirect(url_for('views.home'))
    
@auth.route('/increase-quantity/<int:cart_item_id>')
@login_required
def increase_quantity(cart_item_id):
    cart_item = CartAttraction.query.get_or_404(cart_item_id)
    cart_item.quantity += 1
    db.session.commit()
    flash('Quantity increased!', category='success')
    return redirect(url_for('auth.my_cart'))

@auth.route('/decrease-quantity/<int:cart_item_id>')
@login_required
def decrease_quantity(cart_item_id):
    cart_item = CartAttraction.query.get_or_404(cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        db.session.commit()
        flash('Quantity decreased!', category='success')
    else:
        flash('Minimum quantity reached.', category='error')
    return redirect(url_for('auth.my_cart'))

@auth.route('/remove-from-cart/<int:attraction_id>', methods=['GET', 'POST'])
@login_required
def remove_from_cart(attraction_id):
    attraction = Attraction.query.get(attraction_id)
    if attraction:
        cart = current_user.cart
        if cart:
            cart_attraction = CartAttraction.query.filter_by(cart_id=cart.id, attraction_id=attraction.id).first()
            if cart_attraction:
                db.session.delete(cart_attraction)
                db.session.commit()
                flash('Attraction removed from cart successfully!', category='success')
                return redirect(url_for('auth.bookings'))
            else:
                flash('Attraction not found in cart!', category='error')
    else:
        flash('Attraction not found!', category='error')
    return redirect(url_for('auth.bookings'))

from flask import request

from flask import flash, redirect, url_for

@auth.route('/bookings', methods=['GET', 'POST'])
@login_required
def bookings():
    background_class = 'body-bookings'
    cart = current_user.cart
    if cart:
        attractions = Cart.attractions
    else:
        attractions = []

    form = CheckoutForm()
    bookings = Booking.query.filter_by(user_id=current_user.id).all()

    # Checks if a customer qualifies for a reward
    if not current_user.has_free_tour and not current_user.has_made_booking:
        # Grant a free guided tour
        flash('Congratulations! You have earned a free guided tour.', 'info')
        current_user.has_free_tour = True
        db.session.commit()
    elif not current_user.has_made_booking:
        # provides a discount on first order that a customer books
        flash('Enjoy a 15% discount on your first order.', 'info')

    if form.validate_on_submit():
        flash('Your attraction has been booked!', 'success')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'delete':
            booking_id = request.form.get('booking_id')
            booking = Booking.query.get(booking_id)
            if booking:
                db.session.delete(booking)
                db.session.commit()
                flash('Booking deleted successfully!', 'success')
            else:
                flash('Booking not found!', 'error')
        elif action == 'edit':
            booking_id = request.form.get('booking_id')
            booking = Booking.query.get(booking_id)
            if booking:
                edit_form = EditBookingForm(request.form)
                if edit_form.validate():
                    # updates the booking details for the customer
                    booking.attraction_id = edit_form.attraction_id.data
                    booking.booked_at = edit_form.booked_at.data
                    db.session.commit()
                    flash('Booking updated successfully!', 'success')
                else:
                    flash('Invalid data for editing booking.', 'error')
            else:
                flash('Booking not found!', 'error')

    return render_template("bookings.html", background_class=background_class, attractions=attractions, form=form, bookings=bookings)

@auth.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    form = CardDetails(request.form)
    
    # Check if the user has made any bookings
    has_bookings = Booking.query.filter_by(user_id=current_user.id).first()
    
    # Apply discount if the user has no bookings
    discount = 0
    if not has_bookings:
        discount = 15
    
    if request.method == 'POST' and form.validate():
        # this extracts the form data
        firstname = form.firstname.data.strip()
        lastname = form.lastname.data.strip()
        email = form.email.data.strip()
        address = form.address.data.strip()
        city = form.city.data.strip()
        name_on_card = form.name_on_card.data.strip()
        expiration_date = form.expiration_date.data.strip()
        card_number = form.card_number.data.strip()
        cvc = form.cvc.data.strip()
        
        # this hashes sensitive customer information
        hashed_card_number = generate_password_hash(card_number)
        hashed_cvc = generate_password_hash(cvc)
        
        order = CardDetails (
            firstname=firstname,
            lastname=lastname,
            email=email,
            address=address,
            city=city,
            name_on_card=name_on_card,
            expiration_date=expiration_date,
            card_number=hashed_card_number,
            cvc=hashed_cvc
        )
        # this saves the customers order to the database
        db.session.add(order)
        db.session.commit()
        # Apply discount to the total price
        total_price = calculate_total_price()  # this function calculates the total price
        discounted_price = total_price * (1 - discount / 100)
        # this clears the customers cart after they have completed a successful checkout
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart:
            cart.items.clear()
            db.session.commit()
        flash('Your order has been placed successfully!', category='success')
        return redirect(url_for('views.home'))

    return render_template('checkout.html', form=form, discount=discount)

def calculate_total_price():
    # this retrieves the customers cart
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    # this sets the total price to 0
    total_price = 0
    # calculates the total price based on the items in the customers cart
    if cart:
        # calculates the total price of attractions
        for attraction in cart.attractions:
            total_price += attraction.price * cart.quantity
        # Calculates the total price of hotel reservations
        for reservation in cart.hotel_reservations:
            total_price += reservation.total_price
    return total_price

@auth.route('/edit-booking/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def edit_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    form = EditBookingForm()

    if form.validate_on_submit():
        booking.attraction_id = form.attraction_id.data
        booking.booked_at = form.booked_at.data

        db.session.commit()

        flash('Booking updated successfully!', category='success')
        return redirect(url_for('auth.bookings'))

    form.attraction_id.data = booking.attraction_id
    form.booked_at.data = booking.booked_at

    return render_template('bookings.html', form=form)


