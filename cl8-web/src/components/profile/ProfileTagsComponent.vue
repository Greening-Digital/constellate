<template>
  <div id="tags">
      <input
        type="text"
        v-model="input"
        v-on:keydown.enter="newtag"
        data-tagname
        placeholder="add a new tag"/>

      <div id="tagoptions" v-if="sortedOptions">
        <button
          v-for="(option, index) in sortedOptions"
          :key="index"
          v-on:click="toggle($event, option)"
          v-bind:class="{active: checkInList(option)}">
            {{option.name}}
        </button>
      </div>

  </div>
</template>
<script>
import { sortBy, includes } from 'lodash'
import debugLib from 'debug'

const debug = debugLib('cl8.ProfileTagsComponent')
// TODO
export default {
  name: 'ProfileTagsComponent',
  props: ['data'],
  created () {
    if (this.list === undefined ) this.list = []
  },
  computed: {
    list: function () {
      return this.$store.getters.profile.tags
      // return this.data || []
    },
    options: function () {
      // debug(this.$store.getters.fullTagList
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
      if (!this.list.length){
        return false
      }
      return includes(this.list.map(x => x.name), tagName)
    },
    toggle: function(event, val) {
      event.preventDefault()

      if (this.list !== undefined) {
        if (!this.inTagList(val.name)) {
          this.list.push(val)
        } else {
          this.list.splice(this.list.findIndex(x => x.name === val.name), 1)
        }
      } else {
        this.list = [val]
      }
      // TODO use the store instead here
      this.$emit('update:data', this.list)
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
      const that = this
      if (this.list !== undefined) {
        // debug({option})
        // debug(JSON.parse(JSON.stringify(option)))
        // debug(that.options)
        return that.inTagList(option.name)
      } else {
        return false
      }

    }
  }
}
</script>
<style scoped lang="scss">
@mixin rounded($r: 5px) {
  -webkit-border-radius: $r;
  -moz-border-radius: $r;
  border-radius: $r;
}
@mixin select() {
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
input {
  margin-bottom: 1em;
  width: 100%;
}
#tags {
  $tagbgcolor: #333 !default;
  $tagbgcolorhover: #111 !default;
  $tagtextcolor: #fff !default;
  $deletecolor: #f00 !default;
  $activecolor: green !default;
  button {
    display: inline-block;
    margin: 0 0.5em 0.5em 0;
    background: $tagbgcolor;
    padding: 0.25em 0.5em;
    @include rounded(3px);
    color: $tagtextcolor;
    border: 0;
    cursor: pointer;
    outline: none;
    font-size: 1em;
    @include select();
    &:hover {
      background: $tagbgcolorhover;
      &.tag {
        background: $deletecolor;
      }
    }
    &.notag {
      pointer-events: none;
      font-style: italic;
      opacity: 0.15;
    }
  }

  #tagoptions {
    button {
      opacity: 0.5;
      &.active {
        background: $activecolor !important;
        &:hover {
          background: $deletecolor;
        }
      }
      &:hover {
        opacity: 1;
      }
    }
  }
}
</style>
