import Ember from 'ember';
import Session from 'simple-auth/session';


export var initialize = function(container) {
  Session.reopen({
    setCurrentUser: function() {
      var token = this.get('token');
      var self = this;

      if (!Ember.isEmpty(token)) {
        return container.lookup('store:main').find('user', 'profile').then(function(user) {
          self.set('currentUser', user);
        });
      }
    }.observes('token')
  });
};

export default {
  name: 'set-session',
  after: 'store',
  before: 'simple-auth',
  initialize: initialize
};
