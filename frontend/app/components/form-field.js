import Ember from 'ember';

export default Ember.Component.extend({

  errorMessages: Ember.computed('errors', function() {
    if (this.get('hasErrors')) {
      return this.get('errors')[this.key].join(' ');
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
