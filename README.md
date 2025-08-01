# kudos
`A simple web application to send and receive kudos within an organization. This project includes both the backend (Django) and the frontend (Angular).`

## Backend - Django

# Setup
`cd kudos/`
`python -m venv venv`
`source venv/bin/activate`
`pip install -r files/setup/requirement.txt`

# Run Migrations
`python manage.py migrate`

# Load fixtures 
`python manage.py loaddata files/fixtures/organization.json`
`python manage.py loaddata files/fixtures/users.json`
`python manage.py loaddata files/fixtures/kudos.json`
`python manage.py loaddata files/fixtures/kudos_tracker.json`



## Frontend - Angular

# Setup
`cd kudos-frontend/`
`npm install`

# Run application
`ng serve`
`Navigate to http://localhost:4200/ in your browser`


## Login Credentials

# Regular User
`Email : luke@yopmail.com`
`password: Admin@123`

`All users have the same password: Admin@123`

# Django Admin (Superuser)
`Email : admin@gmail.com`
`password: Admin@123`
