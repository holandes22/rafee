import {
  moduleForModel,
  test
} from 'ember-qunit';

moduleForModel('user', 'User', {
  // Specify the other units that are required for this test.
  needs: ['model:team', 'model:slideshow']
});

test('it exists', function(assert) {
  var model = this.subject();
  // var store = this.store();
  assert.ok(!!model);
});
