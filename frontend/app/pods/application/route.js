import Ember from 'ember';
import ApplicationRouteMixin from 'simple-auth/mixins/application-route-mixin';

export default Ember.Route.extend(ApplicationRouteMixin, {
  beforeModel(transition) {
    this._super(transition);
    if (this.session.isAuthenticated) {
      return this._setCurrentUser();
    }
  },
  actions: {
    sessionAuthenticationSucceeded() {
      this._super();
      this._setCurrentUser();
    },
  },
  _setCurrentUser() {
    return this.store.find('user', 'profile').then(user => {
      return this.get('currentUser').set('content', user);
    });
  }
});
