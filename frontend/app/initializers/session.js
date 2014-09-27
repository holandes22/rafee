import DS from 'ember-data';


export var initialize = function(container, app) {
    var token = window.sessionStorage.getItem('loggedInUserToken');
    if (token) {
        DS.RESTAdapter.reopen({
            headers: {'Authorization': 'Token ' + token}
        });
        app.deferReadiness();
        container.lookup('store:main').find('user', 'profile').then(function(user){
            container.register('user:current', user, {instantiate: false});
            container.injection('route', 'currentUser', 'user:current');
            container.injection('controller', 'currentUser', 'user:current');
            app.advanceReadiness();
        }, function(reason) {
            // TODO: Handle failure case properly
            app.advanceReadiness();
        });
     }
};

export default {
      name: 'set-session',
      after: 'store',

      initialize: initialize
};
