import Ember from 'ember';

export default Ember.Route.extend({

  model: function(team) {
    return this.store.find('team', team.team_id);
  }
});
