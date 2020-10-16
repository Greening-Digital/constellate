<template>
  <div
    class="theprofile pa3 pa4-ns center w-100 cf border-box fixed relative-l bg-white"
  >
    <div v-if="loading">
      <div class="spinner">
        <img src="../../assets/loading.svg" alt="loading" width="50px" />
      </div>
    </div>

    <div v-else>
      <transition name="fade">
        <div
          v-if="showFlashMessage"
          class="status-message cf flex items-center pa3 mb2"
          v-bind:class="messageClassObject"
        >
          <svg
            class="w1"
            data-icon="info"
            viewBox="0 0 32 32"
            style="fill: currentcolor"
          >
            <title>info icon</title>
            <path
              d="M16 0 A16 16 0 0 1 16 32 A16 16 0 0 1 16 0 M19 15 L13 15 L13 26 L19 26 z M16 6 A3 3 0 0 0 16 12 A3 3 0 0 0 16 6"
            />
          </svg>
          <span class="lh-title ml2" role="status" style="flex-grow: 1">{{
            flashMessage
          }}</span>
          <button
            aria-hidden="true"
            role="button"
            class="b--none ml2 mr2 bg-black-90 white br2 grow pointer close"
            @click="hideFlashMessage"
          >
            x
          </button>
        </div>
      </transition>
      <div v-if="profile">
        <div v-if="canEdit()" class="fn fr-l">
          <router-link
            :to="{ name: 'editProfile' }"
            role="link"
            tabindex="0"
            class="f6 link dim br2 ph3 pv2 mb3 dib white bg-gray"
            >{{ $t('message.shared.editProfile') }}</router-link
          >
        </div>

        <div v-if="isAdmin" class="fn fr-l">
          <button
            tabindex="0"
            class="resend-invite f6 link dim br2 ph3 pv2 mb3 dib white bg-gray b--none ml2 mr2"
            @click="resendInvite"
          >
            {{ $t('message.profileDetail.resendInvite') }}
          </button>
        </div>

        <div class="fl w-70 w-20-m w-20-l mr3">
          <img
            v-if="hasPhoto(profile)"
            :src="showPhoto()"
            class="supplied-photo b--light-gray ba w-100"
          />

          <v-gravatar
            v-else
            :email="profile.email"
            :size="200"
            class="gravatar b--light-gray ba w-100"
          />

          <div v-if="canEdit()">
            <div
              v-if="isVisible()"
              class="f6 link dim br2 ph3 pv2 mb2 dib white bg-green w-100 mt2 tc"
            >
              {{ $t('message.shared.visible') }}
            </div>
            <div
              v-else
              class="f6 link dim br2 ph3 pv2 mb2 dib white bg-red w-100 tc mt2"
            >
              {{ $t('message.shared.invisible') }}
            </div>
          </div>
        </div>

        <div class="fl w-100 w-60-m w-60-l mt0 pt0">
          <ul class="list mt0 pt0 pl0">
            <li class="list f3 name mt2 mt0-l mb2 name truncate">
              {{ profile.name }}
            </li>
            <li class="list f5 email truncate mb2">
              <a :href="'mailto:' + profile.email">{{ profile.email }}</a>
            </li>
            <li class="list f5 phone">{{ profile.phone }}</li>
          </ul>

          <ul class="list pl0">
            <li v-if="profile.website" class="list f5 website">
              <a :href="websiteLink" target="_blank">{{ profile.website }}</a>
            </li>
            <li v-if="profile.organisation" class="list f5 organisation mv3">
              {{ profile.organisation }}
            </li>
          </ul>

          <ul class="list pl0 social-links">
            <li v-if="this.profile.twitter" class="list f5 twitter dib mr1">
              <a :href="twitterLink" target="_blank">{{
                $t('message.shared.twitter')
              }}</a>
            </li>
            <li v-if="this.profile.facebook" class="list f5 linkedin dib mr1">
              <a :href="facebookLink" target="_blank">{{
                $t('message.shared.facebook')
              }}</a>
            </li>
            <li v-if="this.profile.linkedin" class="list f5 twitter dib mr1">
              <a :href="linkedinLink" target="_blank">{{
                $t('message.shared.linkedIn')
              }}</a>
            </li>
          </ul>
        </div>

        <div class="fl cf pt2 w-100">
          <ul class="db list tags ml0 pl0">
            <li
              v-for="tag in profile.tags"
              v-bind:key="tag.name"
              class="list bg-near-white br2 f7 pa2 mr1 mb1 ph3 b--light-silver bg-animate hover-bg-blue hover-white"
              :class="{
                'bg-dark-blue white': isActive(tag.name.toLowerCase())
              }"
              @click="toggleTag"
            >
              {{ tag.name.toLowerCase().trim() }}
            </li>
          </ul>

          <!-- TODO, make this into a tag list component -->
          <div v-if="hasActiveClusters()" class="cluster-component">
            <h4>
              {{ $t('message.profileDetail.clusterMember') }}
            </h4>
            <ul class="db list tags clusters ml0 pl0">
              <li
                v-for="cluster in profile.clusters"
                v-bind:key="cluster.name"
                class="list bg-near-white br2 f7 pa2 mr1 mb1 ph3 b--light-silver bg-animate hover-bg-blue hover-white"
                :class="{
                  'bg-dark-blue white': isActive(cluster.name.toLowerCase())
                }"
                @click="toggleCluster"
              >
                {{ cluster.name }}
              </li>
            </ul>
          </div>

          <div v-if="this.profile.bio" class="w-100 bio lh-copy measure-wide">
            <div v-html="bioOutput"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import Vue from 'vue'
