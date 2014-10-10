import Ember from 'ember';

export default Ember.Route.extend({

  setupController: function(controller) {
    this.store.find('team').then(function(teams) {
      controller.set('allTeams', teams);
    });
  },

  actions: {
    submit: function() {
      var user = this.store.createRecord('user', {
        username: this.controller.get('username'),
        email: this.controller.get('email'),
        fullName: this.controller.get('fullName'),
        isStaff: this.controller.get('isStaff'),
      });
      var self = this;
      user.save().then(function(){
        // TODO: Since teams is async we must add them
        // after user is created, but addObjects is not
        // having effect. I believe since get('teams')
        // actually returns a PromiseArray
        var teams = self.controller.get('teams');
        if (teams) {
          user.get('teams').addObjects(teams);
        }
        self.transitionTo('users');
      }, function(reason){
        window.console.log(reason);
      });
    }
  }
});
