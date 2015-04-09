import Ember from 'ember';

export default Ember.Component.extend({

  errorMessages: Ember.computed('errors', 'key', function() {
    var errors = this.get('errors');
    if (errors) {
      var key = this.get('key');
      return errors[key].join(' ');
    }
    return '';
  })

});
