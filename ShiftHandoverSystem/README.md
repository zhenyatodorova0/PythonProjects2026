# Shift Handover System

Shift Handover System is a Django web application for teams working in rotating or 24x7 shifts. It centralizes handover notes, important updates, and follow-up feedback so critical information is not lost between shifts.

## Overview

The system helps teams:

- hand over tickets that need monitoring or further action
- share important operational updates
- organize updates by category
- keep simple profile-based ownership of content
- collect feedback after incidents or major events

## Main Features

### Tickets Handover

- create handover tickets
- edit and delete tickets
- track ticket status
- keep status history
- organize tickets by type such as Action, Discussion, Question, Review, Update, and Information

### Important Updates

- create important updates for the team
- group updates by category
- like and unlike updates
- review update details
- show recent updates on the home page

### Profiles

- create and manage user profiles
- view profile details
- track user-related activity

### Feedback

- submit feedback entries
- review submitted feedback
- connect feedback to a profile owner

## Project Structure

- `ShiftHandoverSystem/` - project configuration and settings
- `tickets_handover/` - handover ticket management
- `important_updates/` - important updates module
- `profiles/` - profile management
- `feedback/` - feedback module
- `accounts/` - account-related functionality
- `templates/` - HTML templates
- `static/` - static assets

## Technologies Used

- Python
- Django
- PostgreSQL
- HTML
- CSS

## Project Setup Guide

### Prerequisites

Before starting, make sure you have the following installed:

- Python 3
- PostgreSQL
- `pip`
- Git

### Setup Guide

#### Step 1: Clone the repository

```bash
git clone https://github.com/zhenyatodorova0/PythonProjects2026
cd ShiftHandoverSystem
```

#### Step 2: Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Step 3: Install the project requirements

```bash
pip install -r requirements.txt
```

#### Step 4: Configure the environment and run migrations

Create a `.env` file in the project root with the required settings:

```env
SECRET_KEY=your-secret-key
DB_NAME=shift_handover_system
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=127.0.0.1
DB_PORT=5432
```

Then apply the database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

#### Step 5: Run the server

```bash
python manage.py runserver
```

Open the application in your browser at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Notes

- The project uses PostgreSQL as its database backend.
- Environment variables are loaded from `.env`.
- If PostgreSQL is running with different credentials, update the `.env` values before starting the application.
