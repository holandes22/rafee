import Ember from 'ember';
import Pretender from 'pretender';
import startApp from '../helpers/start-app';
import preparePretender from '../helpers/prepare-pretender';
import ENV from 'rafee/config/environment';

var application;
var server;


module('Integration - Login', {
  setup: function() {
    application = startApp();
    server = new Pretender(function() {
      this.post(ENV.APP.API_NAMESPACE + '/auth-token', function(request) {
        var token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEyMzQ1Njc4OTAsIm5hbWUiOiJKb2huIERvZSIsImFkbWluIjp0cnVlfQ.eoaDVGTClRdfxUZXiPs3f8FmJDkDE_VCQFXqKxpLsts';
        var data = JSON.parse(request.requestBody);
        if (data.password === 'good') {
            return [200, {}, {token: token}];
        } else {
            return [400, {}, {non_field_errors: ['fake']}];
        }
      });
      this.get(ENV.APP.API_NAMESPACE + '/users/profile/', function(request) {
        var json = {"id":1,"username":"pp","email":"pp@pp.com","full_name":"Pepe Juarez","teams":[],"is_staff":true};
        return [200, {}, json];
      });
      this.get(ENV.APP.API_NAMESPACE + '/slideshows/', function(request) {
        return [200, {}, []];
      });
    });
    preparePretender(server);
  },
  teardown: function() {
    Ember.run(application, 'destroy');
    server.shutdown();
  }
});

test('it redirects to main page on succesful login', function() {
  expect(1);
  visit('/login');
  fillIn('.login-username', 'isidoro');
  fillIn('.login-password', 'good');
  click('.form-signin button');
  andThen(function() {
    equal(currentRouteName(), 'index');
  });
});


test('it shows error message on failed login', function() {
  expect(2);
  visit('/login');
  fillIn('.login-username', 'isidoro');
  fillIn('.login-password', 'bad');
  click('.form-signin button');

  andThen(function() {
    equal(find('.alert-danger').length, 1, 'it shows the failure messsage');
    equal(find('#loginFailureMessage').text(), 'fake', 'it shows message from server');
  });
});
