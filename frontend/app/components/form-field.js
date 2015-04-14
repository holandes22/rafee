import Ember from 'ember';

export default Ember.Component.extend({

  errorMessages: Ember.computed('errors', function() {
    var errors = this.get('errors');
    if (errors && errors.hasOwnProperty(this.key)) {
      return errors[this.key].join(' ');
    }
    return '';
  }),

  hasErrors: Ember.computed('errors', function() {
    var errors = this.get('errors');
    if (errors && errors.hasOwnProperty(this.key)) {
      return true;
    }
    return false;
  })

});
