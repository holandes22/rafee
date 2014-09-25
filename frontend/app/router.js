import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
    this.resource('login');
    this.route('presentation', { path: 'presentation/:slideshow_id' });
});

export default Router;
