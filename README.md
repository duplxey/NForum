# NForum
Simple forum written in Python using Django.

## Preparing the development environment
1. Install Python.
1. Create a virtual environment (https://docs.python.org/3/tutorial/venv.html).
1. Install the packages in requirements.txt.
1. Run the server! :)

## Getting MySQL to work with Django
You may stumble upon problems (again) when trying to hook MySQL with Django. Most of the solutions you'll find won't work like:
- Installing mysqlclient
- Installing Visual Studio with BuildTools
- Trying to compile the module yourself...

The only solution that actually works is the following one: https://stackoverflow.com/questions/15312732/django-core-exceptions-improperlyconfigured-error-loading-mysqldb-module-no-mo#answer-55086635 / https://i.imgur.com/kI897OO.png.
