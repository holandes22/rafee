import Ember from 'ember';

export default Ember.Route.extend({

    model: function(user) {
        return this.store.find('user', user.user_id);
    }
});
