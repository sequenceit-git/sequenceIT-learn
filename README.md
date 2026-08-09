# SequenceIT Learn

> **A modern, open-source Learning Management System** built with Django — designed for schools, colleges, and organizations who want full control over their e-learning platform.

[![Django CI/CD](https://github.com/sequenceit-git/sequenceIT-learn/actions/workflows/django.yml/badge.svg)](https://github.com/sequenceit-git/sequenceIT-learn/actions/workflows/django.yml)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Django 4.0](https://img.shields.io/badge/Django-4.0-green?logo=django)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ Features

### 👥 User Management
- Role-based access: **Admin**, **Lecturer**, and **Student**
- Admin manages students and lecturers (Add, Update, Delete)
- Custom user profiles with avatar support
- Secure login, logout, and password reset

### 📚 Academic Management
- Session/year and semester management
- Program & course management with allocation
- Students can add and drop courses
- Lecturers submit scores: *Attendance, Mid Exam, Final Exam, Assignment*
- System auto-calculates: *Total, Average, GPA, and Grade*
- Grade comment: **Pass**, **Fail**, or **Pass with Warning**
- Assessment and grade result pages for students
- PDF generation for registration slips and grade results

### 🧠 Quiz & Assessment
- Multiple choice, True/False question types
- Essay type *(Coming soon)*
- Question order randomization
- One attempt limit per user (optional)
- Questions grouped by category
- Pass mark configuration
- Detailed per-question explanations
- Progress tracking per category
- Quiz marking page for lecturers (can be filtered by quiz or user)
- Logged-in users can resume incomplete quizzes

### 📊 Dashboard & Analytics
- Admin-only school demographics dashboard
- News & Events for all users
- Search across courses, programs, quizzes, and events

### 🌍 Internationalization
- Multi-language support: **English, French, Spanish, Russian**
- Language switcher built into the UI

### 💳 Payments
- Stripe integration for course payments
- GoPay support

### 🎨 UI / UX
- Premium dark-mode-ready UI with glassmorphism effects
- Responsive sidebar with animated **"S"** brand icon
- Smooth SPA-style page transitions (no full reload)
- Built with Bootstrap 5, Lucide Icons, and Outfit font

---

## 🚀 Deployment

SequenceIT Learn is production-ready with a full Docker + CI/CD setup.

### Stack
| Component | Technology |
|-----------|-----------|
| App server | Gunicorn (Django WSGI) |
| Database | PostgreSQL 15 |
| Reverse proxy | Traefik (auto TLS via Let's Encrypt) |
| Container | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Live URL | [sms-demo.sequenceit.software](https://sms-demo.sequenceit.software) |

### CI/CD Pipeline

Every push to `main` triggers 3 automatic stages:

```
Push to main
     │
     ▼
🧪 Test          — Django test suite (Python 3.10 & 3.11)
     │ passes
     ▼
🐳 Build & Push  — Docker image → Docker Hub (tagged latest + SHA)
     │ passes
     ▼
🚀 Deploy        — SSH into VPS → pull latest image → restart container
```

### Required GitHub Secrets

Set these in **Settings → Secrets and variables → Actions**:

| Secret | Description |
|--------|-------------|
| `VPS_HOST` | VPS IP or hostname |
| `VPS_USER` | SSH user (e.g. `ubuntu`) |
| `VPS_SSH_KEY` | Private SSH key (PEM format) |
| `VPS_PORT` | SSH port (usually `22`) |
| `DOCKER_USERNAME` | Docker Hub username |
| `DOCKER_PASSWORD` | Docker Hub access token |
| `SECRET_KEY` | Django secret key |
| `DB_PASSWORD` | PostgreSQL password |
| `EMAIL_HOST_USER` | SMTP email user |
| `EMAIL_HOST_PASSWORD` | SMTP email password |
| `STRIPE_SECRET_KEY` | Stripe secret key |
| `STRIPE_PUBLISHABLE_KEY` | Stripe publishable key |

---

## 🛠️ Local Development

### Prerequisites
- Python 3.10+
- pip

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/sequenceit-git/sequenceIT-learn.git
cd sequenceIT-learn

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
# .venv\Scripts\activate        # Windows

# 3. Install dependencies
pip install -r requirements/local.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and fill in your values

# 5. Run migrations
python manage.py migrate

# 6. Create a superuser
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

### Local Dev with Docker

```bash
# Run just the Django app (SQLite, hot-reload)
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

---

## 🐳 Production Deployment (VPS)

### One-time VPS setup

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Create app directory
mkdir -p /opt/sequenceit-learn && cd /opt/sequenceit-learn

# Create your .env file
cp .env.example .env && nano .env

# Start all services
docker compose up -d

# Create superuser
docker compose exec web python manage.py createsuperuser
```

### Useful commands

```bash
# View running containers
docker compose ps

# Follow logs
docker compose logs -f web

# Manual redeploy
docker compose pull web && docker compose up -d --no-deps --force-recreate web

# Database backup
docker compose exec db pg_dump -U sequenceit sequenceit > backup_$(date +%Y%m%d).sql

# Run any Django command
docker compose exec web python manage.py <command>
```

---

## 📁 Project Structure

```
sequenceIT-learn/
├── accounts/          # User management (Student, Lecturer, Admin)
├── config/            # Django settings, URLs, WSGI/ASGI
├── core/              # Dashboard, home, sessions, semesters
├── course/            # Programs, courses, allocation, registration
├── payments/          # Stripe & GoPay integration
├── quiz/              # Full quiz engine
├── result/            # Grade & assessment results
├── search/            # Global search
├── templates/         # All HTML templates
├── static/            # CSS, JS, vendor assets
├── media/             # User-uploaded files
├── nginx/             # Nginx config (for non-Traefik setups)
├── scripts/           # entrypoint.sh, data seeders
├── requirements/
│   ├── base.txt       # Shared dependencies
│   ├── local.txt      # Dev-only (black, django-extensions)
│   └── production.txt # Prod (gunicorn, psycopg2, etc.)
├── Dockerfile
├── docker-compose.yml
├── docker-compose.dev.yml
└── .github/
    └── workflows/
        └── django.yml # CI/CD pipeline
```

---

## 🤝 Contributing

Contributions are welcome! Check the [`TODO.md`](TODO.md) for open tasks.

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit your changes: `git commit -m 'feat: add your feature'`
4. Push to the branch: `git push origin feat/your-feature`
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🔗 References

- Quiz engine inspired by: [django_quiz](https://github.com/tomwalker/django_quiz)

---

<div align="center">
  <strong>Built with ❤️ by the SequenceIT team</strong><br/>
  <a href="https://sequenceit.com">sequenceit.com</a>
</div>
