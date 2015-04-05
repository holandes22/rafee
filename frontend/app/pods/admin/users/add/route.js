import Ember from 'ember';

export default Ember.Route.extend({

  setupController: function(controller, model) {
    this._super(controller, model);
    this.controller.set('errors', null);
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

});
