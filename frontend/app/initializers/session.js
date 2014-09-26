import ajax from 'ic-ajax';

import ENV from 'rafee/config/environment';


export var initialize = function(container, app) {
    /* Once we start using ember data, uncomment the code below
    DS.RESTAdapter.reopen({
        namespace: ENV.APP.API_NAMESPACE,
        host: ENV.APP.API_HOST
    });
    */

    var token = window.sessionStorage.getItem('loggedInUserToken');
    if (token) {
        app.deferReadiness();
        var url = ENV.APP.API_HOST + '/' + ENV.APP.API_NAMESPACE + '/users/profile';
        ajax({
            url: url,
            type: 'GET',
            beforeSend: function (request) {
                request.setRequestHeader('Authorization', 'Token ' + token);
            },
        }).then(function(userProfile) {
            // Once we start using ember data, uncomment the code below
            // DS.RESTAdapter.reopen({
            //    headers: {'Authorization': 'Token ' + token}
            // });
            // container.lookup('store:main').find('user', userProfile.user.id).then(function(user){
                // container.register('user:current', user, {instantiate: false});
                container.register('user:current', userProfile, {instantiate: false});
                container.injection('route', 'currentUser', 'user:current');
                container.injection('controller', 'currentUser', 'user:current');
                app.advanceReadiness();
            // });
        });
     }
};

export default {
      name: 'set-session',

      initialize: initialize
};
