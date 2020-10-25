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
      /*onProxyReq: (proxyReq, req, res) => {
        const referer = req.headers.referer
        if (_.isString(referer)) {
          const ref = referer.replace(/^https:\/\/(.*)\//, target + '/')
          proxyReq.setHeader('Referer', ref)
        }

        //res.header("Access-Control-Allow-Origin", "https://localhost:3000");
      }*/
    })
  )
}