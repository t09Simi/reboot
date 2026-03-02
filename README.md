# ⚡ Reboot

> A platform for career gapers and self-taught beginners 
> breaking into the software industry.

## About
Reboot helps people who took a career break or are teaching 
themselves tech break into the software industry. It provides 
structured roadmaps, concept testing, community, and mentorship 
— all in one place.

## Built With
- Python 3.12
- Django 5.0
- PostgreSQL
- Bootstrap 5

## Current Features
- [x] Custom user authentication (career gaper / mentor roles)
- [x] User registration and login
- [x] Career gaper and mentor profiles
- [x] Testimonial submission and approval workflow
- [ ] Profile completion with progress bar
- [ ] Roadmaps and concept testing
- [ ] Community forums
- [ ] Mentor matching

## Local Development Setup

### Prerequisites
- Python 3.12+
- PostgreSQL

### Installation
1. Clone the repository
   git clone https://github.com/yourusername/reboot.git
   cd reboot

2. Create virtual environment
   python -m venv venv
   source venv/bin/activate

3. Install dependencies
   pip install -r requirements.txt

4. Create .env file
   cp .env.example .env

5. Run migrations
   python manage.py migrate

6. Create superuser
   python manage.py createsuperuser

7. Run development server
   python manage.py runserver