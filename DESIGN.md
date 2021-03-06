Backend
=======


Repositories
------------

- A repository represents a folder where templates are stored.
- This should be a git repo.
- No automatic switch of branches.
- The user can add several repositories.
- Django should be able to clone this repository (read access to the repo and write permissions to the specified path).


File system hierarchy is as follows:

`some_folder/<template_name>/`

- template.j2 (mandatory): The template to render . Render engine jinja2
- data.source (optional): A text file containing a URL (only the first line will be considered) from where data will be retrieved and passed to the template. Expected a JSON response.


Every folder including a template.j2 file will be used.

Includes (insert other templates) should be possible, if django can access that file.

Given this is to mainly show static pages, we have some constrains to simplify things:

- Templates will have access to bootstrap styling.
- Templates cannot add link, script nor style tags (they will be removed prior to rendering). Checkout: http://lxml.de/api/lxml.html.clean.Cleaner-class.html


Repository Model:

- url: URL from where to clone the repo (local path is not supported).

The repository will be cloned to a pre-defined reserved folder for rafee with write permissions to it.
If the filepath already exists, adding the repo will fail. The repo will then be polled periodically and bring changes if necessary


Slideshow
---------

A slideshow allows a Team to configure which templates to show and in which order.

Slideshow Model:

    - name
    - team: FK to the Team model
    - templates: CSV of template identifiers to show. The order of appearance is considered. The names are relative to the team repos. Identifier is formed as shuch: <repo_id>-<template_folder_name>
    - transition_interval: Seconds between template transition
    - caching_interval: Seconds to keep a cache copy (maybe move this as query param in the /slides endpoint)

Team
----

Team Model:

    - name
    - users: FK to a user model

User
----

User Model:

    - full_name
    - email:  (used as username as well)


Template rendering
------------------

When a request comes to render a template, a task is fired to do the following:

1. the template is read from the fs along with data source details.
2. Read data source from URLs if required. If there are several URLs, the read should be done with coroutines to speed up process
3. Cache the result for the specified time in the slideshow

Template preview
----------------

The frontend should provide some way to preview a template. This is to facilitate adding new templates (you don't want to push to repo, wait for pull and only then find out you missed something)

API
---

Prefix: `api.<hostname>/v1`

note:: WRITE superseeds READ

    /users WRITE [admin]
    /users/:id READ [user] WRITE [admin]
    /teams CRUD [admin]
    /repositories CRUD [admin] -> Returns a task (Since cloning can be a long running task)
    /slideshows READ [user] WRITE [admin] -> Users can only see slideshows from their teams. When specifying the
    template names. Missing template files are ignored (this omission should be logged).
    /templates READ [admin]--> A list of currently available template in the file system (name, data_src)
    /templates/preview [admin] --> A POST request containing a Jinja 2 template string (mandatory) and a URL to retrieve data (optional). Returns a rendered page
    /slides READ [user,admin] --> :id is formed by the repo id, a dash and the name of the folder that contains the
    template (e.g. 1-commits). The response is a task_id. Returning a task allows the frontend to ask to render all the templates in a slideshow at once, and start showing them only when ready, giving a better user xp.
    /tasks READ [user,admin]

The API needs to support query params to allow filtering (for example /slideshows?team=team_id)

Authentication
--------------

By default there is no security (no TLS, no credentials verification) as this is an internal project to use in the team, so it is trust based.
User is identified by token to allow plugin auth backends if needed (oauth for example).

Admin login will require a password.


Frontend
========

Simple Ember web app.

At the admin page it allows to manage repos, slideshows and users.


    / --> select slideshow (if logged in) from all the available ones to the user
    /login
    /slideshow: Shows stop,play,next,prev buttons. Next, prev show names.
    /admin --> Login page for admin
    /admin/users
    /admin/users/:id
    /admin/teams
    /admin/teams/:id
    /admin/repositories
    /admin/repositories/:id
    /admin/slideshows
    /admin/slideshows/:id
    /admin/templates
    /admin/templates/preview
