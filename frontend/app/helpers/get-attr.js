import Ember from 'ember';

export default Ember.Handlebars.makeBoundHelper(function(obj, name) {
  var property = obj.get(name);
  if (property === undefined || property === '') {
    property = 'Not set';
  }
  return property;
});
