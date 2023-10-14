const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function (app) {
  app.use(
    '/facebook-dialog',
    createProxyMiddleware({
      target: 'https://www.facebook.com',
      changeOrigin: true,
      pathRewrite: {
        '^/facebook-dialog': '/dialog/oauth',
      },
    })
  );
};
