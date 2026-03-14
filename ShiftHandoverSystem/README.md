# Shift Handover System

Shift Handover System is a Django web application developed for teams operating on a 24x7 schedule. It streamlines shift-to-shift communication by centralizing ticket handovers, providing visibility into important updates, and enabling feedback collection from shift members after major outages or other key events, ensuring that essential information is preserved across shifts.

## Overview

The project helps teams:

- hand over information about tickets that require further action or need to be monitored by other shifts
- share important updates with all team members, organized by category
- maintain a simple profile-based ownership system
- collect feedback from users that topic owners can use for future improvements
- view recent updates directly from the home page

- This makes shift transitions more structured, transparent, and easier to manage.

## Main Features

### Tickets Handover
- Create handover tickets
- Edit and delete tickets
- Track ticket status
- Store status history for each ticket
- Organize tickets by type such as Action, Discussion, Question, Review, Update, and Information

### Important Updates
- Add important updates for the team
- Categorize updates as Technical Update, Procedure Update, or Other
- Like/unlike updates
- View update details
- Show recent important updates on the home page

### Profiles
- Create a simple user profile
- View profile details
- Delete profile
- Track user-related activity such as count on created updates

### Feedback
- Submit feedback entries
- View all submitted feedback
- Associate feedback with a profile owner

## Project Structure

- `profiles/` - profile creation, details, and deletion
- `tickets_handover/` - handover ticket management and status tracking
- `important_updates/` - update creation, listing, details, editing, deleting, and likes
- `feedback/` - feedback creation and listing
- `common/` - shared app components
- `templates/` - HTML templates
- `static/` - CSS and image assets

## Technologies Used

- Python
- Django
- PostgreSQL
- HTML
- CSS

## Database Configuration

The project is configured to use PostgreSQL.

Default database settings in the project:
- Database name: `shift_handover_system`
- User: `postgres`
- Host: `127.0.0.1`
- Port: `5432`

Update the database credentials in `ShiftHandoverSystem/settings.py` before running the project if needed.

## Installation

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies
4. Configure PostgreSQL
5. Apply migrations
6. Run the development server

Example:

```bash
python -m venv .venv
source .venv/bin/activate
pip install django psycopg2
python manage.py migrate
python manage.py runserver