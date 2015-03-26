import Ember from 'ember';

export default Ember.View.extend({
  didInsertElement: function() {
    window.console.log('HERE');
    Ember.$(document).foundation();
  }
});
