import Ember from 'ember';
import startApp from '../helpers/start-app';

var application;

module('Acceptance: Users', {
  setup: function() {
    application = startApp();
  },
  teardown: function() {
    Ember.run(application, 'destroy');
  }
});

test('visiting /admin/users', function() {
  visit('/admin/users');

  andThen(function() {
    equal(currentPath(), '/admin/users');
  });
});
