import Ember from 'ember';
import ajax from 'ic-ajax';

export default Ember.Controller.extend({
    username: null,
    password: null,
    response: null,

    disabled: function() {
        return Ember.empty(this.get('username')) || Ember.empty(this.get('password'));
    }.property('username', 'password'),

    actions: {
        signIn: function() {
            var self = this;

            // TODO: Take API prefix from config
            ajax('/api/v1/auth-token', {
                type: 'POST',
                data: this.getProperties('username', 'password')
            }).then(function(response) {
                // TODO: Store in local storage
                self.set('response', response);
            });
        }
    }
});
