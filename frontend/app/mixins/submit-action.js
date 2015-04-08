import Ember from 'ember';

export default Ember.Mixin.create({

  actions: {
    submit: function(model) {
      Ember.$('[class^="form-field-"]').removeClass('error');

      model.save().then(() => {
        this.flashMessages.success(this.get('flashSuccessMessage'));
        this.transitionToRoute.apply(this, this.get('transitionToArgs'));
      }, (reason) => {
        // TODO: If error is 400, show errors in form
        // otherwise, show a sticky flash message with
        // the error message
        this.set('errors', reason.errors);
        Ember.$.each(reason.errors, function(key) {
          Ember.$('.form-field-' + key).addClass('error');
        });
      });
    }
  }
});
