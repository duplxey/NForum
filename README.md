# NForum
NForum is a simple light-weight forum written in Python using Django. It allows users to create their own threads
or talk in already existing ones. It has a built-in upvote/downvote (reputation) system, achievements, alerts & more!

> :warning: The project is still under heavy development and should not be used in production in it's current state.

## Features
- Extremely easy to use UI.
- Admin is able to create different thread subcategories that are grouped in thread categories.
- Users are able to create their own threads (topics) or talk in already existing ones.
- Each user gets his own profile (with changeable description + avatar)
- Reputation system (users can upvote or downvote each others' messages).
- Achievement system (based on thread count, post count, upvotes, downvotes)
- Alerts (users get a notification when someone responds to their thread, are mentioned or their post is rated)
- Wiki pages (community can create wiki pages)

## Preparing the development environment
1. Install Python and pip (https://www.python.org/downloads/).
1. Create a new virtual environment (https://docs.python.org/3/tutorial/venv.html).
1. Create a new `.env` file (in this directory) containing the following:
    ```
    SECRET_KEY = <django-secret-key>
    DATABASE_NAME = <name>
    DATABASE_USER = <user>
    DATABASE_PASSWORD = <password>
    DATABASE_PORT = <port>
    DATABASE_HOST = <host>
    ```
1. Install the packages in requirements.txt (`pip install -r requirements.txt`).
1. Run the server! (`python manage.py runserver`)

NOTE: You also need a database (preferably MySQL) running in the background. Provide your database credentials in `.env`.

## Admin panel
You'll first need to create a super user using the following command:  
`python manage.py createsuperuser`