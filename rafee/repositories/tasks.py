from os import path
from shutil import rmtree

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings

from rafee.repositories.models import Repository
from rafee.repositories.managers.git import GitManager


logger = get_task_logger(__name__)


def get_dst_path(url):
    return path.join(settings.RAFEE_REPO_DIR, path.basename(url))


@shared_task
def clone_and_create_repo(url):
    GitManager(url, get_dst_path(url))
    repo = Repository.objects.create(url=url)
    return repo.id


@shared_task
def remove_repo(pk):
    repo = Repository.objects.get(pk=pk)
    rmtree(get_dst_path(repo.url))
    repo.delete()


@shared_task
def pull_repo(url):
    dst_path = get_dst_path(url)
    git_manager = GitManager(url, dst_path)
    git_manager.pull()
