import Ember from 'ember';
import { module, test } from 'qunit';
import Pretender from 'pretender';
import startApp from '../helpers/start-app';
import preparePretender from '../helpers/prepare-pretender';
import ENV from 'rafee/config/environment';

var application;
var server;

var user = {
  id: 1,
  username: 'geralt',
  email: 'geralt@kaedwen.com',
  full_name: 'Geralt of Rivia',
  teams: [],
  is_staff: true
};

var token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBwIiwidXNlcl9pZCI6MSwiZW1haWwiOiJwcEBwcC5jb20iLCJleHAiOjE0MjkyNTA1NDZ9.C8WtJ7Glnw7-IqbI1muJtdkpGgEkf1S6CooMn34tQZo';

module('Integration - Login', {
  beforeEach: function() {
    application = startApp();
    server = new Pretender(function() {
      this.post(ENV.APP.API_NAMESPACE + '/auth-token', function(request) {
        var data = JSON.parse(request.requestBody);
        if (data.username === 'admin') {
          user.is_staff = true;
        } else {
          user.is_staff = false;
        }
        if (data.password === 'good') {
            return [200, {}, { token: token }];
        } else {
            return [400, {}, { non_field_errors: ['fake'] }];
        }
      });
      this.get(ENV.APP.API_NAMESPACE + '/users/profile/', function() {
        return [200, {}, user];
      });
      this.get(ENV.APP.API_NAMESPACE + '/slideshows/', function() {
        return [200, {}, []];
      });
    });
    preparePretender(server);
  },
  afterEach: function() {
    Ember.run(application, 'destroy');
    server.shutdown();
  }
});

test('it redirects to main page on succesful login', function(assert) {
  assert.expect(2);
  visit('/login');
  fillIn('.login-username', 'admin');
  fillIn('.login-password', 'good');
  click('.form-signin button');
  andThen(function() {
    assert.equal(currentRouteName(), 'index');
    assert.equal(find('.navbar-admin').length, 1, 'it shows the admin dashboar link');
  });
});

test('it hides admin dashboard link if user is not staff', function(assert) {
  assert.expect(2);
  visit('/login');
  fillIn('.login-username', 'notAdmin');
  fillIn('.login-password', 'good');
  click('.form-signin button');
  andThen(function() {
    assert.equal(currentRouteName(), 'index');
    assert.equal(find('.navbar-admin').length, 0, 'it hides the admin dashboar link');
  });
});


test('it shows error message on failed login', function(assert) {
  assert.expect(3);
  visit('/login');
  fillIn('.login-username', 'admin');
  fillIn('.login-password', 'bad');
  click('.form-signin button');

  andThen(function() {
    assert.equal(find('.alert-box').length, 1, 'it shows the failure messsage');
    assert.equal(find('#loginFailureMessage').text(), 'fake', 'it shows message from server');
    assert.equal(find('.navbar-admin').length, 0, 'it hides the admin dashboard link');
  });
});
