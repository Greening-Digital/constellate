<template>
  <div id="tags">
    <input
      class="mb3 w-100"
      type="text"
      v-model="input"
      v-on:keydown.enter="newtag"
      data-tagname
      placeholder="add a new tag"
    />

    <div id="tagoptions" v-if="sortedTagList">
      <button
        class="f6 grow no-underline b br-pill ph3 pv2 mb2 ml1 mr1 dib white bg-mid-gray bn pointer"
        v-for="(option, index) in sortedTagList"
        :key="index"
        :data-tagname="option.name"
        @click.stop.prevent="toggle(option)"
        v-bind:class="{'active bg-dark-green': inProfileTags(option.name)}"
      >{{option.name}}</button>
    </div>
  </div>
</template>
<script>
import { sortBy, includes, remove } from 'lodash'
import debugLib from 'debug'

const debug = debugLib('cl8.ProfileTagsComponent')

export default {
  name: 'ProfileTagsComponent',
  computed: {
    profileTags: function () {
      return this.$store.getters.profile.tags || []
    },
    originalTagList: function () {
      return this.$store.getters.fullTagList
    },
    sortedTagList: function() {
      const tags = this.originalTagList

      return sortBy(tags, function(x){
        return x.name ? x.name.toLowerCase() : x.toLowerCase()
      })
      return tags
    }
  },
  data: () => {
    return {
      input: ''
    }

  },
  methods: {
    inProfileTags: function(tagName) {
      if (this.profileTags.length < 1){
        return false
      }
      const tagNames = this.profileTags.map(x => x.name)
      // debug({tagNames})
      // debug({tagName})
      // debug({inlist: includes(tagNames, tagName)})
      return includes(tagNames, tagName)
    },
    toggle: function(tag) {
      debug('toggle', tag)

      let toggleList = this.sortedTagList.slice()
      let profileTags = this.profileTags.slice()

      if (this.inProfileTags(tag.name)) {
        console.log(`checking ${tag.name}`)
        console.log(`found ${tag.name} in ${toggleList.map(x => x.name)}`)
        remove(profileTags, function(x) { return x.name === tag.name})
      } else {
        console.log(`didn't find ${tag.name} in ${profileTags}`)
        profileTags.push(tag)
      }
      // TODO: this is triggered for the first element whenever we load the element. Why?
      debug('profileTags', this.profileTags.map(x => x.name))
      debug('toggleList', toggleList.map(x => x.name))
      this.$store.commit('SET_PROFILE_TAGS', profileTags)

    },
    newtag: function(event) {
      event.stopPropagation()
      event.preventDefault()
      debug('newtag:', this.input)
      if (this.input.length > 0) {
        const newTagName = this.input.toLowerCase().trim()
        if (!this.inProfileTags(newTagName)) {
          debug('new tag, adding to the list:', newTagName)
          this.$store.dispatch('newProfileTag', newTagName)
        } else {
          debug('this tag already exists. Doing nothing for:', newTagName)
        }
      }
      // then reset input
      this.input = ''
    },
    checkInList: function(option){
      debug('checkInList', option)
      return this.inTagList(option.name)
    }
  }
}
</script>
