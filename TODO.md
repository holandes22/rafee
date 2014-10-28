TODO: open tickets for each item

Backend
-------

- Try out postgresql 9.4

General
-------
- try json api
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

Templates
---------
- Make search a component
- Refactor templates for reuse

Controllers
-----------
- Generic CRUD

Routes
------
- All routes show extend the authenticated mixins


Tests
-----
- Start covering with unit and integration tests

Tasks
-----
- Make pollster generic
- Find a solution for clearing finished tasks
