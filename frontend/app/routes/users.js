import Ember from 'ember';

export default Ember.Route.extend({

    model: function() {
        return [
            {id: 1, fullName: 'pp juarez', email: 'pp@pp.com', username: 'pp'},
            {id: 2, fullName: 'Juan perez', email: 'juan@pp.com', username: 'juan'}
        ];
    }
});
