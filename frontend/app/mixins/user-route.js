import Ember from 'ember';

export default Ember.Mixin.create({

  setupController: function(controller, model) {
    this._super(controller, model);
    this.controller.set('errors', null);
    Ember.$('[class^="form-field-"]').removeClass('error');
    this.store.find('team').then(function(teams) {
      controller.set('allTeams', teams);
    });
  }

});
