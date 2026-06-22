# INFY Real Estate - Installation Guide

## India's Smartest AI Powered Real Estate Platform

---

## Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Installation Steps

```bash
# 1. Navigate to project directory
cd infy_real_estate

# 2. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate property images
python3 generate_images.py

# 5. Seed the database
python3 seed_data.py

# 6. Run the application
python3 app.py
```

### Access the Application
- **Website:** http://localhost:5000
- **Admin Panel:** http://localhost:5000/admin

---

## Login Credentials

| Role   | Email            | Password  |
|--------|------------------|-----------|
| Admin  | admin@infy.com   | admin123  |
| Buyer  | buyer@infy.com   | buyer123  |
| Agent  | agent@infy.com   | agent123  |

---

## Project Structure

```
infy_real_estate/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── seed_data.py           # Database seeder
├── generate_images.py     # Image generator
├── INSTALL.md             # This file
├── ai_modules/            # AI/ML modules
│   ├── price_predictor.py # Price prediction engine
│   ├── investment_scorer.py # Investment scoring
│   ├── trust_scorer.py    # Scam detection
│   ├── growth_predictor.py # Growth & neighborhood AI
│   └── chatbot.py         # INFY AI chatbot
├── routes/                # Flask route blueprints
│   ├── main.py            # Landing page routes
│   ├── auth.py            # Authentication routes
│   ├── properties.py      # Property listing routes
│   ├── dashboard.py       # User dashboard routes
│   ├── admin.py           # Admin panel routes
│   └── ai_routes.py       # AI tool routes
├── templates/             # Jinja2 HTML templates
│   ├── base.html          # Base layout
│   ├── index.html         # Landing page
│   ├── auth/              # Login, register, etc.
│   ├── properties/        # Listing, detail, search
│   ├── dashboard/         # User dashboard
│   ├── admin/             # Admin panel
│   └── ai/               # AI tools (predictor, chatbot)
└── static/
    ├── css/style.css      # Premium CSS styling
    └── images/properties/ # Property images (SVG)
```

---

## Features

### AI-Powered Tools
- **Price Predictor** - ML-powered 1/3/5 year forecasts
- **Investment Analyzer** - Score 0-100 with ROI analysis
- **Trust Score** - Scam detection and verification
- **Growth Predictor** - Infrastructure impact analysis
- **INFY AI Chat** - Conversational assistant
- **Neighborhood Intelligence** - Area quality scores
- **Negotiation Assistant** - Fair price calculation

### Core Features
- User registration, login, logout, password reset
- Property listing with 20+ filters
- Property detail with full AI insights
- Save/favorite properties
- Compare up to 5 properties
- User dashboard with history
- Admin panel (CRUD for properties, users, cities)
- Mobile responsive design
- Premium glassmorphism UI

---

## Technology Stack
- **Backend:** Python, Flask
- **Database:** SQLite
- **AI/ML:** NumPy (simulated ML models)
- **Frontend:** Jinja2, HTML, CSS (no JavaScript frameworks)
- **Auth:** Flask-Login, Werkzeug password hashing
- **Security:** CSRF protection, input validation

---

## Database Reset
To reset and reseed the database:
```bash
python3 seed_data.py
```

## Production Deployment
For production, set environment variables:
```bash
export SECRET_KEY='your-production-secret-key'
export DATABASE_URL='postgresql://user:pass@host/dbname'
```
