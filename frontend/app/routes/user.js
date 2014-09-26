import Ember from 'ember';

export default Ember.Route.extend({

    model: function(user) {
        if (user.user_id === "1") {
            return {id: 1, fullName: 'pp juarez', email: 'pp@pp.com', username: 'pp'};
        } else {
            return {id: 2, fullName: 'Juan perez', email: 'juan@pp.com', username: 'juan'};
        }
    }
});
