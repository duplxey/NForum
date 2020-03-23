# NForum
NForum is a simple light-weight forum written in Python using Django. It allows users to create their own threads
or talk in already existing ones. It has a built-in upvote/downvote (reputation) system, achievements, alerts & more!

> :warning: The project is still under heavy development and should not be used in production in it's current state.

## Features
- Extremely easy to use UI.
- Admin is able to create different thread subcategories that are grouped in thread categories.
- Users are able to create their own threads (topics).
- Reputation system (users can upvote or downvote each others' messages).
- Achievement system (based on thread count, post count, upvotes, downvotes)
- Alerts (users get a notification when someone responds to their thread or are mentioned)

## Preparing the development environment
1. Install Python.
1. Create a virtual environment (https://docs.python.org/3/tutorial/venv.html).
1. Install the packages in requirements.txt.
1. Run the server! :)

NOTE: You'll also need a MySQL database running in the background. You can configure the DB access in nforum/settings.py.

## Admin panel
You'll first need to create a super user using the following command:  
`python manage.py createsuperuser`