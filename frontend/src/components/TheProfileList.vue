<template>
  <div>
    <div v-if="loading">
      <div class="spinner">
        <img src="../assets/loading.svg" alt="loading" />
      </div>
    </div>

    <div v-else>
      <div class="tag-list pa2 bb b--light-gray" v-if="activeTags">
        <p>
          <button
            v-for="tag in activeTags"
            :key="tag"
            class="remove-tag list pt2 pb2 mr1 mb1 ph3 pr5 br2 bn f7 white bg-dark-blue relative bg-animate hover-bg-red"
            @click.stop.prevent="toggleTag"
          >
            {{ tag }}
          </button>
        </p>
      </div>

      <div class="tag-list pa2 bb b--light-gray" v-if="activeClusters">
        <p>
          <button
            v-for="cluster in activeClusters"
            :key="cluster"
            :data-name="cluster"
            class="remove-cluster list pt2 pb2 mr1 mb1 ph3 pr5 br2 bn f7 white bg-dark-blue relative bg-animate hover-bg-red"
            @click.stop.prevent="toggleCluster"
          >
            {{ cluster }}
          </button>
        </p>
      </div>

      <ul class="list ma0 ml0 pl0 pa0">
        <profile-search-item
          v-for="item in searchResults"
          :item="item"
          :key="item.id"
        />
      </ul>
    </div>
  </div>
</template>

<script>
import { includes } from 'lodash'

import ProfileSearchItem from '@/components/profile/ProfileSearchItem.vue'
import debugLib from 'debug'
const debug = debugLib('cl8.TheProfileList')

const searchKeys = ['name', 'email', 'tags.name']
const searchOptions = {
  keys: searchKeys,
  defaultAll: true,
  threshold: 0.2
}

export default {
  name: 'TheProfileList',
  components: {
    ProfileSearchItem
  },
  data() {
    return {
      loading: true,
      searchResults: []
    }
  },
  computed: {
    term() {
      return this.$store.getters.currentTerm
    },
    activeTags() {
      return this.$store.getters.activeTags
    },
    activeClusters() {
      return this.$store.getters.activeClusters
    },
    profileList() {
      return this.$store.getters.profileList
    }
  },
  watch: {
    term() {
      this.checkAgainstSearch()
    },
    activeTags() {
      this.checkAgainstSearch()
    },
    activeClusters() {
      this.checkAgainstSearch()
    }
  },
  async created() {
    debug('created')
    this.$store.commit('startLoading')

    // make a new promise to fetch this stuff, then after they have loaded show the stuff
    try {
      await this.$store.dispatch('fetchProfileList')
      debug('loaded the profiles in the component')
      this.searchResults = this.profileList
      this.$store.commit('stopLoading')
      this.loading = false
    } catch (e) {
      debug("couldn't load in the profile: ", e)
    }
  },

  methods: {
    checkAgainstSearch() {
      debug('checkAgainstSearch: filtering against matching tags:', this.term)
      let searchResults = this.matchingTags()
      this.searchResults = this.matchingClusters(searchResults)

      debug('this.searchResults', this.searchResults.length)

      // if we have a term to search against too, after ouer tags
      if (this.term !== '') {
        debug('checkAgainstSearch: searching against term:', this.term)
        this.$search(this.term, this.searchResults, searchOptions).then(
          (results) => {
            debug('checkAgainstSearch: results', results.length)
            this.searchResults = results
          }
        )
      }
    },
    toggleTag: function (ev) {
      const tag = ev.target.textContent.trim()
      debug('toggleTag', { tag })
      this.$store.dispatch('updateActiveTags', tag)
    },
    toggleCluster: function (ev) {
      const cluster = ev.target.textContent.trim()
      debug('toggleCluster', { cluster })
      this.$store.dispatch('updateActiveClusters', cluster)
    },
    matchingTags() {
      const activeTags = this.activeTags
      const activeClusters = this.activeClusters
      debug('matchingTags', { activeTags }, { activeClusters })

      const noActiveTags =
        typeof activeTags === 'undefined' || activeTags === ''
      const noActiveClusters =
        typeof activeClusters === 'undefined' || activeClusters === ''

      if (noActiveTags && noActiveClusters) {
        debug('returning early. no clusters or tags to filter by')
        return this.profileList
      }

      const availableProfiles = this.profileList
      let profilesFilteredByTags

      debug('availableProfiles', { availableProfiles })
      // clear out profiles with NO tags
      if (!noActiveTags) {
        // now reduce the list till we only have people matching all tags
        activeTags.forEach(function (activeTag) {
          profilesFilteredByTags = availableProfiles.filter(function (profile) {
            const profileTags = profile.tags.map(function (tag) {
              return tag.name.toLowerCase()
            })
            debug('comparing', { profileTags }, { activeTag })
            return includes(profileTags, activeTag)
          })
        })
      }
      debug('profilesFilteredByTags', { profilesFilteredByTags })
      let profilesFilteredByClusters =
        profilesFilteredByTags || availableProfiles
      if (!noActiveClusters) {
        debug('checking against matchingClusters', activeClusters)
        activeClusters.forEach(function (clusterName) {
          profilesFilteredByClusters = profilesFilteredByClusters.filter(
            function (profile) {
              const profileClusters = profile.clusters.map(function (cluster) {
                return cluster.name.toLowerCase()
              })
              debug('comparing', { profileClusters }, { clusterName })
              return includes(profileClusters, clusterName)
            }
          )
        })
      }
      debug('profilesFilteredByClusters', { profilesFilteredByClusters })
      return profilesFilteredByClusters
    }
  }
}
</script>


<style>
.side-column,
.profile-holder {
  height: auto;
  overflow: visible;
  @media (min-width: 960px) {
    overflow: auto;
    height: calc(100vh - 4.25rem - 1px);
  }
}
p span.list {
  display: inline-block;
}
.tag-list span {
  cursor: pointer;
}
.tag-list span i.remove_icon:after {
  content: '\D7';
  color: white;
}
.tag-list span i.remove_icon {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 1em;
  font-style: normal;
}
.bg-network {
  /* background-image: url(../../assets/network-watermark.png); */
  background-repeat: no-repeat;
}
.profile-holder {
  /* box-shadow: 5px 0px 20px #ddd; */
}
hr {
  border: 0;
  border-top: 1px solid #ddd;
}
button.remove-tag {
  background-image: url(../assets/cross-mark.svg);
  background-size: 0.75em;
  background-repeat: no-repeat;
  background-position: top 0.5em right 0.5em;
  padding-right: 2em;
}
input {
  outline-style: none;
}
.navnav {
  top: 0;
}
.mainframe {
  @media screen and (max-width: 960px) {
    margin-top: calc(4.25rem + 1px);
  }
  @media screen and (max-width: 480px) {
    margin-top: calc(6.25rem + 1px);
  }
}
</style>
