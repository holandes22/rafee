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
    Ember.run(application, 'destroy');
    server.shutdown();
  }
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
