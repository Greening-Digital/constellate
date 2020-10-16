<template>
  <div id="app" class="cf center w-100 mw8 system-sans-serif sans-serif">
    <router-view></router-view>
  </div>
</template>

<script>
import debugLib from 'debug'
import { fetchCurrentUser } from './utils'
// eslint-disable-next-line
const debug = debugLib('cl8.App')

export default {
  components: {},
  name: 'app',
  data() {
    return {}
  },
  methods: {},
  async mounted() {
    // if a user is not logged in, push to the login
    debug('mounted')
    const currentUser = await fetchCurrentUser(this.$store)

    if (!currentUser) {
      if (this.$router.currentRoute.name !== 'signin') {
        this.$router.push({ name: 'signin' })
      }
    }
  }
}
</script>

<style>
</style>
