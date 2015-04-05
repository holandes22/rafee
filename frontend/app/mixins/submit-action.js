import Ember from 'ember';

export default Ember.Mixin.create({

  actions: {
    submit: function(model) {
      Ember.$('[class^="form-field-"]').removeClass('error');

      model.save().then(() => {
        this.transitionToRoute.apply(this, this.get('transitionToArgs'));
      }, (reason) => {
        this.set('errors', reason.errors);
        Ember.$.each(reason.errors, function(key) {
          Ember.$('.form-field-' + key).addClass('error');
        });
      });
    }
  }
});
