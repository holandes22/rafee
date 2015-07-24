import Ember from 'ember';

export default Ember.Mixin.create({

  actions: {
    submit: function(model) {

      model.save().then(() => {
        this.flashMessages.success(this.get('flashSuccessMessage'));
        this.transitionToRoute.apply(this, this.get('transitionToArgs'));
      }, () => {
        // TODO: If error is 400, show errors in form
        // otherwise, show a sticky flash message with
        // the error message
        this.set('errors', model.get('errors'));
      });
    }
  }
});
