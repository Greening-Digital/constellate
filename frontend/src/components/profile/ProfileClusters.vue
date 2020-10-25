<template>
  <div id="clusters">
    <div id="cluster-options" v-if="sortedTagObjectList">
      <button
        class="f6 grow no-underline b br-pill ph3 pv2 mb2 ml1 mr1 dib white bg-mid-gray bn pointer"
        v-for="(option, index) in sortedTagObjectList"
        :key="index"
        :data-tagname="option.name"
        @click.stop.prevent="toggle(option)"
        v-bind:class="{'active bg-dark-green': inProfileClusters(option.name)}"
      >{{option.name}}</button>
    </div>
  </div>
</template>
<script>
import { sortBy, includes, remove } from 'lodash'
import debugLib from 'debug'

const debug = debugLib('cl8.ProfileClusters')

export default {
  name: 'ProfileClustersComponent',
  computed: {
    profileClusters: function () {
      return this.$store.getters.profile.clusters || []
    },
    originalClusterList: function () {
      return this.$store.getters.fullClusterList
    },
    sortedTagObjectList: function () {
      const clusters = this.originalClusterList

      return sortBy(clusters, function (x) {
        return x.name ? x.name.toLowerCase() : x.toLowerCase()
      })
      return clusters
    }
  },
  data: () => {
    return {
      input: ''
    }
  },
  methods: {
    inProfileClusters: function (clusterName) {
      if (this.profileClusters.length < 1) {
        return false
      }
      const clusterNames = this.profileClusters.map((x) => x.name)
      return includes(clusterNames, clusterName)
    },
    toggle: function (cluster) {
      debug('toggle', cluster)
      debug('this.profileClusters', this.profileClusters)
      let profileClusters = this.profileClusters.slice()

      if (this.inProfileClusters(cluster.name)) {
        remove(profileClusters, function (x) {
          return x.name === cluster.name
        })
      } else {
        profileClusters.push(cluster)
      }
      debug(
        'profileCLusters',
        this.profileClusters.map((x) => x.name)
      )
      this.$store.commit('SET_PROFILE_CLUSTERS', profileClusters)
    },
    checkInList: function (option) {
      debug('checkInList', option)
      return this.inClusterList(option.name)
    }
  }
}
</script>
