import Ember from 'ember';
import ajax from 'ic-ajax';
import ENV from 'rafee/config/environment';

export default Ember.Controller.extend({

  task: null,
  renderResult: function() {
    return this.task? this.task.get('result') : 'Rendering...';
  }.property('task.result'),


  actions: {

    render: function(name) {
      var self = this;
      var urlPrefix = ENV.APP.API_HOST + '/' + ENV.APP.API_NAMESPACE + '/';
      var url =  urlPrefix + 'slide/';
      var data = { template_name: name };
      var setHeaders =  function (request) {
        var token = window.sessionStorage.getItem('loggedInUserToken');
        request.setRequestHeader('Authorization', 'Token ' + token);
      };
      ajax(url, {
        type: 'POST', beforeSend: setHeaders, data: data
      }).then(function(response) {
        return self.store.find('task', response.task);
      }).then(function(task) {
        self.set('task', task);
        task.poll();
      }); // TODO: Catch errors
    }

  }

});
