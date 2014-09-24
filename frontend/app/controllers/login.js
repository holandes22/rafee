import Ember from 'ember';
import ajax from 'ic-ajax';
import ENV from 'rafee/config/environment';


export default Ember.Controller.extend({
    username: null,
    password: null,

    disabled: function() {
        return Ember.empty(this.get('username')) || Ember.empty(this.get('password'));
    }.property('username', 'password'),

    actions: {
        signIn: function() {
            var self = this;
            var url = ENV.APP.API_HOST + '/' + ENV.APP.API_NAMESPACE + '/auth-token';
            ajax(url, {
                type: 'POST',
                data: this.getProperties('username', 'password')
            }).then(function(response) {
                // TODO: Store token in local storage
                window.console.log(response.token);
                self.setProperties({success: true, failure: false});
            }, function(reason){
                self.setProperties({success: false, failure: true});
                var errorMessage = 'Error';
                var status = reason.jqXHR.status;
                var response = reason.jqXHR.responseJSON;
                if (status === 400) {
                    errorMessage = response.non_field_errors;
                }
                self.set('errorMessage', errorMessage);
            });
        }
    }
});
