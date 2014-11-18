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
        var teams = self.controller.get('teams');
        if (teams) {
          user.get('teams').addObjects(teams);
        }
        user.save();
      }).then(function(){
        self.transitionTo('users');
      }, function(reason){
        //TODO: Handle the error properly
        window.console.log(reason);
      });
    }
  }
});
