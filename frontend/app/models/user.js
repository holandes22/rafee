import DS from 'ember-data';

export default DS.Model.extend({
    email: DS.attr('string'),
    fullName: DS.attr('string'),
    isStaff: DS.attr('boolean'),
});
