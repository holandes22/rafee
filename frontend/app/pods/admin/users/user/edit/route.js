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
        self.transitionTo('admin.users.user', user.get('id'));
      }, function(reason){
        window.console.log(reason);
      });
    },
    //TODO: put this in a mixin
    willTransition: function(transition) {
      var model = this.controller.get('model');
      if (model.get('isDirty')) {
          if (confirm("Are you sure you want to abandon progress?")) {
            model.rollback();
          } else {
            transition.abort();
          }
      } else {
        // Bubble the `willTransition` action so that
        // parent routes can decide whether or not to abort.
        return true;
      }
    }
  }
});
