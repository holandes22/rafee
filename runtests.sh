#!/bin/bash
function usage()
{
cat <<-ENDOFMESSAGE

$0 [OPTIONS]

options:

    -c With coverage.
    -p Path to tests. Accepts specific test/test suite.
    -h Display this message.

ENDOFMESSAGE
    exit 1
}


if [ -z "$VIRTUAL_ENV" ]; then
    echo "Make sure you run the tests in a virtualenv!!"
    exit 1
fi

COVERAGE=""
TEST_PATH=rafee
export PYTHONPATH=$PYTHONPATH:./
export DJANGO_SETTINGS_MODULE=rafee.settings.test


while getopts "hp:c" opt; do
  case $opt in
    c)
      echo "Running tests with coverage!" >&2
      COVERAGE="--cov rafee --cov-report html"
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


find . -name "*.pyc" -exec rm -rf {} \;
python manage.py makemigrations && python manage.py migrate
py.test -q --durations=3 $COVERAGE $TEST_PATH
