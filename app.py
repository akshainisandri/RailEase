from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///railease.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)

# ========== MODELS ==========
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    feedback = db.Column(db.Text, nullable=False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    message = db.Column(db.Text, nullable=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Text, nullable=False)

class Hotel(db.Model):
    __tablename__ = "hotels"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    booking_url = db.Column(db.String(255), nullable=False)

class Restaurant(db.Model):
    __tablename__ = "restaurants"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    location_url = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Float, nullable=False)

# Lost and Found Models
class FoundItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    date_found = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(200))
    is_claimed = db.Column(db.Boolean, default=False)

class Enquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('found_item.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    item = db.relationship('FoundItem', backref='enquiries')

# ========== INITIALIZATION ==========
with app.app_context():
    db.create_all()

# ========== ROUTES ==========

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
def main():
    questions = Question.query.all()
    return render_template('main.html', questions=questions)

@app.route('/get-questions', methods=['GET'])
def get_questions():
    questions = Question.query.all()
    return jsonify([{"id": q.id, "question": q.question} for q in questions])

@app.route('/get-answer/<int:question_id>', methods=['GET'])
def get_answer(question_id):
    question = Question.query.get(question_id)
    if question:
        return jsonify({"answer": question.answer})
    return jsonify({"error": "Question not found"}), 404

# Admin login for Feedback/Contact
@app.route('/admin-login-feedback', methods=['POST'])
def admin_login_feedback():
    if request.form.get('password') == 'admin123':
        session['admin_feedback'] = True
    return redirect(url_for('view_feedback'))

@app.route('/admin-logout-feedback')
def admin_logout_feedback():
    session.pop('admin_feedback', None)
    return redirect(url_for('view_feedback'))

@app.route('/admin-login-contact', methods=['POST'])
def admin_login_contact():
    if request.form.get('password') == 'admin456':
        session['admin_contact'] = True
    return redirect(url_for('view_contacts'))

@app.route('/admin-logout-contact')
def admin_logout_contact():
    session.pop('admin_contact', None)
    return redirect(url_for('view_contacts'))

# ======= Lost and Found Feature =======
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'pass123'

@app.route('/lost')
def lost_home():
    return render_template('lost.html')

@app.route('/lost-items')
def lost_items():
    items = FoundItem.query.filter_by(is_claimed=False).all()
    return render_template('lost_items.html', items=items)

@app.route('/admin/login', methods=['POST'])
def admin_login():
    if request.form['username'] == ADMIN_USERNAME and request.form['password'] == ADMIN_PASSWORD:
        session['admin_logged_in'] = True
        flash("Logged in successfully.")
    else:
        flash("Invalid credentials.")
    return redirect(url_for('lost_home'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash("Logged out successfully.")
    return redirect(url_for('lost_home'))

@app.route('/enquire/<int:item_id>', methods=['POST'])
def enquire(item_id):
    enquiry = Enquiry(
        item_id=item_id,
        name=request.form['name'],
        contact=request.form['contact'],
        message=request.form['message']
    )
    db.session.add(enquiry)
    db.session.commit()
    flash("Enquiry submitted!")
    return redirect(url_for('lost_items'))

@app.route('/admin/upload', methods=['GET', 'POST'])
def admin_upload():
    if not session.get('admin_logged_in'):
        return redirect(url_for('lost_home'))

    if request.method == 'POST':
        item = FoundItem(
            item_name=request.form['item_name'],
            date_found=request.form['date_found'],
            location=request.form['location']
        )

        image = request.files.get('image')
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            item.image_path = f'uploads/{filename}'

        db.session.add(item)
        db.session.commit()
        flash("Item uploaded successfully.")
        return redirect(url_for('lost_items'))

    return render_template('admin_upload.html')

@app.route('/admin/enquiries')
def view_enquiries():
    if not session.get('admin_logged_in'):
        return redirect(url_for('lost_home'))
    enquiries = Enquiry.query.order_by(Enquiry.timestamp.desc()).all()
    return render_template('admin_enquiries.html', enquiries=enquiries)

@app.route('/admin/claim/<int:item_id>', methods=['POST'])
def mark_as_claimed(item_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('lost_home'))
    item = FoundItem.query.get_or_404(item_id)
    item.is_claimed = True
    db.session.commit()
    flash("Item marked as claimed.")
    return redirect(url_for('lost_items'))

# ======= Recommendation Feature =======
@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    data = request.json
    budget = int(data.get('budget', 10000))
    food_preference = data.get('food_preference', 'all')

    hotels = Hotel.query.all()
    restaurants = Restaurant.query.filter_by(type=food_preference).all() if food_preference != "all" else Restaurant.query.all()

    best_combo = None
    best_rating = 0

    for hotel in hotels:
        for restaurant in restaurants:
            total_cost = hotel.price + restaurant.price
            avg_rating = (hotel.rating + restaurant.rating) / 2
            if total_cost <= budget and avg_rating > best_rating:
                best_rating = avg_rating
                best_combo = {
                    "hotels": [{
                        "name": hotel.name,
                        "price": hotel.price,
                        "rating": hotel.rating,
                        "image": url_for('static', filename=f'images/{hotel.image}'),
                        "booking_url": hotel.booking_url
                    }],
                    "restaurants": [{
                        "name": restaurant.name,
                        "price": restaurant.price,
                        "type": restaurant.type,
                        "rating": restaurant.rating,
                        "image": url_for('static', filename=f'images/{restaurant.image}'),
                        "location_url": restaurant.location_url
                    }]
                }

    if best_combo:
        return jsonify(best_combo)

    # Fallback to best restaurant only
    best_restaurant = max(
        [r for r in restaurants if r.price <= budget],
        key=lambda x: x.rating,
        default=None
    )
    if best_restaurant:
        return jsonify({
            "message": "No combo found. But here's a restaurant recommendation:",
            "restaurant": {
                "name": best_restaurant.name,
                "price": best_restaurant.price,
                "type": best_restaurant.type,
                "rating": best_restaurant.rating,
                "image": best_restaurant.image,
                "location_url": best_restaurant.location_url
            }
        })

    return jsonify({"error": "No options available within budget."}), 404

# ======= Static Routes =======
@app.route('/restaurants')
def restaurants(): return render_template('restaurants.html')

@app.route('/auto')
def auto(): return render_template('auto.html')

@app.route('/hotels')
def hotels(): return render_template('hotels.html')

@app.route('/package')
def package(): return render_template('package.html')

@app.route('/facility-finder')
def facility_finder(): return render_template('facility-finder.html')

@app.route('/cloak')
def cloak(): return render_template('cloak.html')

@app.route('/food')
def food(): return render_template('food.html')

@app.route('/parking')
def parking(): return render_template('parking.html')

@app.route('/ticket-counters')
def ticket_counters(): return render_template('ticket-counters.html')

@app.route('/emergency')
def emergency(): return render_template('emergency.html')

@app.route('/waiting-rooms')
def waiting_rooms(): return render_template('waiting_rooms.html')

@app.route('/washrooms')
def washrooms(): return render_template('washrooms.html')

@app.route('/tourist-attractions')
def tourist_attractions(): return render_template('tourist-attractions.html')

@app.route('/feedback')
def feedback(): return render_template('feedback.html')

@app.route('/contact')
def contact(): return render_template('contact.html')

@app.route('/wheel')
def wheelchair(): return render_template('wheel.html')

@app.route('/train')
def train(): return render_template('train-updates.html')

@app.route('/veg')
def veg(): return render_template('veg.html')

@app.route('/nonveg')
def nonveg(): return render_template('nonveg.html')

# ======= Feedback/Contact Logic =======
@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    feedback_text = request.form['feedback']
    existing = Feedback.query.filter_by(email=email).first()
    if existing:
        flash("You have already submitted feedback!", "warning")
    else:
        db.session.add(Feedback(name=name, email=email, feedback=feedback_text))
        db.session.commit()
        flash("Thank you for your feedback!", "success")
    return redirect(url_for('view_feedback'))

@app.route('/view-feedback')
def view_feedback():
    feedbacks = Feedback.query.all()
    return render_template('view_feedback.html', feedbacks=feedbacks)

@app.route('/delete-feedback/<int:feedback_id>', methods=['POST'])
def delete_feedback(feedback_id):
    if not session.get('admin_feedback'):
        return redirect(url_for('view_feedback'))
    feedback = Feedback.query.get(feedback_id)
    if feedback:
        db.session.delete(feedback)
        db.session.commit()
    return redirect(url_for('view_feedback'))

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    existing = Contact.query.filter_by(email=email).first()
    if existing:
        flash("You have already submitted a message!", "warning")
    else:
        db.session.add(Contact(name=name, email=email, message=message))
        db.session.commit()
        flash("Message sent successfully!", "success")
    return redirect(url_for('view_contacts'))

@app.route('/view-contacts')
def view_contacts():
    contacts = Contact.query.all()
    return render_template('view_contacts.html', contacts=contacts)

@app.route('/delete-contact/<int:contact_id>', methods=['POST'])
def delete_contact(contact_id):
    if not session.get('admin_contact'):
        return redirect(url_for('view_contacts'))
    contact = Contact.query.get(contact_id)
    if contact:
        db.session.delete(contact)
        db.session.commit()
    return redirect(url_for('view_contacts'))

if __name__ == '__main__':
    app.run(debug=True)
