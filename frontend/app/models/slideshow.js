import DS from 'ember-data';

export default DS.Model.extend({

  name: DS.attr('string'),
  team: DS.belongsTo('team', { async: true }),
  templates: DS.attr('string'),
  transitionInterval: DS.attr('number'),
  cachingInterval: DS.attr('number'),

  templateNames: function() {
    return this.get('templates').split(',');
  }.property('templates'),

  templateList: function() {
    var templateList = [];
    this.get('templateNames').forEach(function(name) {
      var obj = {};
      obj.key = name.replace('/', '::');
      obj.name = name;
      templateList.push(obj);
    });
    return templateList;
  }.property('templates')

});
