import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
  location: config.locationType
});

// Altough it seems odd, we need to laid down delete
// and edit routes next to the resource since we want
// their templates to be rendere in the main resource
// outlet. See a good explanation why in this blog post:
// http://hashrocket.com/blog/posts/ember-routing-the-when-and-why-of-nesting
//
Router.map(function() {
  this.route('login');
  this.route('profile');
  this.route('presentation', { path: 'presentation/:slideshow_id' });

  this.route('admin', function() {
    this.route('users/add');
    this.resource('users', function() {
      this.resource('user.delete', { path: ':user_id/delete' });
      this.resource('user.edit', { path: ':user_id/edit' });
      this.resource('user', { path: ':user_id' });
    });

    this.route('teams/add');
    this.resource('teams', function() {
      this.resource('team.delete', { path: ':team_id/delete' });
      this.resource('team.edit', { path: ':team_id/edit' });
      this.resource('team', { path: ':team_id' });
    });

    this.resource('repositories', function() {
      this.route('add');
      this.resource('repository', { path: ':repository_id' }, function() {
        this.route('delete');
      });
    });

    this.route('slideshows/add');
    this.resource('slideshows', function() {
      this.resource('slideshow.delete', { path: ':slideshow/delete' });
      this.resource('slideshow.edit', { path: ':slideshow_id/edit' });
      this.resource('slideshow', { path: ':slideshow_id' });
    });

    this.route('templates/preview');
    this.resource('templates', function() {
      this.resource('template', { path: ':template_id' }, function() {
        this.route('render');
      });
    });
  });
});

export default Router;
