import Vue from 'vue'
import VeeValidate from 'vee-validate'

const vvConfig = {
  events: 'blur',
  class: true
}
Vue.use(VeeValidate, vvConfig)

const validationLocalizedStrings = {
  custom: {
    confirmPassword: {
      required: 'Please enter your password again.',
      confirmed: 'Passwords do not match'
    }
  }
}

export default validationLocalizedStrings
