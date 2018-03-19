# Title

## Setup for development

### Create virtualenv

`source venv/bin/activate` should work and you should be able to skip the next step. 

### Install required packages

pip install requirements.txt

### Setup database

`python manage.py makemigrations`

`python manage.py migrate`

### Run server

`python manage.py runserver`
