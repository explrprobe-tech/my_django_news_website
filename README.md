# My Django News Website

A modern news website built with Django, featuring real-time solar data from NOAA APIs, user authentication, and a beautiful glass-morphism UI.

## ✨ Features

- 📰 **News Management** - Create, edit, and publish news articles
- 🔐 **User Authentication** - Login/register with role-based permissions (Admins, Editors, Regular Users)
- 🚀 **Secret Space Page** - Real-time solar radio flux data from NOAA APIs
- 🎨 **Beautiful UI** - Glass-morphism design with smooth animations
- 📱 **Responsive** - Works perfectly on all devices
- 🐳 **Docker Support** - Containerized for easy deployment
- ✅ **Automated Tests** - Comprehensive test suite

## 🛠️ Tech Stack

- **Backend**: Django 5.0, Python 3.12
- **Database**: SQLite3 (development), PostgreSQL (production-ready)
- **Frontend**: HTML5, CSS3, JavaScript
- **APIs**: NOAA Space Weather Prediction Center
- **Container**: Docker, Docker Compose
- **Testing**: Django TestCase, Pytest
- **CI/CD**: GitHub Actions

## 📋 Prerequisites

- Python 3.12+
- Docker and Docker Compose (optional)
- Git

## Project Structure

my_django_news_website/
├── mysite/                 # Main Django project
│   ├── settings.py        # Project settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI entry point
├── news/                   # News application
│   ├── models.py          # Database models
│   ├── views.py           # View functions/classes
│   ├── forms.py           # Form definitions
│   ├── admin.py           # Admin panel configuration
│   ├── urls.py            # App URL configuration
│   └── templates/         # HTML templates
│       └── news/          # App templates
├── tests/                  # Test files
│   ├── test_models.py
│   ├── test_views.py
│   ├── test_forms.py
│   └── test_auth.py
├── manage.py
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── .dockerignore          # Files to ignore in Docker
└── README.md              # This file

## 🚀 Quick Start

### Option 1: Local Development

# 1. Clone the repository
git clone https://github.com/explrprobe-tech/my_django_news_website.git
cd my_django_news_website

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Run development server
python manage.py runserver

Visit http://localhost:8000 🎉


#Option 2: Using Docker

# 1. Build the Docker image
docker build -t my-django-news-website .

# 2. Run the container
docker run -p 8000:8000 -v $(pwd)/db.sqlite3:/app/db.sqlite3 my-django-news-website

# Or using Docker Compose:
docker-compose up --build

#Docker Commands

# Build image
docker build -t my-django-news-website .

# Run container (database inside mysite\db.sqlite3)
docker run -p 8000:8000 my-django-news-website

# Using docker-compose
docker-compose up
docker-compose down
docker-compose up --build  # Rebuild and start


### Testing

# Run all tests
python manage.py test

# Run specific test file
python manage.py test news.tests.test_models

# Run with coverage
coverage run manage.py test
coverage report
coverage html  # Generate HTML report