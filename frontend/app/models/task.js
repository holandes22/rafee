import Ember from 'ember';
import DS from 'ember-data';

export default DS.Model.extend({

  status: DS.attr('string'),
  result: DS.attr('string'),
  traceback: DS.attr('string'),

  poll: function(interval) {
    if (!interval) {
      interval = 1000;
    }
    Ember.run.later(this, function() {
       if (this.get('status') === 'PENDING') {
          this.reload().then(function(task) {
            task.poll(interval);
          });
        } else {
          // TODO: Do we want this logic here?
          // a controller might still need to get
          // more info from the task. Disadvantage is
          // having to repeat cleanup logic accross controllers
          this.deleteRecord();
        }
    }, interval);
  }.observes('didLoad'),
});
