
```markdown
# SDDv2 Installation Guide

## Voorvereisten
- Python 3.9+
- Git
- Docker & Docker Compose (voor later gebruik)

## Basis Setup

### 1. Poetry Installatie
```bash
# Voor macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -

# Voor Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# Voeg Poetry toe aan PATH (voor macOS/Linux)
export PATH="$HOME/.local/bin:$PATH"

# Verifieer installatie
poetry --version
```

### 2. Project Setup
```bash
# Clone het project (indien nog niet gedaan)
git clone [repository-url]
cd SDDv2

# Ga naar de backend directory
cd backend

# Activeer Poetry environment
poetry shell

# Installeer dependencies
poetry install
```

### 3. Django Project Structuur
```bash
# Maak basis directory structuur
mkdir -p core/settings
touch core/settings/__init__.py
touch core/settings/base.py
touch core/settings/development.py
touch core/settings/production.py

# Maak apps
python manage.py startapp discounts
python manage.py startapp shopware
python manage.py startapp users

# Maak apps directory en verplaats apps
mkdir apps
mv discounts shopware users apps/
touch apps/__init__.py
```

### 4. Settings Configuratie

#### core/settings/base.py aanpassen:
```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-development-key')

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # Third party apps
    'rest_framework',
    
    # Local apps
    'apps.discounts.apps.DiscountsConfig',
    'apps.shopware.apps.ShopwareConfig',
    'apps.users.apps.UsersConfig',
]

# [Rest van de standaard Django settings...]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}
```

### 5. Apps Configuratie
Voor elke app (discounts, shopware, users), update apps.py:

```python
# apps/[app_name]/apps.py
from django.apps import AppConfig

class [AppName]Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.[app_name]'
```

### 6. Database Setup
```bash
# Voer database migraties uit
python manage.py migrate

# Maak superuser aan
python manage.py createsuperuser
```

### 7. Development Server Starten
```bash
# Check eerst of poort 8000 vrij is
lsof -i :8000  # Voor macOS/Linux
# Als bezet, stop het proces:
kill $(lsof -ti:8000)

# Start de server
python manage.py runserver
```

## Verificatie
1. Open browser en ga naar http://127.0.0.1:8000/admin
2. Log in met superuser credentials
3. Controleer of je de admin interface kunt zien

## Troubleshooting

### Veel voorkomende problemen

1. **Poetry niet gevonden**
```bash
export PATH="$HOME/.local/bin:$PATH"
source ~/.zshrc  # of ~/.bashrc
```

2. **Poort 8000 in gebruik**
```bash
# Optie 1: Stop het proces
kill $(lsof -ti:8000)

# Optie 2: Gebruik andere poort
python manage.py runserver 8001
```

3. **Import errors voor apps**
- Controleer of `apps/__init__.py` bestaat
- Controleer of de app paths correct zijn in INSTALLED_APPS
- Controleer of de `name` in elke `apps.py` correct is

## Development Workflow
1. Activeer altijd eerst de Poetry environment:
```bash
cd backend
poetry shell
```

2. Start de development server:
```bash
python manage.py runserver
```

3. Voor nieuwe dependencies:
```bash
poetry add [package-name]
```

## Volgende Stappen
- Models definiëren voor elke app
- API endpoints configureren
- Frontend setup
- Docker configuratie