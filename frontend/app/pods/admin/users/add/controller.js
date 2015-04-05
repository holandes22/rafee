import Ember from 'ember';

export default Ember.Controller.extend({

  // TODO: Move to a mixin for re-use
  actions: {
    submit: function(model) {
      Ember.$('[class^="form-field-"]').removeClass('error');

      model.save().then(() => {
        this.transitionToRoute('admin.users');
      }, (reason) => {
        this.set('errors', reason.errors);
        Ember.$.each(reason.errors, function(key) {
          Ember.$('.form-field-' + key).addClass('error');
        });
      });
    }
  }
});
