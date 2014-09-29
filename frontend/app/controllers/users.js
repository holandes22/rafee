import Ember from 'ember';

export default Ember.ArrayController.extend({

  sortProperties: ['fullName'],
  sortAscending: true,
  searchText: null,

  searchResults: function() {
    var searchText = this.get('searchText');
    var users = this.get('arrangedContent');
    if (!searchText) {
      return users;
    }
    return users.filter(function(user) {
      var fullName = user.get('fullName');
      if (fullName) {
        return user.get('fullName').match(searchText);
      }
      return false;
    });
  }.property('arrangedContent', 'searchText')
});

