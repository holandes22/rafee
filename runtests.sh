if [ -z "$VIRTUAL_ENV" ]; then
    echo "Make sure you run the tests in a virtualenv"
    exit 1
fi

export PYTHONPATH=$PYTHONPATH:./rafee
find . -name "*.pyc" -exec rm -rf {} \;
export DJANGO_SETTINGS_MODULE=rafee.settings.test
python manage.py makemigrations && python manage.py migrate && coverage run --source='.' manage.py test
