import Ember from 'ember';
import Pretender from 'pretender';
import startApp from '../helpers/start-app';
import ENV from 'rafee/config/environment';

var App;
var server;

function parsePostData(query) {
  var result = {};
  query.split("&").forEach(function(part) {
    var item = part.split("=");
    result[item[0]] = decodeURIComponent(item[1]);
  });
  return result;
}


module('Integration - Login', {
  setup: function() {
    App = startApp();
    server = new Pretender(function() {
        this.post(ENV.APP.API_NAMESPACE + '/auth-token', function(request) {
            var data = parsePostData(request.requestBody);
            if (data.password === 'good') {
                return [200, {'Content-Type': 'application/json'}, JSON.stringify({token: 'fake'})];
            } else {
                return [400, {'Content-Type': 'application/json'}, JSON.stringify({non_field_errors: ['fake']})];
            }
        });
    });
  },
  teardown: function() {
    Ember.run(App, 'destroy');
    server.shutdown();
  }
});

test('It can login successfully', function() {
  visit('/login');
  fillIn('.login-username', 'isidoro');
  fillIn('.login-password', 'good');
  click('.form-signin button');

  andThen(function() {
    equal(find('.alert-success').length, 1, 'it shows the success messsage');
    equal(find('.alert-danger').length, 0, 'it hides the failure messsage');
  });
});

test('It shows error message on failed login', function() {
  visit('/login');
  fillIn('.login-username', 'isidoro');
  fillIn('.login-password', 'bad');
  click('.form-signin button');

  andThen(function() {
    equal(find('.alert-danger').length, 1, 'it shows the failure messsage');
    equal(find('.alert-success').length, 0, 'it hides the success messsage');
  });
});
