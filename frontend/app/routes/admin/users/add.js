import Ember from 'ember';

export default Ember.Route.extend({

  setupController: function(controller) {
    this.store.find('team').then(function(teams) {
      controller.set('teams', teams);
    });
  },

  actions: {
    submit: function() {
      var self = this;
      window.console.log(self.controller);
      var user = this.store.createRecord('user', {
        username: self.controller.get('username'),
        email: self.controller.get('email'),
        fullName: self.controller.get('fullName'),
        isStaff: self.controller.get('isStaff'),
        //teams: self.controller.get('selectedTeams')
      });
      user.save().then(function(){
        self.transitionTo('users');
      }, function(reason){
        window.console.log(reason);
      });
    }
  }
});
