from models import Attraction, db

# Create instances of the Attraction model for new attractions
discovery_cart_tour = Attraction(name='Discovery Cart Tour')
animals_in_action = Attraction(name='Animals in Action')
childrens_zoo = Attraction(name='Childrens Zoo')
safari_trail = Attraction(name='Safari Trail')
exclusive_experiences = Attraction(name='Exclusive Experiences')
guided_tours = Attraction(name='Guided Tours')
Autralian_Outback_Adventure = Attraction(name='Australian Outback Adventure')

# Add the instances to the session
db.session.add(discovery_cart_tour)
db.session.add(animals_in_action)
db.session.add(childrens_zoo)
db.session.add(safari_trail)
db.session.add(exclusive_experiences)
db.session.add(guided_tours)
db.session.add(Autralian_Outback_Adventure)

# Commit the session to save the changes to the database
db.session.commit()
