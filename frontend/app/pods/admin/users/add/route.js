import Ember from 'ember';

export default Ember.Route.extend({

  setupController: function(controller, model) {
    controller.set('model', model);
    this.store.find('team').then(function(teams) {
      controller.set('allTeams', teams);
    });
  },

  model: function() {
    return this.store.createRecord('user', {
      username: null,
      email: null,
      fullName: null,
      isStaff: null,
    });
  },

  actions: {
    submit: function(model) {
      var self = this;
      model.save().then(function(){
        self.transitionTo('admin.users');
      }, function(reason){
        //TODO: Handle the error properly
        window.console.log(reason);
      });
    }
  }
});
