import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rafee.settings.dev')
django.setup()

from rafee.users.factories import UserFactory
from rafee.teams.factories import TeamFactory
from rafee.slideshows.factories import SlideshowFactory
from rafee.repositories.tasks import clone_and_create_repo


team1 = TeamFactory(name='Team Fortress 2')
team2 = TeamFactory(name='The A team')

admin = UserFactory(is_staff=True)
user1 = UserFactory(teams=[team1])
user2 = UserFactory(teams=[team1, team2])

repo_urls = [
    'https://github.com/holandes22/hsg-templates.git',
    'https://github.com/holandes22/css-templates.git',
]

for repo_url in repo_urls:
    task = clone_and_create_repo.delay(repo_url)
    result = task.get()

templates1 = 'hsg-templates/commits,css-templates/users'
slideshow1 = SlideshowFactory(templates=templates1, team=team1)

templates2 = 'css-templates/user_repos,css-templates/users,css-templates/no_data'
slideshow1 = SlideshowFactory(templates=templates2, team=team2)
