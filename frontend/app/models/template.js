import DS from 'ember-data';

export default DS.Model.extend({

  name: DS.attr('string'),
  dataSourceUrl: DS.attr('string')

});
