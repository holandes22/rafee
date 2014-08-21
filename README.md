rafee
=====

## Setting development environment

git clone and init submodules.
You need to have the following installed in your system:

- python 2.7
- vagrant 1.6: http://www.vagrantup.com/downloads.html
- virtualbox: https://www.virtualbox.org/wiki/Downloads
- virtualenv (optional but highly recommended): pip install virtualenv

### Backend

Run all the actions below in a virtual env:

    cd rafee
    pip install -r requirements-dev.txt
    vagrant up

Choose default option for all steps below:

    fab vagrant migrate  # in order to apply token migration from DRF
    fab vagrant runserver  # choose the default dev option, runs at http://localhost:8888 (from VM)

In order to run the unittests:

    cd rafee/rafee
    python manage.py makemigrations --settings=rafee.settings.test && python manage.py test --settings=rafee.settings.test

or alternatively:

    export DJANGO_SETTINGS_MODULE=rafee.settings.test
    python manage.py makemigrations && python manage.py test

### Frontend

Install the latest stable version of Node. To verify is properly installed, both commands below should return output:

    node --help
    npm --help

Install ember-cli and bower (you might need sudo for this):

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

