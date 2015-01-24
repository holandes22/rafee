import Ember from 'ember';
import Pretender from 'pretender';
import startApp from '../helpers/start-app';
import parsePostData from '../helpers/parse-post-data';
import ENV from 'rafee/config/environment';

var application;
var server;


module('Integration - Login', {
  setup: function() {
    application = startApp();
    server = new Pretender(function() {
      var headers = {'Content-Type': 'application/json'};
      this.post(ENV.APP.API_NAMESPACE + '/auth-token', function(request) {
        var data = JSON.parse(request.requestBody);
        var token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEyMzQ1Njc4OTAsIm5hbWUiOiJKb2huIERvZSIsImFkbWluIjp0cnVlfQ.eoaDVGTClRdfxUZXiPs3f8FmJDkDE_VCQFXqKxpLsts';
        if (data.password === 'good') {
            return [200, headers, JSON.stringify({token: token})];
        } else {
            return [400, headers, JSON.stringify({non_field_errors: ['fake']})];
        }
      });
      this.get(ENV.APP.API_NAMESPACE + '/users/profile/', function(request) {
        var json = {"id":1,"username":"pp","email":"pp@pp.com","full_name":"Pepe Juarez","teams":[],"is_staff":true};
        return [200, headers, JSON.stringify(json)];
      });
      this.get(ENV.APP.API_NAMESPACE + '/slideshows/', function(request) {
        return [200, headers, JSON.stringify([])];
      });
    });
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
