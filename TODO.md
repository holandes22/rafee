TODO: open tickets for each item

Backend
-------

- Add debug tools
    - Werkzeug
    - Sentry?
    - Django debug tool bar
    - Set django logs properly. Maybe use email notification too.
    - Set uwsgi and nginx logs properly
- Ansible:
    - check best practices
        - http://goodcode.io/blog/ansible-tips/
        - https://gist.github.com/marktheunissen/2979474
        - http://docs.ansible.com/playbooks_best_practices.html#best-practices
    - Supervisor
        - security: since we run supervisor as root, is recommended to explicitely indicate the config file, instead of
          it searching automatically in some places.
    - ssh to vm
        - for vagrant, path to ssh key is relative, causing problems to run provision when running vagrant cmd elsewhere
          than root
        - known_hosts key checking fails if vm was added to known hosts and then recreated
    - For prod password and secret key, use var_promt_
    - Separate dev and prod variables
    - Add meta info to roles
    - remove sudo: yes?
    - create project user if needed
    - uwsgi params move to files instead of templates
    - create django superuser only in dev
    - Update vars for dev and prod
    - Re-arrange ansible folder (in preparation to use it for production)
    - Create deployment, upgrade and reload playbooks
    - Separate playbook into roles. This will allow to run certain parts after changes are introduced
      during dev (added task, changed a model, etc)
        - common
        - packages
        - create folders
        - db
        - django (migration, collectstatic)
        - celery
        - uwsgi
        - nginx
- switch to python3
    - Need to remove fabric usage (no much needed anyway, can just use ansible ad-hoc commands)
    - Use supervisor from master  branch (Py3 support will come with release 4.0, currently dev branch)
- Switch ssl on in dev env
- nginx
    - fix errors [emerg] bind() to 0.0.0.0:8000 failed (98: Address already in use)
- Set up redis for template render caching
- Test how would work to add new task (which services need restart and document how to do so)
- Test how would work to do a change to a model (document how to run the migration)

General
-------
- Add authenticated mixin to all routes (except login, about). Check if it can cascade down application maybe.
- Slideshow main screen should not show dropdown if no slideshows
- Add mixin that redirects to error page if user is not staff when browsing /admin
- Fix confirm delete component redirect to resource list
- Refactor confirm delete component to bubble up delete action to router
- Refactor code to pave the upgrade for ember 2.0 https://gist.github.com/samselikoff/1d7300ce59d216fdaf97
- try json api
- fix text overflow when name on list is long (overflows to edit form)
- Add bulk selection of list items (for delete for example)
- Search bars and filters in sections
- Redirect to error page if server is down (now it just shows the loading icon)
- Maybe move loading icon to topbar
- active classes on sections
- Lists of resources should be ordered
- Generic error handler mixin
- try to move stuff in application template to somewhere else (should just contain the outlet, annoying each update of ember)
- Mostrar 404 y 500 error (specially after delete if user presses back button)
- slideshow dropdown should not appear at main page if slideshow list is empty
- Admin dashboard index add cards counting objects in each class or something similar
- Unify colors in less: For example use a details-color class (which points to success in bootstrap) to have it one place
- Add error handlers for promises
- Add/Edit forms (check ember forms)
- Add delete view
- Add slideshows screen and flow logic
- Add error and loading states templates
- Templates rendered should appear as html
- Use jquery knob to indicate polling intervals
- Fix nav bar not staying on top when scrolling right pane content
- Details box of resources should always stay on top (when we have a long list of users for example and need to scroll down) --> position: fixed
- Add active classes when navigating (to everythin!)
- Fix CSS in login screen (use less secific stuff)
- Adding repo
- fix  http://0.0.0.0:4200/assets/bootstrap-theme.css.map 404 (Not Found)
- Template screen
    - Add details section
    - Add template string to details
    - Render should be shown full page

Tests
-----
- Start covering with unit and integration tests

Tasks
-----
- Make pollster generic
- Find a solution for clearing finished tasks
