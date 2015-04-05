import Ember from 'ember';
import UserRouteMixin from 'rafee/mixins/user-route';

export default Ember.Route.extend(UserRouteMixin, {

  model: function() {
    return this.store.createRecord('user', {
      username: null,
      email: null,
      fullName: null,
      isStaff: null,
    });
  }

});
