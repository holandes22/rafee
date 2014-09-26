import DS from 'ember-data';

export default DS.Model.extend({
    username: DS.attr('string'),
    email: DS.attr('string'),
    fullName: DS.attr('string'),
    isStaff: DS.attr('boolean'),
    teams: DS.hasMany('team', { async: true })
});
