import Ember from 'ember';

export default Ember.Controller.extend({
  task: null,  // this is set from the route

  renderResult: function() {
    if (this.task) {
      return this.task.get('result');
    }
  }.property('task.result'),
});
