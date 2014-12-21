import AuthRoute from 'rafee/routes/authenticated';

export default AuthRoute.extend({
    model: function() {
        return this.store.find('slideshow');
    }
});
