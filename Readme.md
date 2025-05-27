# Library Management System

This project is a simple REST API built with Django and DRF. Allows users to register, log in, search for books, borrow and return them. Admins can manage users and books through the admin panel.

## Features

- Registration and login with JWT authentication
- Role based Permissions: Anonymous users can browse, authenticated users can borrow/return books, only admin users can manage all data
- Filter books by title, author, and availability
- Admin panel for managing books, users, and loans
- Swagger documentation for all endpoints
- Unit tests and integration tests with coverage
- Dockerfile for deployment
- Ready for deployment on Heroku

## Tech Stack Used
- Ubuntu
- Python 3.11
- Django 5.2.1
- Django REST Framework
- PostgreSQL
- SimpleJWT (for authentication)
- Docker
- Gunicorn (Not Confirgured)
- Heroku (didnt deploy, but set it ready to deploy)

## Setup Instructions (Local)

1. Clone the repository
    git clone <your-repo-url>
    cd library_system

2. Create and activate a virtual environment
    python -m venv venv
    source venv/bin/activate

3. Install dependencies
    pip install -r requirements.txt

4. Set up the database
    Make sure PostgreSQL is installed and running. Create a database called `library_db` and update the database settings in `config/settings.py` to match the db user and password.

5. Run migrations
    python manage.py migrate

6. Create a superuser
    python manage.py createsuperuser

7. Run the development server
    python manage.py runserver

8. For API Endpoints, Use swagger url localhost:8000/swagger/, also have created a Postman collection with sample data, import the collection file provided or, use the following link to import https://martian-resonance-855726.postman.co/workspace/Team-Workspace~f4c1bfd2-25fe-4d2a-8825-ac7189fe3cdc/collection/29980308-94830ce0-5a64-4af8-92cf-aeb6256e4955?action=share&creator=29980308.

9. Running Tests

    To run unit and integration tests:
    python manage.py test

    To check test coverage:
    coverage run manage.py test
    coverage report (Text based report) (Have included the .coverage file for ease of reading, not the best practice to do so in production deployments though)
    coverage html (Html report) (Have also added the html coverage, open index.html from htmlcov folder)

10. Docker (Optional)

    To build and run the app in a Docker container:
        docker build -t library-system .
        docker run -p 8000:8000 library-system

    If you're using `docker-compose.yml` for local PostgreSQL:
        docker-compose up --build

11. Heroku Deployment (Optional)
    My expertise is mostly on deploying to Azure/AWS, havent worked with Heroku, but I have setup the basic files by refering to various arctivles on the web on how to deploy to Heroku.
