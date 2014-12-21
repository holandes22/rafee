import Ember from 'ember';

export default Ember.Controller.extend({

    actions: {
        logout: function() {
           window.sessionStorage.clear();
           window.location.replace('/');
        }
    }
});
