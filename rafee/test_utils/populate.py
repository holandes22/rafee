import os
import sys

sys.path.append('/vagrant')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rafee.settings.dev')

import django

django.setup()  # Call this before importing the models

from rafee.teams.models import Team
from rafee.users.factories import UserFactory
from rafee.teams.factories import TeamFactory
from rafee.slideshows.factories import SlideshowFactory
from rafee.repositories.tasks import clone_and_create_repo


teams = []


print 'Creating teams'
for name in ['Team Fortress 2', 'The A team']:
    try:
        team = Team.objects.get(name=name)
        teams.append(team)
    except Team.DoesNotExist:
        teams.append(TeamFactory(name=name))

print 'Teams: ', teams

admin = UserFactory(is_staff=True)
user1 = UserFactory(teams=(teams[0],))
user2 = UserFactory(teams=teams)
UserFactory(teams=teams)
UserFactory(teams=teams)

repo_urls = [
    'https://github.com/holandes22/hsg-templates.git',
    'https://github.com/holandes22/css-templates.git',
]

for repo_url in repo_urls:
    print 'Cloning {}'.format(repo_url)
    task = clone_and_create_repo.delay(repo_url)
    result = task.get()

templates1 = 'hsg-templates/commits,css-templates/users'
slideshow1 = SlideshowFactory(templates=templates1, team=teams[0])

templates2 = 'css-templates/user_repos,css-templates/users,css-templates/no_data'
slideshow1 = SlideshowFactory(templates=templates2, team=teams[1])
print 'Done'
