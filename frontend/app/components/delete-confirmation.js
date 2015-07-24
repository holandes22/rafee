import Ember from 'ember';

export default Ember.Component.extend({
  didInsertElement: function() {
    this.$().foundation();
  },
  actions: {
    delete: function() {
      this.$().foundation('dropdown', 'closeall');
      this.get('resource').destroyRecord();
    },
    cancel: function() {
      // TODO: For some reason, when I use data-dropdown-content
      // in the template, actions are not being triggered, so we
      // need here the logic to close the active ones
      this.$().foundation('dropdown', 'closeall');
    }
  }
});
