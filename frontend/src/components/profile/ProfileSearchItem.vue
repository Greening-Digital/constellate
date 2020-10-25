<template>
  <li
    :data-atid="item.id"
    class="list peep cf pa3 bb b--light-gray mid-gray hover-bg-white"
    @click="profileChosen"
  >
    <div class="dib w-20 mw4">
      <img v-if="hasPhoto(item)" :src="showPhoto('thumbnail')" class="supplied-photo w-100" />

      <v-gravatar v-else :email="item.email" :size="64" class="gravatar fl b--light-silver ba" />
    </div>
    <div class="dib w-70 ph2 flex-auto v-top h3 h-auto-m overflow-hidden">
      <ul class="list pt1 mt0 ml0 pl0 pb1 f4-m">
        <li class="name mid-gray">{{ item.name }}</li>
        <li v-if="item.organisation" class="organisation black-40 f6 mt1">{{ item.organisation }}</li>
      </ul>

      <div class="dib mt1-m">
        <div class="dib mr2 black-30 f7 f6-m" v-for="tag in item.tags" :key="tag.id">{{tag.name}}</div>
      </div>
    </div>
  </li>
</template>

<script>
import Vue from 'vue'
import { hasPhoto } from '@/utils'
import Gravatar from 'vue-gravatar'
import debugLib from 'debug'
const debug = debugLib('cl8.ProfileSearchItem')
Vue.component('v-gravatar', Gravatar)

export default {
  props: {
    item: {
      type: Object,
      default: function () {
        return {
          name: 'default',
          photo: null
        }
      }
    }
  },
  data() {
    return {}
  },
  computed: {},
  methods: {
    profileChosen() {
      debug(this.item)
      this.$store.dispatch('fetchProfile', this.item)
    },
    hasPhoto,
    showPhoto(size) {
      if (size == 'thumbnail') {
        return this.item.thumbnail_photo
      } else {
        return this.item.photo
      }
    }
  }
}
</script>

<style>
li.peep {
  cursor: pointer;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
</style>
