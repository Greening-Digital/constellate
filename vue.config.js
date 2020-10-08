const path = require('path')


// vue.config.js
module.exports = {
  // serve this for `npm run serve` in development
  // but set the public path to /static/ for django when
  // deploying the final bundle
  publicPath: process.env.NODE_ENV === 'production'
    ? '/static/'
    : '/',

  // Because the vue build step clears the folder, use a different name for the
  // static folder that django uses for static files. This stops django files
  // being cleared by accident.
  outputDir: 'static-vue',

  // because our front end is nested one folder down, and we compile as part of our deployment process, we need to tell webpack to point the '@' one folder in too.
  chainWebpack: config => {
    config.resolve.alias.set('@', path.resolve(__dirname, 'frontend/src'))
  },

  // django and whitenoise does its own hashing and cache busting,
  // so we defer to that. Switch it to true if you want to rely on
  // webpack's cache busting behaviour
  filenameHashing: false,

  // proxy requests that are not matched by our own files
  // to the django server running at the address below
  devServer: {
    proxy: 'http://127.0.0.1:8000'
  },

  // pluginOptions: {
  //   i18n: {
  //     locale: 'en',
  //     fallbackLocale: 'en',
  //     localeDir: 'locales',
  //     enableInSFC: false
  //   }
  // }
}