import Gravatar from 'vue-gravatar'
import debugLib from 'debug'
import marked from 'marked'
import sanitizeHTML from 'sanitize-html'
const debug = debugLib('cl8.ProfileDetail')
Vue.component('v-gravatar', Gravatar)

import { linkify, hasPhoto } from '@/utils'

export default {
  name: 'ProfileDetail',
  components: {
    Gravatar
  },
  data() {
    return {
      loading: false,
      showFlashMessage: false,
      flashMessage: ''
    }
  },
  computed: {
    user() {
      return this.$store.getters.currentUser
    },
    profile() {
      return this.$store.getters.profile
    },
    activeTags() {
      return this.$store.getters.activeTags
    },
    websiteLink() {
      return this.profile.website ? linkify(this.profile.website) : null
    },
    twitterLink() {
      return this.profile.twitter
        ? linkify(this.profile.twitter, 'https://twitter.com')
        : null
    },
    facebookLink() {
      return this.profile.facebook
        ? linkify(this.profile.facebook, 'https://facebook.com')
        : null
    },
    linkedinLink() {
      return this.profile.linkedin
        ? linkify(this.profile.linkedin, 'https://linkedin.com/in')
        : null
    },
    bioOutput() {
      return this.profile.bio ? marked(sanitizeHTML(this.profile.bio)) : null
    },
    isAdmin() {
      return !!this.user.admin
    },
    messageClassObject: function () {
      return {
        'bg-light-blue': this.flashMessageClass == 'info',
        'bg-light-red': this.flashMessageClass == 'error'
      }
    }
  },
  methods: {
    canEdit: function () {
      if (this.profile && this.user) {
        debug('can edit?', this.profile.id, this.user.id)
        return this.profile.id == this.user.id
      }
      return false
    },
    toggleTag: function (ev) {
      let tag = ev.target.textContent.trim().toLowerCase()
      this.$store.dispatch('updateActiveTags', tag)
    },
    toggleCluster: function (ev) {
      const cluster = ev.target.textContent.trim().toLowerCase()
      debug('toggleCluster', { cluster })
      this.$store.dispatch('updateActiveClusters', cluster)
    },
    hasActiveClusters: function () {
      if (this.profile.clusters) {
        return !!this.profile.clusters.length
      }
    },
    hideFlashMessage: function () {
      debug('hiding message')
      this.showFlashMessage = false
      this.flashMessage = ''
    },
    isActive: function (term) {
      if (typeof this.activeTags !== 'undefined') {
        let matchesActiveTag = this.activeTags.indexOf(term) !== -1
        return matchesActiveTag
      }
    },
    isVisible: function () {
      return this.profile.visible
    },
    hasPhoto,
    showPhoto() {
      return this.profile.detail_photo
    },
    async resendInvite() {
      debug('resendInvite', this.profile)

      const response = await this.$store
        .dispatch('resendInvite', this.profile)
        .catch((err) => {
          debug({ errMessage: err.response.data.message })
          this.flashMessage = err.response.data.message
          this.flashMessageClass = 'error'
          this.showFlashMessage = true
        })
      if (response) {
        debug({ response })
        this.flashMessage = response.data.message
        this.flashMessageClass = 'info'
        this.showFlashMessage = true
      }
    }
  }
}
</script>

<style lang="scss">
ul.tags li.list {
  display: inline-block;
}
img.gravatar {
  box-shadow: 3px 3px 3px #ddd;
}

/* this only shows a border when we have two or more links in a row */
.social-links li + li {
  border-left: 1px solid #000000;
  padding-left: 1em;
}

@mixin animation(
  $name,
  $times: infinite,
  $duration: 0.5s,
  $ease: ease-out,
  $direction: forwards
) {
  @keyframes #{$name} {
    @content;
  }
  @-moz-keyframes #{$name} {
    @content;
  }
  @-webkit-keyframes #{$name} {
    @content;
  }
  -webkit-animation: $name $ease $times;
  -moz-animation: $name $ease $times;
  animation: $name $ease $times;
  -webkit-animation-fill-mode: $direction;
  -moz-animation-fill-mode: $direction;
  animation-fill-mode: $direction;
  animation-duration: $duration;
}
@mixin transform($arguments) {
  -webkit-transform: $arguments;
  -moz-transform: $arguments;
  -o-transform: $arguments;
  -ms-transform: $arguments;
  transform: $arguments;
}
.theprofile {
  top: 0;
  left: 0;
  // width:100vw;
  height: 100vh;
  overflow: auto;
  @media screen and (max-width: 960px) {
    @include animation(profilein, 1, 0.25s, ease-in-out) {
      from {
        opacity: 0;
        // @include transform(translateX(0vw));
      }
      to {
        opacity: 1;
        // @include transform(translateX(0vw));
      }
    }
  }
}
.closeProfile {
  position: absolute;
  top: 0;
  right: 0;
  width: 2rem;
  height: 2rem;
  background: #fff;
  border: 0;
  outline: none;
  background-image: url('../../assets/cross-thin.svg');
  background-size: contain;
  @media screen and (min-width: 960px) {
    display: none;
  }
}

.fade-enter {
  opacity: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease-out;
}

.fade-leave-to {
  opacity: 0;
}
</style>
