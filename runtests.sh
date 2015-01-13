if [ -z "$VIRTUAL_ENV" ]; then
    echo "Make sure you run the tests in a virtualenv!!"
    exit 1
fi

TEST_PATH=rafee
export PYTHONPATH=$PYTHONPATH:./
export DJANGO_SETTINGS_MODULE=rafee.settings.test

if [ -n "$1" ]; then
    TEST_PATH=$1
fi

find . -name "*.pyc" -exec rm -rf {} \;
python manage.py makemigrations && python manage.py migrate
py.test -q --durations=3 --cov rafee --cov-report html $TEST_PATH
