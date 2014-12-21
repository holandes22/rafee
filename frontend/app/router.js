import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
  location: config.locationType
});

// Altough it seems odd, we need to laid down delete
// and edit routes next to the resource since we want
// their templates to be rendered in the main resource
// outlet. See a good explanation why, in this blog post:
// http://hashrocket.com/blog/posts/ember-routing-the-when-and-why-of-nesting

Router.map(function() {
  this.route('login');
  this.route('profile');
  this.route('presentation', { path: 'presentation/:slideshow_id' });

  this.route('admin', function() {

    this.route('users.add', { path: 'users/add' });
    this.route('users', function() {
      this.route('user', { path: ':user_id' }, function() {
        this.route('delete');
        this.route('edit');
      });
    });

    this.route('teams.add', { path: 'teams/add' });
    this.route('teams', function() {
      this.route('team', { path: ':team_id' }, function() {
        this.route('delete');
        this.route('edit');
      });
    });

    this.route('repositories.add', { path: 'repositories/add' });
    this.route('repositories', function() {
      this.route('repository', { path: ':repository_id' }, function() {
        this.route('delete');
      });
    });

    this.route('slideshows.add', { path: 'slideshows/add' });
    this.route('slideshows', function() {
      this.route('slideshow', { path: ':slideshow_id' }, function() {
        this.route('delete');
        this.route('edit');
      });
    });

    this.route('templates.preview', { path: 'templates/preview' });
    this.route('templates', function() {
      this.route('template', { path: ':template_id' }, function() {
        this.route('render');
      });
    });
  });
});

export default Router;
