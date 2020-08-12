<template>
  <div id="tags">
      <input
        class="mb3 w-100"
        type="text"
        v-model="input"
        v-on:keydown.enter="newtag"
        data-tagname
        placeholder="add a new tag"/>

      <div id="tagoptions" v-if="sortedOptions">
        <button
        class="f6 grow no-underline b br-pill ph3 pv2 mb2 ml1 mr1 dib white bg-mid-gray bn pointer" 
          v-for="(option, index) in sortedOptions"
          :key="index"
          v-on:click="toggle($event, option)"
          v-bind:class="{'active bg-green': checkInList(option)}">
            {{option.name}}
        </button>
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
    list: function () {
      return this.$store.getters.profile.tags || []
    },
    options: function () {
      return this.$store.getters.fullTagList
    },
    sortedOptions: function() {
      return sortBy(this.options, function(x){
        return x.name ? x.name.toLowerCase() : x.toLowerCase()
      })
    }
  },
  data: () => {
    return {
      input: '',      
    }

  },
  methods: {
    inTagList: function(tagName) {
      if (this.list.length < 1){
        return false
      }
      const tagNames = this.list.map(x => x.name)

      return includes(tagNames, tagName)
    },
    toggle: function(event, val) {
      event.preventDefault()

      let toggleList = this.list

      if (this.inTagList(val.name)) {
        remove(toggleList, function(x) { return x.name === val.name})
      } else {
        toggleList.push(val)
      }

      this.$store.dispatch('updateProfileTags', toggleList)
    },
    newtag: function(event) {
      debug('new tag submission:', this.input)
      if (this.input.length > 0) {
        const newTagName = this.input.toLowerCase().trim()
        if (!this.inTagList(newTagName)) {
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
      return this.inTagList(option.name)
    }
  }
}
</script>
