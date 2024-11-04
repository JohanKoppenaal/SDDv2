#!/bin/bash

# Kleuren voor output
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Creating project structure in SDDv2...${NC}"

# Backend structure
mkdir -p backend/core/settings
mkdir -p backend/apps/{discounts,shopware,users}
mkdir -p backend/utils
touch backend/Dockerfile
touch backend/pyproject.toml
touch backend/manage.py
touch backend/core/__init__.py
touch backend/core/settings/{__init__.py,base.py,development.py,production.py}
touch backend/core/{urls.py,wsgi.py}

# Frontend structure
mkdir -p frontend/src/{assets,components,views,store,router}
mkdir -p frontend/public
touch frontend/Dockerfile
touch frontend/package.json
touch frontend/vite.config.js
touch frontend/src/App.vue

# Docker configuration
mkdir -p docker/nginx
mkdir -p docker/postgres
touch docker/nginx/nginx.conf
touch docker/postgres/init.sql

# Root level files
touch docker-compose.yml
touch .env.example
touch README.md

# Set correct permissions
chmod 755 $(find . -type d)
chmod 644 $(find . -type f)

echo -e "${GREEN}Project structure created successfully!${NC}"
echo -e "${GREEN}Directory structure:${NC}"
tree

# Creëer .env bestand met basis configuratie
cat > .env.example << EOL
# Django settings
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=shopware_discount
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=postgres
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Shopware API
SHOPWARE_API_URL=
SHOPWARE_CLIENT_ID=
SHOPWARE_CLIENT_SECRET=
EOL

# Kopieer .env.example naar .env
cp .env.example .env

echo -e "${GREEN}Setup complete!${NC}"
