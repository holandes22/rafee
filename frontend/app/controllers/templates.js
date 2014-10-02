import Ember from 'ember';
import ajax from 'ic-ajax';
import ENV from 'rafee/config/environment';

export default Ember.Controller.extend({

  renderResult: 'Rendering...',

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
        self.store.find('task', response.task).then(function(task){
          var poll = function() {
            if (task.get('status') === 'PENDING') {
              task.reload().then(function() {
                window.console.log('Polling task ', response.task);
              });
            } else {
              self.set('renderResult', task.get('result'));
              window.console.log(self.get('renderResult'));
              clearInterval(intervalId);
              task.deleteRecord();
            }
          };
          var intervalId = setInterval(poll, 1500);
        });
      });
    }

  }

});
