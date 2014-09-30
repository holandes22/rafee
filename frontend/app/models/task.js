import DS from 'ember-data';

export default DS.Model.extend({

  status: DS.attr('string'),
  result: DS.attr('string'),
  traceback: DS.attr('string')

});
