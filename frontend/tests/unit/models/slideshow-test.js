import {
  moduleForModel,
  test
} from 'ember-qunit';

moduleForModel('slideshow', 'Slideshow', {
  // Specify the other units that are required for this test.
  needs: ['model:user', 'model:team']
});

test('it exists', function(assert) {
  var model = this.subject();
  // var store = this.store();
  assert.ok(!!model);
});
