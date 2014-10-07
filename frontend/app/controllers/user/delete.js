import Ember from 'ember';

export default Ember.Controller.extend({

  needs: 'users',

  actions: {
    delete: function() {
      var self = this;
      this.get('model').destroyRecord().then(function() {
        self.get('controllers.users').get('model').update();
      }).then(function() {
        // TODO: this is mighty ugly, but for some reason
        // updating model is not trigerring a searchResult
        self.get('controllers.users').set('searchText', '');
        self.transitionToRoute('users');
      });
    }
  },

  cancel: function() {
    this.transitionToRoute('users');
  }
});
