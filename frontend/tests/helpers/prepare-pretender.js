var prepareBody = function(body) {
  return JSON.stringify(body);
};

var prepareHeaders = function(headers) {
  headers['content-type'] = 'application/json';
  return headers;
};

export default function preparePrentender(server) {
  server.prepareBody = prepareBody;
  server.prepareHeaders = prepareHeaders;
  return server;
}
