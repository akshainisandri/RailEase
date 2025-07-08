from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///railease.db'  # Ensure correct DB path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Hotel model
class Hotel(db.Model):
    __tablename__ = "hotels"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    booking_url = db.Column(db.String(255), nullable=False)

# Define Restaurant model
class Restaurant(db.Model):
    __tablename__ = "restaurants"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    location_url = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Float, nullable=False)

# Function to reset and populate the database
def reset_database():
    with app.app_context():
        if os.path.exists("app.db"):
            os.remove("app.db")

        db.create_all()  # Create new tables

        # ✅ Define `hotels` inside the function
        hotels = [
            Hotel(name="The Grand Solitaire", price=1800, rating=4.7,
                  image="static/images/hotel1.jpg",
                  booking_url="https://www.google.com/travel/search?q=grand+solitaire+hyderabad"),
            Hotel(name="Welkin Hotel", price=1200, rating=4.3,
                  image="static/images/hotel2.jpg",
                  booking_url="https://www.google.com/travel/search?q=welkin+hotel+hyderabad"),
            Hotel(name="Heritage Inn", price=1500, rating=4.5,
                  image="images/hotel3.jpg",
                  booking_url="https://www.google.com/travel/search?q=heritage+inn"),
            Hotel(name="The Central Court Hotel", price=1400, rating=4.1,
                  image="static/images/hotel4.jpg",
                  booking_url="https://www.google.com/travel/search?q=central+court+hotel+secunderabad"),
            Hotel(name="Hyderabad Marriott Hotel & Convention Centre", price=2000, rating=4.9,
                  image="static/images/hotel5.jpg",
                  booking_url="https://www.google.com/travel/search?q=hyderabad+marriott+hotel+secunderabad")
        ]


        # ✅ Define `restaurants` inside the function
        restaurants = [
            Restaurant(name="Paradise Restaurant", price=400, type="non-veg", rating=4.5,
                       image="static/images/paradise.jpg",
                       location_url="https://www.google.com/maps/search/?api=1&query=Paradise+Restaurant+Secunderabad"),
            Restaurant(name="Subbaya Gari Hotel", price=350, type="veg", rating=4.7,
                       image="../static/images/subbaya.jpg",
                       location_url="https://www.google.com/maps/search/?api=1&query=Subbaya+Gari+Hotel+Secunderabad"),
            Restaurant(name="Alpha Restaurant", price=300, type="non-veg", rating=4.4,
                       image="static/images/alpha.jpg",
                       location_url="https://www.google.com/maps/search/?api=1&query=Alpha+Restaurant+Secunderabad"),
            Restaurant(name="Kaadhale Restaurant", price=250, type="veg", rating=4.3,
                       image="static/images/kadhale.jpg",
                       location_url="https://www.google.com/maps/search/?api=1&query=Kaadhale+Restaurant+Secunderabad"),
            Restaurant(name="Taj Tristar", price=500, type="non-veg", rating=4.6,
                       image="static/images/taj.jpg",
                       location_url="https://www.google.com/maps/search/?api=1&query=Taj+Tristar+Secunderabad")
        ]

        # ✅ Now `hotels` and `restaurants` exist inside this function
        db.session.add_all(hotels + restaurants)
        db.session.commit()

        print("✅ Database setup complete!")

# Run database setup
if __name__ == "__main__":
    reset_database()
