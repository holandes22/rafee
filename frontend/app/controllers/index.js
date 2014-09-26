import Ember from 'ember';

export default Ember.Controller.extend({
    selectedSlideshow: null,

    templateList: function() {
        if (this.get('selectedSlideshow')) {
            return this.get('selectedSlideshow').templates.split(',');
        }
    }.property('selectedSlideshow')
});
