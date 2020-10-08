<template>
  <nav class="dt w-100 border-box pa3 bb b--light-gray bg-white">
    <div class="v-mid flex-ns items-stretch tr-s">
      <div class="w-100 order-0">
        <input
          :placeholder="$t('message.navHeaderLoggedIn.search')"
          class="input-reset ba br2 b--light-gray pa2 mr1 w-100 border-box"
          name="search-term"
          @input="updateSearchTerm"
        />
      </div>
      <router-link
        v-if="canAddUsers"
        :to="{ name: 'addUser' }"
        role="link"
        tabindex="0"
        class="link dark-gray f6 nowrap f6-ns dib fr fn-ns pointer pt0 pb3 pa2-m pa2-l ph3 v-mid order-1 tr"
      >{{ $t('message.shared.addUser') }}</router-link>
      <span
        :title="$t('message.navHeaderLoggedIn.myProfile')"
        role="link"
        tabindex="0"
        class="link dark-gray f6 nowrap f6-ns dib fr fn-ns pointer pt0 pb3 pa2-m pa2-l ph3 v-mid order-1 tr"
        @click="myProfile"
      >{{ $t('message.navHeaderLoggedIn.myProfile') }}</span>
      <span
        :title="$t('message.navHeaderLoggedIn.logOut')"
        role="link"
        tabindex="0"
        class="link dark-gray f6 nowrap f6-ns dib fr fn-ns pointer pt0 pb3 pa2-m pa2-l ph3 v-mid order-1 tr"
        @click="logout"
      >{{ $t('message.navHeaderLoggedIn.logOut') }}</span>
    </div>
  </nav>
</template>

<script>
import debugLib from 'debug'
const debug = debugLib('cl8.NavHeaderLoggedIn.vue')
export default {
  name: 'Header',
  computed: {
    canAddUsers() {
      return this.$store.getters.isAdmin
    }
  },
  methods: {
    updateSearchTerm(ev) {
      let term = ev.target.value.trim()
      this.$store.commit('setTerm', term)
    },
    logout: function() {
      debug('log out')
      this.$store.dispatch('logout')
    },
    myProfile: function() {
      debug('setting profile back to user')
      debug('currentUser', this.$store.getters.currentUser)
      this.$store.dispatch('fetchProfile', this.$store.getters.currentUser)
    }
  }
}
</script>
<style lang="scss">
.dtc span {
  cursor: pointer;
}
// TODO check the a11y implications of this style - I think it screws screen readers
input {
  outline-style: none;
}
</style>
