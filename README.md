# Fasal Sathi

Fasal Sathi is a mobile and web-based platform designed to bridge the gap between farmers and storage providers, optimizing agricultural logistics and resource management. The platform enables farmers to find and reserve storage facilities while allowing storage providers to list their spaces, fostering transparency and trust through user reviews and location-based recommendations.

---

## Features

- **For Farmers:**
  - Search for storage spaces based on location and requirements.
  - View and compare storage options with detailed information.
  - Leave reviews to help other farmers make informed decisions.

- **For Storage Providers:**
  - List storage spaces with descriptions, pricing, and location details.
  - Manage listings and respond to inquiries efficiently.
  - Gain visibility and attract farmers through the platform.

- **Enhanced Matchmaking:**
  - Location-based recommendations improve the accuracy of matches by 40%.
  - User reviews and ratings enhance trust and transparency.

---

## Technologies Used

- **Backend:** Django, PostgreSQL
- **Frontend:** ReactJS & Android(Kotlin)
- **API:** RESTful APIs for seamless communication between frontend and backend.
- **Database:** PostgreSQL for efficient data storage and retrieval.

---

## Installation and Setup

1. Clone the repository:
   ```bash
   https://github.com/adavadkardhruv13/fasal_saathi.git
   ```

2. Set up a virtual environment and install dependencies:
   ```bash
   python3 -m venv env
   source env/bin/activate  # For Windows, use `env\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Run the development server:
   ```bash
   python manage.py runserver
   ```

---

## Usage

1. Access the platform at `http://127.0.0.1:8000/` after running the server.
2. Farmers can:
   - Search for and book storage facilities.
   - Leave reviews for storage spaces.
3. Storage providers can:
   - List and manage storage facilities.
   - Monitor bookings and inquiries.

---
