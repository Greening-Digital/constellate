const path = require('path')


// vue.config.js
module.exports = {
  // serve this for `npm run serve` in development
  // but output to the /static/ dir for django when
  // deploying the final bundle
  publicPath: process.env.NODE_ENV === 'production'
    ? '/static/'
    : '/',
  outputDir: 'static-vue',
  // becuase our front end is nested one folder down, and we compile as part of our deployment process, we need to tell webpack to point the '@' one folder in too.
  chainWebpack: config => {
    config.resolve.alias.set('@', path.resolve(__dirname, 'cl8-web/src'))
  },
  // django and whitenoise does its own hashing and cache busting
  filenameHashing: false,
  // proxy requests that are not matched by our own files
  // to the django server running at the address below
  devServer: {
    proxy: 'http://127.0.0.1:8000'
  }
}

