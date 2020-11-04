const { createProxyMiddleware } = require('http-proxy-middleware')

const target = `${process.env.REACT_APP_MAIN_API_BASE}`

module.exports = function(app) {
  app.use(
    createProxyMiddleware('/api/**', {
      target: target,
      changeOrigin: true,
      onProxyRes: function (proxyRes, req, res) {
        proxyRes.headers['Access-Control-Allow-Origin'] = '*';
      }
    })
  )
}