import AuthMixin from 'rafee/routes/authenticated-mixin';

export default AuthMixin.extend({
    model: function() {
        return this.store.find('slideshow');
    }
});
