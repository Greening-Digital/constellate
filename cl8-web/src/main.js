// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
/* eslint-disable */
import Vue from 'vue'
import Vuex from 'vuex'
import App from './App'

import router from './routes'
import store from './store'

import VeeValidate from 'vee-validate'
import VueFuse from 'vue-fuse'

import debugLib from 'debug'
const debug = debugLib('cl8.main.js')

Vue.config.productionTip = false
Vue.config.devtools = true

const vvConfig = {
  events: 'blur',
  class: true
}

const dict = {
  custom: {
    confirmPassword: {
      required: 'Please enter your password again.',
      confirmed: 'Passwords do not match'
    }
  }
}

Vue.use(Vuex)
Vue.use(VeeValidate, vvConfig)
Vue.use(VueFuse)

const VueStore = new Vuex.Store(store)

const app = new Vue({
  router,
  store: VueStore,
  render: h => h(App)
}).$mount('#app')

app.$validator.localize('en', dict)

// check for our user on load of the app
;(async () => {
  const currentUser = VueStore.getters.currentUser

  if (!currentUser) {
    await VueStore.dispatch('createUserSession')
  }
})()

router.beforeEach(async (to, from, next) => {
  debug(to.name, to.from, next)
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const currentUser = VueStore.getters.currentUser

  if (currentUser && to.name === 'signin') {
    next('home')
  }

  if (requiresAuth && !currentUser) {
    // you need to be logged in, so log the user in
    next('signin')
  } else {
    next()
  }
})
