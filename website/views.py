#stores URL endpoints for front-end functioning

from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/Riget-Zoo-Adventures')
def home():
  background_class = 'body-home' #links the background class and specific styling for the background image of this page
  return render_template("home.html", background_class=background_class)



