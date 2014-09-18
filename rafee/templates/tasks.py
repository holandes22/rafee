import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings

from rafee.templates.manager import TemplateManager


logger = get_task_logger(__name__)

# TODO: Add tests
@shared_task
def render(template_name):
    data_source = {}
    manager = TemplateManager(settings.RAFEE_REPO_DIR)
    info = manager.get_template_info(template_name)
    data_source_url = info.get('data_source_url', None)
    if data_source_url is not None:
        r = requests.get(data_source_url)
        data_source = r.json()
    return manager.render(template_name, data_source=data_source)
