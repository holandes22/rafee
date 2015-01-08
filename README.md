rafee
=====

## Setting development environment

git clone and init submodules.
You need to have the following installed in your system:

- python 2.7.x
- vagrant 1.6.x or later: http://www.vagrantup.com/downloads.html
- virtualbox 4.3.x or later: https://www.virtualbox.org/wiki/Downloads
- virtualenv 1.11.6 (optional but highly recommended): pip install virtualenv

### Backend

Run all the actions below in a virtual env:

    cd rafee
    pip install -r requirements-dev.txt
    vagrant up

Choose default option for all steps below:

    fab vagrant runserver  # Runs at http://localhost:8888 (from VM). Choose default values when prompted.

In order to run the unittests:

    cd rafee/rafee
    python manage.py makemigrations --settings=rafee.settings.test && python manage.py migrate && python manage.py test --settings=rafee.settings.test

or alternatively:

    export DJANGO_SETTINGS_MODULE=rafee.settings.test
    python manage.py makemigrations && python manage.py migrate && python manage.py test

running tests with coverage:

    python manage.py makemigrations && python manage.py migrate && coverage run --source='.' manage.py test
    coverage report


When adding new celery tasks, you will need to reload the celery process.

    fab vagrant supervisor.celery_restart

If the task belongs to a newly added django app, make sure is added to the INSTALLED_APPS (celery autodiscover tasks
from there). and restart of the web server.


### Frontend

A superuser is created automatically when loading the dev vm. You can login using credentials::
    username: pp
    password: pp

Install the latest stable version of Node. To verify is properly installed, both commands below should return output:

    node --help
    npm --help

Install ember-cli (0.4.6 or later is required) and bower (you might need sudo for this):

    npm install -g ember-cli
    npm install -g bower

You need to have PhantomJS installed to be able to run the tests from the command line:

    npm install -g phantomjs

Open another window terminal and run:

    cd rafee/frontend && npm install && bower install
    ember server

navigate to http://localhost:4200 for the app.
navigate to http://localhost:4200/tests for the tests.

See more info on how to run tests at http://www.ember-cli.com/

