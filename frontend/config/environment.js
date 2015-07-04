/* jshint node: true */

module.exports = function(environment) {
  var ENV = {
    modulePrefix: 'rafee',
    podModulePrefix: 'rafee/pods',
    environment: environment,
    baseURL: '/',
    locationType: 'auto',
    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. 'with-controller': true
      }
    },

    APP: {
      // Here you can pass flags/options to your application instance
      // when it is created
    }
  };
  ENV.contentSecurityPolicy = {
    'img-src': "'self'",
    'style-src': "'self' 'unsafe-inline'"
  };

  ENV['simple-auth'] = {};

  if (environment === 'development') {
    // ENV.APP.LOG_RESOLVER = true;
    // ENV.APP.LOG_ACTIVE_GENERATION = true;
    // ENV.APP.LOG_TRANSITIONS = true;
    // ENV.APP.LOG_TRANSITIONS_INTERNAL = true;
    // ENV.APP.LOG_VIEW_LOOKUPS = true;

    ENV.APP.API_HOST = 'http://localhost:8888';
    ENV.APP.API_NAMESPACE = 'api/v1';
  }

  if (environment === 'test') {
    // Testem prefers this...
    ENV.baseURL = '/';
    ENV.locationType = 'none';

    // keep test console output quieter
    ENV.APP.LOG_ACTIVE_GENERATION = false;
    ENV.APP.LOG_VIEW_LOOKUPS = false;

    ENV.APP.rootElement = '#ember-testing';

    ENV.APP.API_HOST = '';
    ENV.APP.API_NAMESPACE = 'api/v1';

    ENV['simple-auth'].store = 'simple-auth-session-store:ephemeral';
  }

  if (environment === 'production') {
    ENV.APP.API_HOST = 'https://rafee.com';
    ENV.APP.API_NAMESPACE = 'v1';

  }

  ENV.APP.API_URL = ENV.APP.API_HOST + '/' + ENV.APP.API_NAMESPACE;

  ENV['simple-auth'].authorizer = 'simple-auth-authorizer:token';
  ENV['simple-auth'].crossOriginWhitelist = [ENV.APP.API_HOST];

  ENV['simple-auth-token'] = {
    serverTokenEndpoint: ENV.APP.API_URL + '/auth-token',
    authorizationPrefix: 'JWT '
  };

  return ENV;
};
