import Ember from 'ember';

export default Ember.ArrayController.extend({

  sortProperties: ['fullName'],
  sortAscending: true,
  searchText: null,

  searchResults: function() {
    var searchText = this.get('searchText');
    var users = this.get('arrangedContent');
    if (!searchText) {
      return users.filter(function(user) {
        return user.get('id') !== 'profile';
      });
    }
    var rx = new RegExp(searchText, 'gi');
    return users.filter(function(user) {
      var fullName = user.get('fullName');
      if (fullName) {
        return user.get('fullName').match(rx) && user.get('id') !== 'profile';
      }
      return false;
    });
  }.property('arrangedContent', 'model', 'searchText')
});

