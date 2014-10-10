import Ember from 'ember';

export default Ember.Route.extend({
  setupController: function(controller, model) {
    controller.set('model', model);
    this.store.find('team').then(function(teams) {
      controller.set('allTeams', teams);
    });
  },

  actions: {
    submit: function(user) {
      var self = this;
      user.save().then(function(){
        self.transitionTo('user', user.get('id'));
      }, function(reason){
        window.console.log(reason);
      });
    }
  }
});
