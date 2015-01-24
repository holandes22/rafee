### TODO: open tickets for each item

General
-------

- try json api

Backend
-------

- nginx
    - if uwsgi is down, nginx should time out inmediately (it keeps waiting from django,
      delaying the response)

- Add debug tools
    - Sentry? (or other monitoring tool)
    - Profiling (perf)
    - Django debug tool bar or django-queryinspect (might work better than dt for API)
    - Set django logs properly. Maybe use email notification too.
    - Set uwsgi and nginx logs properly
- Ansible:
    - check we comply with best practices
        - http://goodcode.io/blog/ansible-tips/
        - https://gist.github.com/marktheunissen/2979474
        - http://docs.ansible.com/playbooks_best_practices.html#best-practices
    - Create a deployment playbook for staging/prod that pulls code from git
        - For prod passwords and secret key, use var_prompt
    - remove sudo: yes?
- switch to python3
    - Need to use supervisor from dev branch (Py3 support will come with release 4.0, currently dev branch)
- Security
    - Run with django-secure
    - Switch ssl on (should be easy to switch off during dev)
    - use same security django settings for dev and prod
- nginx
    - fix errors [emerg] bind() to 0.0.0.0:8000 failed (98: Address already in use) (apparently the workers
      raise this error after the main process was started)
- Set up redis for template render caching
- Test how would work to add new task (which services need restart and document how to do so)
- Test how would work to do a change to a model (document how to run the migration)


Frontend
--------
- General
    - Add slideshows flow logic diagram to DESIGN.md
    - Add error and loading states templates
    - Refactor code to pave the upgrade for ember 2.0 https://gist.github.com/samselikoff/1d7300ce59d216fdaf97
    - Redirect to error page if server is down (now it just shows the loading icon)
    - Search bars and filters in sections
    - Generic error handler mixin
    - Show 404 and 500 error (specially after delete if user presses back button)
    - Admin dashboard index add cards counting objects in each class or something similar
    - Unify colors in less: For example use a details-color class (which points to success in bootstrap) to have it one place
    - Add error handlers for promises
    - Add/Edit forms where missing (check ember forms)
    - Use jquery knob to indicate polling intervals
    - Fix nav bar not staying on top when scrolling right pane content
    - Details box of resources should always stay on top (when we have a long list of users for example and need to scroll down) --> position: fixed
- Maybe move loading icon to topbar
- User
    - Changing user in edit form is not bound to user detail list (should be changed live)
- Login / Auth
    - Fix CSS in login screen (use less secific stuff)
    - Add authenticated mixin to all routes (except login, about). Check if it can cascade down application maybe.
    - Add mixin that redirects to error page if user is not staff when browsing /admin
- Slideshows
    - slideshow dropdown should not appear at main page if slideshow list is empty
- Components
    - fix text overflow when name on list is long (overflows to edit form)
    - Fix confirm delete component redirect to resource list
    - Refactor confirm delete component to bubble up delete action to router
    - Add bulk selection of list items (for delete for example)
    - Lists of resources should be ordered
- Templates
    - Render should be shown full page

Tests
-----
- Start covering with unit and integration tests

Tasks
-----
- Make pollster generic
- Find a solution for clearing finished tasks
