import Ember from 'ember';

function renderedTemplate(value) {
  return new Ember.Handlebars.SafeString(value);
}

export {
  renderedTemplate
};

export default Ember.Handlebars.makeBoundHelper(renderedTemplate);
