import Ember from 'ember';
import LoginControllerMixin from 'simple-auth/mixins/login-controller-mixin';


export default Ember.Controller.extend(LoginControllerMixin, {

authenticator: 'simple-auth-authenticator:token',

  disabled: function() {
    return Ember.isEmpty(this.get('identification')) || Ember.isEmpty(this.get('password'));
  }.property('identification', 'password'),

});
