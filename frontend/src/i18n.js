import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)
const messages = require('./locales/en.json')

const i18n = new VueI18n({
  messages, // set locale messages
})


export default i18n
