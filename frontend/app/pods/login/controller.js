import Ember from 'ember';
import LoginControllerMixin from 'simple-auth/mixins/login-controller-mixin';


export default Ember.Controller.extend(LoginControllerMixin, {

  authenticator: 'simple-auth-authenticator:jwt',

  disabled: function() {
    return Ember.isEmpty(this.get('identification')) || Ember.isEmpty(this.get('password'));
  }.property('identification', 'password'),

  actions: {
    authenticate: function() {
      var self = this;
      this._super().then(function() {
        self.set('loginFailure', false);
      }, function(response) {
        self.set('loginFailure', true);
        var errorMessage = 'Unknown';
        if (response.non_field_errors) {
            errorMessage = response.non_field_errors;
        }
        self.set('errorMessage', errorMessage);
      });
    }
  }

});
