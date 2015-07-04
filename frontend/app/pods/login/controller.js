import Ember from 'ember';


export default Ember.Controller.extend({


  disabled: Ember.computed('identification', 'password', function() {
    return Ember.isEmpty(this.get('identification')) || Ember.isEmpty(this.get('password'));
  }),

  actions: {
    authenticate: function() {

      var credentials = this.getProperties('identification', 'password');
      var authenticator = 'simple-auth-authenticator:token';

      this.get('session').authenticate(authenticator, credentials).then(() => {
          this.set('loginFailure', false);
        }, (response) => {
          var errorMessage = 'Unknown';
          if (response.non_field_errors) {
              errorMessage = response.non_field_errors;
          }
          this.set('loginFailure', true);
          this.set('errorMessage', errorMessage);
        });
    }
  }

});
