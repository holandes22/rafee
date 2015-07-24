import Ember from 'ember';

export default Ember.Component.extend({

  errorMessages: Ember.computed('errors', function() {
    console.log(this.get('val'));
    if (this.get('hasErrors')) {
      const key = this.get('key'),
            errors = this.get(`errors.${key}`);
      return errors.map((o) => {return o.message;}).join(' ');
    }
    return '';
  }),

  hasErrors: Ember.computed('errors', function() {
    var key = this.get('key');
    if (this.get(`errors.${key}`)) {
      return true;
    }
    return false;
  })

});
