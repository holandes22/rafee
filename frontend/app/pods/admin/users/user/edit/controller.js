import Ember from 'ember';
import SubmitActionMixin from 'rafee/mixins/submit-action';

export default Ember.Controller.extend(SubmitActionMixin, {

  transitionToArgs: Ember.computed('model.id', function() {
    return ['admin.users.user', this.model.get('id')];
  })

});
