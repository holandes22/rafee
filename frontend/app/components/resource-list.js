import Ember from 'ember';


//TODO: Use Ember Inflector
var pluralize = function(word) {
  if (word === 'repository') {
    return 'repositories';
  }
  return word + 's';
};

export default Ember.Component.extend({

  tableHeaders: 'Name',

  tableValues: 'name',

  globalLinks: 'add',

  actionLinks: 'edit,details',

  getLink: function(action) {
    var resourceName = this.get('resourceName');
    var template = 'admin.%@.%@';
    switch(action) {
      case 'add':
      case 'preview':
        return template.fmt(pluralize(resourceName), action);
      case 'details':
        return template.fmt(pluralize(resourceName), resourceName);
      default:
        template = 'admin.%@.%@.%@';
        return template.fmt(pluralize(resourceName), resourceName, action);
    }
  },

  globalLinksMap: function() {
    return {
      'add': {
        title: 'Add ' + this.get('resourceName'),
        link: this.getLink('add')
      },
      'preview': {
        title: 'Preview',
        link: this.getLink('preview')
      }
    };
  }.property(),

  actionLinksMap: function() {
    return {
      'edit': { title: 'Edit', link: this.getLink('edit'), icon: 'glyphicon glyphicon-edit' },
      'details': { title: 'Details', link: this.getLink('details'), icon: 'glyphicon glyphicon-list' },
      'render': { title: 'Render', link: this.getLink('render'), icon: 'glyphicon glyphicon-eye-open' }
    };
  }.property(),

  getLinksArray: function(linkProperty, linkMapProperty) {
    var linkNames = this.get(linkProperty).split(',');
    var actionLinks = [];
    var self = this;
    Ember.$.each(linkNames, function(index, linkName) {
      actionLinks.push(self.get(linkMapProperty)[linkName]);
    });
    return actionLinks;
  },

  globalLinksArray: function() {
    return this.getLinksArray('globalLinks', 'globalLinksMap');
  }.property(),

  actionLinksArray: function() {
    return this.getLinksArray('actionLinks', 'actionLinksMap');
  }.property(),

  tableHeadersArray: function() {
    return this.get('tableHeaders').split(',');
  }.property('tableHeaders'),

  tableValuesArray: function() {
    return this.get('tableValues').split(',');
  }.property('tableValues')
});
