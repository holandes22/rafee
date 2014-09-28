import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route('login');
  this.route('profile');
  this.route('presentation', { path: 'presentation/:slideshow_id' });
  this.route('admin', function() {
    this.resource('users', function() {
      this.route('add');
      this.resource('user', { path: ':user_id' }, function() {
        this.route('edit');
        this.route('delete');
      });
    });
    this.resource('teams', function() {
      this.route('add');
      this.resource('team', { path: ':team_id' }, function() {
        this.route('edit');
        this.route('delete');
      });
    });
    this.resource('repositories', function() {
      this.route('add');
      this.resource('repository', { path: ':repository_id' }, function() {
        this.route('edit');
        this.route('delete');
      });
    });
    this.resource('slideshows', function() {
      this.resource('slideshow', { path: ':slideshow_id' });
    });
    this.resource('templates', function() {
      this.route('preview');
    });
  });
  this.route('template');
});

export default Router;
