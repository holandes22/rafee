import Ember from 'ember';
import SubmitActionMixin from '../../../mixins/submit-action';
import { module, test } from 'qunit';

module('SubmitActionMixin');

// Replace this with your real tests.
test('it works', function(assert) {
  var SubmitActionObject = Ember.Object.extend(SubmitActionMixin);
  var subject = SubmitActionObject.create();
  assert.ok(subject);
});
