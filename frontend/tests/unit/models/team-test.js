import {
  moduleForModel,
  test
} from 'ember-qunit';

moduleForModel('team', 'Team', {
  // Specify the other units that are required for this test.
  needs: ['model:user', 'model:slideshow']
});

test('it exists', function(assert) {
  var model = this.subject();
  // var store = this.store();
  assert.ok(!!model);
});
