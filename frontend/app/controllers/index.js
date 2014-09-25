import Ember from 'ember';

export default Ember.Controller.extend({
    selectedSlideshow: null,

    templateList: function() {
        return this.get('selectedSlideshow').templates.split(',');
    }.property('selectedSlideshow')
});
