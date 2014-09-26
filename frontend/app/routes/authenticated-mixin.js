import Ember from 'ember';

export default Ember.Route.extend({
    beforeModel: function(transition) {
        if (this.get('currentUser')) {
            this.intermediateTransitionTo(transition.targetName);
        } else {
            this.transitionTo('login');
        }
    }
});
