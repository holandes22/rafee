import Ember from 'ember';

export default Ember.Route.extend({

  activate: function() {
    this.controllerFor('user').set('showDeleteConfirmation', true);
  },
  deactivate: function() {
    this.controllerFor('user').set('showDeleteConfirmation', false);
  }
});
