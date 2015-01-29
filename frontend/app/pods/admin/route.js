import Ember from 'ember';
import AuthenticatedRouteMixin from 'simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, {

  beforeModel: function(transition) {
    this._super(transition);
    var self = this;
    this.get('store').find('user', 'profile').then(function(user) {
      if (!user.get('isStaff')) {
        transition.abort();
        var errorMessage = 'You must be a staff member to access this path.';
        self.controllerFor('error').set('errorMessage', errorMessage);
        self.transitionTo('error');
      }
    }, function(error) {
      // TODO: error handler
      window.console.log(error);
    });
  }
});
