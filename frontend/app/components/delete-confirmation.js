import Ember from 'ember';

export default Ember.Component.extend({
  didInsertElement: function() {
    this.$().foundation();
  },
  dataDropdownId: function() {
    return 'drop-delete-confirmation-' + this.resource.id;
  }.property('resource'),
  actions: {
    delete: function() {
      this.$().foundation('dropdown', 'closeall');
      this.resource.destroyRecord();
    },
    cancel: function() {
      // TODO: For some reason, when I use data-dropdown-content
      // in the template, actions are not being triggered so we
      // the logic to close the active ones
      this.$().foundation('dropdown', 'closeall');
    }
  }
});
