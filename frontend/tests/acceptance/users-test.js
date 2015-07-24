import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';
import Pretender from 'pretender';
import ENV from 'rafee/config/environment';
import preparePretender from '../helpers/prepare-pretender';
import 'simple-auth-testing/test-helpers';

var application;
var server;

var admin = {
  id: 1,
  username: 'geralt',
  email: 'geralt@kaedwen.com',
  full_name: 'Geralt of Rivia',
  teams: [],
  is_staff: true
};

var user = {
  id: 2,
  username: 'zoltan',
  email: 'zoltan@vizima.com',
  full_name: 'Zoltan Chivay',
  teams: [],
  is_staff: false
};

var users = [admin, user];


module('Acceptance: Users', {
  beforeEach: function() {
    application = startApp();
    server = new Pretender(function() {
      this.get(ENV.APP.API_NAMESPACE + '/users/', function() {
        return [200, {}, users];
      });
      this.get(ENV.APP.API_NAMESPACE + '/users/:user_id', function() {
        return [200, {}, currentSession().get('currentUser')];
      });
    });
    preparePretender(server);
  },
  afterEach: function() {
    Ember.run(application, 'destroy');
    server.shutdown();
  }
});

test('visiting /admin/users', function(assert) {
  authenticateSession();
  currentSession().set('currentUser', admin);
  visit('/admin/users');

  andThen(function() {
    assert.equal(currentRouteName(), 'admin.users.index');
  });
});

test('visiting /admin/users redirects to login if not authenticated', function(assert) {
  currentSession().set('currentUser', admin);
  invalidateSession();
  visit('/admin/users');

  andThen(function() {
    assert.equal(currentRouteName(), 'login');
  });
});


test('visiting /admin/users gives error if user not admin', function(assert) {
  authenticateSession();
  currentSession().set('currentUser', user);
  visit('/admin/users');

  andThen(function() {
    assert.equal(currentRouteName(), 'error');
    assert.equal(find('#error-message').text(), 'You must be a staff member to access this path.');
  });
});
