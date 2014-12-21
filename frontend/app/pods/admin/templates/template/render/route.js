import Ember from 'ember';
import ajax from 'ic-ajax';
import ENV from 'rafee/config/environment';

export default Ember.Route.extend({

  setupController: function(controller, model) {
    controller.set('model', model);
    var self = this;
    var urlPrefix = ENV.APP.API_HOST + '/' + ENV.APP.API_NAMESPACE + '/';
    var url =  urlPrefix + 'slide/';
    var data = { template_name: model.get('name') };
    var setHeaders =  function (request) {
      var token = window.sessionStorage.getItem('loggedInUserToken');
      request.setRequestHeader('Authorization', 'Token ' + token);
    };
    ajax(url, {
      type: 'POST', beforeSend: setHeaders, data: data
    }).then(function(response) {
      return self.store.find('task', response.task);
    }).then(function(task) {
      controller.set('task', task);
      task.poll();
    }); // TODO: Catch errors
  },

  deactivate: function() {
    var task = this.controllerFor('admin/templates/template/render').get('task');
    if (task) {
      // We don't want to keep polling if we exit the route
      task.stopPolling();
    }
  }
});
