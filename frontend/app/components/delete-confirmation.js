import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'a',
  didInsertElement: function() {
      var component = this,
      content = this.$('.delete-confirmation-popover-content');
      component.$().popover({
          title: 'Are you sure?',
          animation: true,
          html: true,
          content: content,
          placement: 'auto',
      }).on('show.bs.popover', function() {
          // TODO: Hide all other popovers
          content.removeClass('hide');
      });
  },
  willDestroyElement: function() {
    this.$().popover('destroy');
  },
  actions: {
    delete: function() {
      this.get('resource').destroyRecord();
    },
    cancel: function() {
      this.$().popover('hide');
    }
  }
});
