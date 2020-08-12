<template>
  <div class="w-100">
    <div v-if="loading">
      <div class="spinner">
        <img src="../../assets/loading.svg" alt="loading" />
      </div>
    </div>

    <div v-if="!loading">
      <div class="v-mid sign-in-prompt">
        <h2 class="pt5 tc fw3 tracked">Constellation</h2>
        <div class="w-100 tc">
          <div role="status" aria-live="polite" class="vh dib">
            <!--
              when there is an error, we want list it in here, to a screen reader
              can pick it up and read out the announcement
            -->
            <div v-if="errors" class="errors">
              <p v-for="(key) in errors.all()" v-bind:key="key">{{ key }}</p>
            </div>
          </div>

          <div
            v-if="signInData.message"
            role="status"
            aria-live="polite"
            class="flex items-center justify-center pa3 bg-lightest-blue navy f6"
          >
            <svg class="w1" data-icon="info" viewBox="0 0 32 32" style="fill:currentcolor">
              <title>info icon</title>
              <path
                d="M16 0 A16 16 0 0 1 16 32 A16 16 0 0 1 16 0 M19 15 L13 15 L13 26 L19 26 z M16 6 A3 3 0 0 0 16 12 A3 3 0 0 0 16 6"
              />
            </svg>
            <span class="ml3">{{signInData.message}}</span>
          </div>

          <form v-on:submit.prevent class="w-100 pa3 dib border-box mw6 ph5">
              <p class="gray measure tl lh-copy">Enter the email address you signed up with to sign in. We'll send a one time login code, to finish logging in.</p>
              <p class="gray measure tl lh-copy">No passwords needed. </p>
            <div class="w-100 mb3">
              <input
                type="text"
                name="email"
                v-model="email"
                class="input-reset br2 pa2 ba b--light-gray mt1 w-100"
                :class=" {'bg-washed-red b--red': errors ? errors.has('email') : null}"
                placeholder="your email address"
                aria-label="your email address"
                autocomplete="email"
                @input="checkForValidFormSubmission"
                :disabled="emailSubmitted"
              />

              <div>
                <small v-if="errors && errors.has('email')" class="red">{{ errors.first('email') }}</small>
              </div>
            </div>

            <div v-if="emailSubmitted">
              <div class="w-100">
                <input
                  type="password"
                  name="login-code"
                  v-model="token"
                  class="input-reset pa2 ba br2 b--light-gray w-100"
                  :class=" {'bg-washed-red b--red': errors && errors.has('token') }"
                  placeholder="your login code"
                  aria-label="your login code"
                />

                <div>
                  <small
                    v-if="errors && errors.has('token')"
                    class="red"
                  >{{ errors.first('token') }}</small>
                </div>
              </div>
              <div class="mt2 cf">
                <button
                  class="f6 link br3 bn pv2 mb2 mt2 bg-light-silver b white w-60 ml0 mr1 fl"
                  :class="{'bg-green pointer grow hover-bg-dark-green': formValid}"
                  :disabled="!formValid"
                  name="button"
                  @click="signIn"
                >Sign in</button>
                <button
                  class="f6 link br3 bn pv2 mb2 mt2 bg-light-silver b white w-60 ml0 mr1 fl bg-red pointer grow hover-bg-dark-red"
                  name="button"
                  @click="resetForm"
                >Reset</button>
              </div>
            </div>
            <div v-else>
              <div class="mt2 cf">
                <button
                  class="f6 link br3 bn pv2 mb2 mt2 bg-light-silver b white w-60 ml0 mr1 fl"
                  :class="{'bg-green pointer grow hover-bg-dark-green': formValid}"
                  :disabled="!formValid"
                  name="button"
                  @click="submitEmail"
                >Request login code</button>
              </div>
            </div>
          </form>

          <footer>
            <p class="f6 tc gray">
              <em>Having trouble logging in? <a class="f6 tc gray" :href="supportEmail">Get in touch with support</a>.</em>
            </p>
          </footer>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import debugLib from 'debug'
const debug = debugLib('cl8.Login')

export default {
  name: 'Login',
  components: {},
  data: function() {
    return {
      email: '',
      token: null,
      announcement: '',
      formIsValid: false,
      emailSubmitted: false,
      supportEmail: `mailto:${process.env.VUE_APP_SUPPORT_EMAIL}`
    }
  },
  methods: {
    checkForValidFormSubmission: function() {
      let validation = {
        email: this.email
      }

      return this.$validator
        .validateAll(validation)
        .then(result => {
          if (!result) {
            this.formIsValid = result
            return false
          }
          this.formIsValid = result
          return result
        })
        .catch(err => {
          debug(err)
        })
    },
    resetForm: function() {
      this.email = null
      this.emailSubmitted = false
    },
    signIn: function() {
      let user = {
        email: this.email,
        token: this.token
      }
      this.$store.dispatch('login', user)
    },
    submitEmail: async function() {
      const emailSubmitted = await this.$store.dispatch(
        'submitEmail',
        this.email
      )

      if (emailSubmitted) {
        this.emailSubmitted = true
      }
    }
  },
  computed: {
    formValid: function() {
      return this.formIsValid
    },
    signInData: function() {
      return this.$store.getters.signInData
    },
    loading: function() {
      return this.$store.getters.isLoading
    }
  }
}
</script>

<style>
@import '../../../../node_modules/tachyons/css/tachyons.css';

input {
  outline-style: none;
}

.sign-in-prompt {
  margin-left: auto;
  margin-right: auto;
  background-repeat: no-repeat;
}

.sign-in-prompt a {
  top: 175px;
  left: 145px;
}

.vh {
  position: absolute !important;
  clip: rect(1px, 1px, 1px, 1px);
  padding: 0 !important;
  border: 0 !important;
  height: 1px !important;
  width: 1px !important;
  overflow: hidden;
}

.spinner {
  position: absolute;
  display: flex;
  justify-content: center;
  height: 100vh;
  width: 100vw;
  background-color: white;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
}
</style>
