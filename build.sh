#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Create any missing migrations
python manage.py makemigrations

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate
