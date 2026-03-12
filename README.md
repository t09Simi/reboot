# ⚡ Reboot

> You took a break. Now let's restart.

Reboot is a platform built for career gapers and self-taught beginners who want to break into the tech industry. It connects them with mentors, shows them exactly what the job market expects, and will soon give them an AI buddy to guide them through closing their skill gaps — step by step, without judgment.

---

## The Problem

Breaking into tech is hard. Breaking back in after a career gap is even harder.

Most platforms assume you already have experience, a degree, or a network. Reboot is built for people who don't — yet.

---

## Who Is It For

**Career Gapers** — people who took time off from their careers and want to re-enter the tech industry with the right skills and support.

**Self-taught Beginners** — people teaching themselves to code with no formal degree or prior tech experience.

**Mentors** — experienced tech professionals who want to give back by guiding the next generation of developers.

---

## What Reboot Offers

### For Career Gapers
- A personalised dashboard showing profile completion and next steps
- A job roles explorer showing exactly what skills the market expects for each role, organised by domain
- A community to connect with people who understand the journey
- Access to mentors who have been where they are
- An AI Career Buddy (coming soon) to guide them through closing skill gaps

### For Mentors
- A discovery feed showing career gapers who need guidance
- Tools to schedule mentorship sessions
- A requests and inbox system for managing mentee relationships
- The ability to share resources with mentees

---

## Current Features

- [x] Custom user authentication with role based access (Career Gaper / Mentor)
- [x] Role based registration and login
- [x] Automatic profile creation via Django signals
- [x] Career Gaper profile with completion tracking and progress bar
- [x] Mentor dashboard — incoming requests with Accept / Decline actions
- [x] Mentorship request system — career gapers send requests with a     message
- [x] Notifications for both sides — mentor notified on new request, career gaper notified on response
- [x] Job roles explorer organised by IT domain

## Coming Soon

- [ ] Session scheduling between mentor and career gaper
- [ ] Testimonials — submission, mentor approval, admin publish
- [ ] AI Career Buddy — personalised guidance via Claude API
- [ ] Community forums
- [ ] Industry news feed
- [ ] REST API with Django REST Framework
- [ ] React frontend
- [ ] Docker deployment
- [ ] CI/CD pipeline

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, Django 5.0 |
| Frontend | Bootstrap 5, Custom CSS |
| Database | SQLite (development), PostgreSQL (production) |
| Auth | Django Auth with custom User model |
| Admin | Django Admin |
| Coming Soon | Django REST Framework, Docker, Claude API, Celery, Redis, Kafka |

---

## Local Development Setup

### Prerequisites
- Python 3.12+
- pip

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/t09Simi/reboot.git
cd reboot
```

**2. Create and activate virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create `.env` file**
```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
```

**5. Run migrations**
```bash
python manage.py migrate
```

**6. Create superuser**
```bash
python manage.py createsuperuser
```

**7. Run development server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

---