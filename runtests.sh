#!/bin/bash

set -e  # Abort on first error

function usage()
{
cat <<-ENDOFMESSAGE

$0 [OPTIONS]

options:

    -c With coverage.
    -p Path to tests. Accepts specific test/test suite.
    -h Display this message.
    -m Run migrations before pytest. Needed for first time
       after cloning or after modifying the DB schema.

ENDOFMESSAGE
exit 1
}


if [ -z "$VIRTUAL_ENV" ]; then
    echo "Make sure you run the tests in a virtualenv!!"
    exit 1
fi

COVERAGE=""
TEST_PATH=rafee
export DJANGO_SETTINGS_MODULE=rafee.settings.test


while getopts "hp:cm" opt; do
  case $opt in
    c)
      echo "Running tests with coverage!" >&2
      COVERAGE="--cov rafee --cov-report html --cov-report xml"
      ;;
    m)
      echo "Running migrations!" >&2
      find . -name "*.pyc" -exec rm -rf {} \;
      python manage.py makemigrations && python manage.py migrate
      ;;
    p)
      TEST_PATH=$OPTARG
      ;;
    h)
      usage
      ;;
    \?)
      usage
      ;;
  esac
done

py.test -q --durations=3 $COVERAGE $TEST_PATH
