# ⚡ Reboot

> You took a break. Now let's restart.

A full-stack platform helping career gapers and self-taught beginners break into tech — with mentor matching, real-time job market intelligence, and an AI Career Buddy (coming soon).

🌐 **Live demo:** [https://reboot-bllo.onrender.com](https://reboot-bllo.onrender.com)

---

## The Problem

Breaking into tech is hard. Breaking back in after a career gap is even harder.

Most platforms assume you already have experience, a degree, or a network. Reboot is built for people who don't — yet.

---

## What It Does

**For Career Gapers:**
- A personalised dashboard with profile completion tracking
- **Live job trends widget** — top skills, roles, and companies in the market right now, with week-over-week growth indicators
- A job roles explorer organised by IT domain
- Access to mentors who've been where they are

**For Mentors:**
- A request inbox with one-click accept/decline
- Notifications when a career gaper reaches out
- Tools to manage mentee relationships

---

## Screenshots


## Next

- AI Career Buddy — personalised guidance via Claude API
- Real-time JSearch API integration (replacing mock data)
- Scheduled weekly data fetches (Celery Beat or Render Cron)

## Future

- Session scheduling between mentor and mentee
- Testimonials with mentor approval workflow
- Community forums
- Industry news feed

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.14, Django 5.0 |
| **Frontend** | React, Recharts, JWT authentication |
| **Database** | SQLite (development), PostgreSQL (production) |
| **Containerisation** | Docker, docker-compose (multi-container local dev) |
| **Hosting** | Render (Docker web service + Static Site + managed Postgres) |
| **Coming soon** | Claude API, Celery + Redis (for scheduled real data fetches), JSearch integration |

---

## Local Development Setup

### With Docker

```bash
git clone https://github.com/t09Simi/reboot.git
cd reboot
docker compose up --build
```

Then inside the running web container:

```bash
docker compose exec web python manage.py seed_skills
docker compose exec web python manage.py seed_mock_listings --wipe
docker compose exec web python manage.py compute_trends --window 30
docker compose exec web python manage.py createsuperuser
```

Backend at `http://localhost:8000`, frontend at `http://localhost:3000` (after `cd frontend && npm start`).

---