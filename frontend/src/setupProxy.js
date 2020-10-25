const { createProxyMiddleware } = require('http-proxy-middleware')
const _ = require('lodash')

const target = `https://${process.env.REACT_APP_MAIN_API_BASE}`
console.log(target)
const filter = function(pathname, req) {
  return pathname.match('^/api')
}

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