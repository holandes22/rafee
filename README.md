rafee
=====

## Setting development environment

You need to have the following installed in your system:

- python 2.7.x
- vagrant 1.6.x or later: http://www.vagrantup.com/downloads.html
- virtualbox 4.3.x or later: https://www.virtualbox.org/wiki/Downloads
- virtualenv 1.11.6 (optional but highly recommended): pip install virtualenv


## Backend

Run all the actions below in a virtual env:

    cd rafee
    pip install -r requirements-dev.txt
    vagrant up  # If something fails, just do vagrant reload --provision

After vagrant finishes booting the VM, you can access the GUI via http://localhost:8888.
A superuser is created automatically when loading the dev vm. You can login using the credentials:

    username: pp
    password: pp

#### API

The REST API is accessed via http://localhost:8888/api/v1

You can checkout the API docs at http://localhost:8888/api/v1/docs

#### Running Tests

In order to run the unittests:

    ./runtests.sh  # Linux only, for windows you can check the script to know what to do

running tests with coverage:

    ./runtests.sh -c  # Places html coverage report under htmlcov

Run `runtests.sh -h` to see other options.

#### Adding celery tasks

When adding new celery tasks, you will need to reload django (uwsgi) and celery.

    ansible-playbook -i provisioning/inventory/ --tags=uwsgi,celery provisioning/site.yml --limit=vagrant

If the task belongs to a newly added django app, before reloading make sure is added to the INSTALLED_APPS (celery autodiscover tasks
from there).


## Frontend

Install the latest stable version of Node. To verify is properly installed, both commands below should return output:

    node --help
    npm --help

Install ember-cli (0.1.17 or later is required) and bower (you might need sudo for this):

    npm install -g ember-cli
    npm install -g bower

In order to install the frontend dependencies, run

    cd rafee/frontend && ember install

#### Dev server

In order to run the ember dev server (which provides automatic rebuild and browser reload), run:

    cd rafee/frontend
    ember server

You can then either navigate to http://localhost:4200 for the app (served by ember server) or go to http://localost:888 to get the app
served by nginx on the dev vm. The advantage of using ember server is automatic browser reload (which is very nice while
developing)

#### Running tests

You need to have PhantomJS installed to be able to run the tests from the command line:

    npm install -g phantomjs

The run

    ember server

and navigate to http://localhost:4200/tests to see the frontend tests report.
