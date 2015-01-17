rafee
=====

## Setting development environment

You need to have the following installed in your system:

- python 2.7.x
- vagrant 1.6.x or later: http://www.vagrantup.com/downloads.html
- virtualbox 4.3.x or later: https://www.virtualbox.org/wiki/Downloads
- virtualenv 1.11.6 (optional but highly recommended): pip install virtualenv


### Backend

Run all the actions below in a virtual env:

    cd rafee
    pip install -r requirements-dev.txt
    vagrant up  # If something fails, just do vagrant reload --provision

    After vagrant finishes booting the VM. You can access the GUI via http://localhost:8888.

In order to run the unittests:

    ./runtests.sh  # Linux only, for windows you can check the script to know what to do

running tests with coverage:

    ./runtests --with-coverage  # Places html coverage report under htmlcov

When adding new celery tasks, you will need to reload the celery process from within the vm.
If the task belongs to a newly added django app, make sure is added to the INSTALLED_APPS (celery autodiscover tasks
from there) and restart uwsgi.


### Frontend

A superuser is created automatically when loading the dev vm. You can login using credentials::
    username: pp
    password: pp

Install the latest stable version of Node. To verify is properly installed, both commands below should return output:

    node --help
    npm --help

Install ember-cli (0.1.17 or later is required) and bower (you might need sudo for this):

    npm install -g ember-cli
    npm install -g bower

You need to have PhantomJS installed to be able to run the tests from the command line:

    npm install -g phantomjs

Open another window terminal and run:

    cd rafee/frontend && ember install
    ember server

navigate to http://localhost:4200 for the app.
navigate to http://localhost:4200/tests for the tests.

See more info on how to run tests at http://www.ember-cli.com/
