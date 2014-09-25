import Ember from 'ember';

export default Ember.Route.extend({

    model: function() {
        return [
            {
                id: 1,
                name: 'commits',
                templates: 'css/t1,css/t2',
                transition_interval: 15,
                caching_interval: 120
            },
            {
                id: 2,
                name: 'users',
                templates: 'css/user1,css/user2',
                transition_interval: 20,
                caching_interval: 120
            }
        ];
    }
});
