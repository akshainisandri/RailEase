from flask_sqlalchemy import SQLAlchemy
from app import app, db, Question  # Importing the app and database from your Flask app

# List of questions and answers
questions_data = [
    {"question": "What are the facilities available at Secunderabad Station?", "answer": "Secunderabad Station offers a variety of facilities, including ticket counters, restrooms, food courts, waiting areas, and more."},
    {"question": "How can I find live train updates?", "answer": "You can find live train updates on the Indian Railways website (e.g., erail.in) or through various train tracking apps."},
    {"question": "Are there any hotels near the station?", "answer": "Yes, there are several hotels located near Secunderabad Station. You can find a list of them on our website's 'Nearby Hotels' page."},
    {"question": "What restaurants are available near the station?", "answer": "There are many restaurants near Secunderabad Station, offering various cuisines. Check our 'Nearby Restaurants' page for details."},
    {"question": "How do I contact customer support?", "answer": "You can contact our customer support through the contact form on our website or by calling us at (123) 456-7890."},
    {"question": "Is there parking available at the station?", "answer": "Yes, there is parking available for both two-wheelers and four-wheelers at Secunderabad Station."},
    {"question": "What are the timings of the local trains?", "answer": "You can check the timings of local trains on the official South Central Railway website or through various train apps."},
    {"question": "How can I book a retiring room at the station?", "answer": "You can book a retiring room at Secunderabad Station online through the IRCTC website or at the station's booking counter."},
    {"question": "Are there any ATMs at the station?", "answer": "Yes, there are ATMs from various banks located within the station premises."},
    {"question": "Where can I find information about lost and found items?", "answer": "You can inquire about lost and found items at the station's Railway Protection Force (RPF) office."},
    {"question": "What are the different types of tickets available?", "answer": "Secunderabad Station offers various ticket types, including reserved, unreserved, platform tickets, and season passes."},
    {"question": "How can I cancel my train ticket?", "answer": "You can cancel your train ticket online through the IRCTC website or at the station's reservation counter."},
    {"question": "Are there any waiting rooms at the station?", "answer": "Yes, there are waiting rooms available for passengers at Secunderabad Station."},
    {"question": "Is there a cloakroom facility at the station?", "answer": "Yes, a cloakroom facility is available at Secunderabad Station for passengers to store their luggage."},
    {"question": "How can I reach the airport from Secunderabad Station?", "answer": "You can reach the airport from Secunderabad Station by taxi, bus, or the airport liner train."},
    {"question": "Are there any bookstalls at the station?", "answer": "Yes, there are bookstalls at Secunderabad Station where you can purchase books and magazines."},
    {"question": "Is there a Wi-Fi facility available at the station?", "answer": "Yes, Wi-Fi is available at Secunderabad Station. You may need to register your mobile number to use it."},
    {"question": "What is the customer care number for Secunderabad Station?", "answer": "You can contact the Secunderabad Station customer care at (mention a valid number if available)."},
    {"question": "How can I complain about any issue at the station?", "answer": "You can lodge a complaint at the station manager's office or through the online complaint portal on the railway website."},
    {"question": "Are there any special assistance services for senior citizens and disabled passengers?", "answer": "Yes, Secunderabad Station provides special assistance services for senior citizens and disabled passengers. Please contact the station staff for assistance."},
    {"question": "What are the nearby tourist attractions from Secunderabad Station?", "answer": "Secunderabad Station is close to several tourist attractions, including Charminar, Golconda Fort, and Birla Mandir."},
    {"question": "How can I find information about train arrivals and departures?", "answer": "You can find information about train arrivals and departures on the display boards at the station or through online train tracking websites/apps."},
    {"question": "Are there any food courts on the platforms?", "answer": "Yes, there are food courts available on some platforms at Secunderabad Station."},
    {"question": "Is there a medical facility at the station?", "answer": "Yes, there is a basic medical facility available at Secunderabad Station for emergencies."},
    {"question": "How can I pre-book a taxi from the station?", "answer": "You can pre-book a taxi through various online taxi booking apps or by contacting local taxi services."},
    {"question": "Are there any cyber cafes near Secunderabad Station?", "answer": "Yes, there are cyber cafes located near Secunderabad Station."},
    {"question": "What is the pin code of Secunderabad Railway Station?", "answer": "The pin code of Secunderabad Railway Station is (mention the correct pin code)."},
    {"question": "Are there any waiting rooms for ladies at the station?", "answer": "Yes, there are separate waiting rooms for ladies at Secunderabad Station."},
    {"question": "How can I get a platform ticket?", "answer": "You can purchase a platform ticket from the ticket counters at the station."},
    {"question": "Is there a bus service from Secunderabad Station to other parts of the city?", "answer": "Yes, there are regular bus services from Secunderabad Station to various parts of Hyderabad and Secunderabad."},
    {"question": "How do I reach the metro station from Secunderabad Railway Station?", "answer": "The Secunderabad Metro Station is adjacent to the railway station and is easily accessible by walking."}
]

# Function to populate the database
def populate_database():
    with app.app_context():
        db.create_all()  # Ensure the database tables are created
        
        # Insert only if database is empty
        if not Question.query.first():
            for item in questions_data:
                question = Question(question=item["question"], answer=item["answer"])
                db.session.add(question)
            db.session.commit()
            print("✅ Database populated with 30+ questions!")
        else:
            print("⚠️ Database already contains data. No new entries added.")

# Run the function
if __name__ == "__main__":
    populate_database()
