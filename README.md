# 🚆 RailEase

**RailEase** is a web application designed to make travel through **Secunderabad Railway Station** smooth, stress-free, and traveler-friendly.

It provides:
- 🔍 In-station navigation to help passengers find ticket counters, restrooms, waiting rooms, and food courts.
- ⏱️ Real-time train platform and schedule updates using third-party APIs.
- 💬 An **Ease Assistant Chatbot** to answer common queries instantly.
- 🏨 Recommendations for nearby hotels and restaurants for long layovers.
- 📢 Emergency contact access for quick help.
- 🗂️ An admin panel to manage passenger feedback and contact messages.

---

## 📌 Project Overview

Secunderabad Railway Station is one of India’s busiest stations. Many travelers struggle with:
- Finding essential facilities inside the station.
- Keeping up with sudden platform changes or delays.
- Locating safe nearby stays and food options.
- Getting quick help during emergencies.

**RailEase** addresses these gaps by combining real-time updates, easy navigation, chatbot support, and emergency access — all in one web-based platform.

---

## ⚙️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python Flask
- **Database:** SQLite with SQLAlchemy ORM
- **APIs:** eRail API for live train data, Google Places API for nearby recommendations

---

## 🚀 How to Run Locally

1. **Clone this repo**

   git clone https://github.com/YOUR_USERNAME/RailEase.git  
   cd RailEase

2. **Create & activate a virtual environment**

   python -m venv venv  
   source venv/bin/activate  # Windows: venv\Scripts\activate

3. **Install dependencies**

   pip install -r requirements.txt

4. **Set up the database**

   python setup_db.py  
   python populate_db.py

5. **Run the app**

   python app.py

6. Open [http://localhost:5000](http://localhost:5000) in your browser 🚉

---

## ✅ Main Features

- **Integrated Navigation:** Interactive maps and station guide.
- **Live Train Updates:** Real-time schedule & platform info.
- **Ease Assistant Chatbot:** Instant answers to FAQs.
- **Feedback & Contact:** User feedback system stored in SQLite.
- **Admin Panel:** Manage messages & feedback securely.
- **Emergency Module:** Quick dial to emergency contacts.

---

## 🔒 License

© 2025 Akshaini Sandri — All rights reserved.

This project is **proprietary** and not licensed for reuse, modification, or distribution without written permission.

---

## 🙌 Author

**Akshaini Sandri**  
B.Tech CSE | CVR College of Engineering  
Third year,Fifth Semester

> RailEase — making station travel smart, simple, and stress-free!
