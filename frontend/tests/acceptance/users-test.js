import Ember from 'ember';
import startApp from '../helpers/start-app';
import Pretender from 'pretender';
import ENV from 'rafee/config/environment';
import 'simple-auth-testing/test-helpers';

var application;
var server;

var user = {
  "id":1,"username":"p","email":"pp@p.com","full_name":"PJ","teams":[],"is_staff":true
};

module('Acceptance: Users', {
  setup: function() {
    application = startApp();
    server = new Pretender(function() {
      var headers = {'Content-Type': 'application/json'};
      this.get(ENV.APP.API_NAMESPACE + '/users/', function(request) {
        return [200, headers, JSON.stringify([user])];
      });
    });
  },
  teardown: function() {
    Ember.run(application, 'destroy');
    server.shutdown();
  }
});

test('visiting /admin/users', function() {
  authenticateSession();
  currentSession().set('currentUser', user);
  visit('/admin/users');

  andThen(function() {
    equal(currentRouteName(), 'admin.users.index');
  });
});
