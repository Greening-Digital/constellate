<template>
  <div class="cf bg-white">
    <nav-header-edit />
    <div class="fl pa2">
      <div class="pa3 center w-80-l cf">
        <div>
          <form class v-if="profile">
            <div class="cf w-100" style="min-height:11em;">
              <div class="fl w-100 w-25-ns mb3">
                <router-link :to="{ name: 'editProfilePhoto' }" class="edithover w-80 mr4">
                  <img
                    v-if="hasPhoto()"
                    :src="showPhoto()"
                    class="supplied-photo b--light-silver ba w-100 v-top fn-ns"
                  />

                  <v-gravatar
                    v-else
                    :email="profile.email"
                    :size="200"
                    class="gravatar b--light-silver ba"
                  />
                </router-link>

                <div class="w-40 w-100-ns fn-ns dib v-btm mt2">
                  <div
                    class="f6 dim br2 dib w-80 white mb2"
                    v-bind:class="{ 'bg-green': profile.visible, 'bg-red': !profile.visible }"
                  >
                    <input
                      type="checkbox"
                      class="dib w-20 mv2 ml2"
                      id="visible-checkbox"
                      v-model="profile.visible"
                    />
                    <label 
                    v-if="profile.visible"
                    for="visible-checkbox"
                    class="dib w-70">
                      Visible
                    </label>
                    <label 
                    v-else
                    for="visible-checkbox"
                    class="dib w-70">
                      Hidden
                    </label>
                  </div>
<p 
class="f6 lh-copy i gray ph2"
v-if="profile.visible"
>Your profile is visible to other members</p>
<p 
class="f6 lh-copy i gray ph2"
v-else
>Your profile is hidden from other members</p>

                </div>
              </div>

              <div class="fl w-100 w-75-ns mt0 pt0">
                <ul class="list mt0 pt0 f4 pa0 border-box">
                  <li class="list name">
                    <label class="f5" for>Name <span class="f6 lh-copy i gray">(use your full name to make you easier to find)</span></label>

                    <input class="w-100 mt1 pa1" v-model="profile.name" />
                  </li>

                  <li class="list email mt2">
                    <label class="f5" for>
                      Email
                      <span class="f6 lh-copy i gray">(You are unable to change your email address.)</span>
                      </label>
                    <div  class="w-100 mt1 bg-near-white pa2">
                      {{ profile.email }}
                    </div>
                  </li>
                  <li class="list phone mt2">
                    <label class="f5 mb2" for>Phone</label>
                    <span class="f6 lh-copy i gray"> (include the country code i.e. +44 78945 123 456) </span>
                    <input class="w-100 mt1 pa1" v-model="profile.phone" />
                  </li>
                  <li class="list website mt2">
                    <label class="f5" for>
                      Website

                    </label>
                    <input class="w-100 mt1 pa1" v-model="profile.website" />
                  </li>
                  <li class="list organisation mt2">
                    <label class="f5" for>
                      Organisation

                    </label>
                    <input class="w-100 mt1 pa1" v-model="profile.organisation" />
                  </li>
                </ul>

                <ul class="list mt0 pt0 pa0">
                  <li class="list twitter">
                    <label class="f5" for>
                      Twitter
                    </label>
                    <input class="w-100 mt1" v-model="profile.twitter" />
                  </li>
                  <li class="list facebook mt2">
                    <label class="f5" for>
                      Facebook
                    </label>
                    <input class="w-100 mt1" v-model="profile.facebook" />
                  </li>
                  <li class="list linkedin mt2">
                    <label class="f5" for>
                      LinkedIn
                      <span class="f6 lh-copy i gray">(it normally looks like http://www.linked.com/in/some-name-or-id)</span>
                    </label>
                    <input class="w-100 mt1" v-model="profile.linkedin" />
                  </li>

                  <li class="list mt2">
                    <label class="f5" for>
                      About
                      <span class="f6 lh-copy i gray">
                        (Using
                        <a href="https://daringfireball.net/projects/markdown/">markdown</a> for formatting is supported)
                      </span>
                    </label>
                    <textarea
                      class="w-100 mt1 pa1 ba b--light-gray"
                      v-model="profile.bio"
                      placeholder="Summary of interests and expertise relevant to Icebreaker One"
                      name
                      id
                      cols="30"
                      rows="10"
                    ></textarea>
                  </li>
                </ul>
              </div>

              <div class="cf pt2 bg-white mb4 mb5">
                <label class="typo__label">Skills and Interests</label>
                <p class="f6 mb3">
                  <span class="f6 lh-copy i gray">(type below to add new tags)</span>
                </p>
                <profile-tags-component
                ></profile-tags-component>
              </div>
            </div>

          </form>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
/* eslint-disable */
import NavHeaderEdit from '../shared/NavHeaderEdit.vue'
import ProfileTagsComponent from '@/components/profile/ProfileTagsComponent.vue'
import { includes } from 'lodash'
import debugLib from 'debug'

const debug = debugLib('cl8.ProfileEdit')

export default {
  name: 'ProfileEdit',
  components: {
    NavHeaderEdit,
    ProfileTagsComponent
  },

  data() {
    return {
      localPhoto: null
    }
  },
  computed: {
    user() {
      return this.$store.getters.currentUser
        ? this.$store.getters.currentUser
        : false
    },
    profile() {
      return this.$store.getters.profile
    },
    profileTags: function() {
      return this.profile.tags
    },
    fullTagList: function() {
      return this.$store.getters.tagList
    }
  },
  async created() {
    debug('fetching latest profiles and tags')
    await this.$store.dispatch('fetchVisibleProfileList')
  },
  methods: {
    updatePhoto(ev) {
      debug('image added')
      // assign the photo
      debug(ev.target.files)
      if (ev.target.files.length === 1) {
        let newPhoto = ev.target.files[0]
        this.localPhoto = window.URL.createObjectURL(newPhoto)
        let payload = { profile: this.profile, photo: newPhoto }
        this.$store.dispatch('updateProfilePhoto', payload)
      }
    },
    hasPhoto() {
      if (this.profile.photo) {
        return true
      }
      return false
    },
    showPhoto(size) {
      return this.profile.photo
    },
    setUserProfile() {
      debug('setting own profile for ', this.user)
      let user = this.user
      let matchingProfiles = this.items.filter(function(peep) {
        return peep.id === user.uid
      })
      if (matchingProfiles.length > 0) {
        debug('We have a match!', matchingProfiles[0])
        this.$store.commit('SET_PROFILE', matchingProfiles[0])
      } else {
        debug('No matches', matchingProfiles)
      }
    }
  }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style media="screen" lang="scss" scoped>
@import '../../../../node_modules/tachyons/css/tachyons.css';
p span.list {
  display: inline-block;
}

@mixin rounded($r: 5px) {
  -webkit-border-radius: $r;
  -moz-border-radius: $r;
  border-radius: $r;
}

@mixin padding() {
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
}

/deep/ input,
textarea {
  box-sizing: border-box;
  background: #fafafa;
  border: 1px solid rgba(#000, 0.1);
  @include rounded(3px);
  padding: 0.25em 0.5em;
  font-size: 1.25rem;
}
/deep/ textarea {
  font-size: 1rem;
}
li.email div {
  cursor:not-allowed
}

.edithover {
  position: relative;
  display: inline-block;
  width: auto;
  color: #fff;
  text-align: center;
  &:before {
    content: 'change';
    position: absolute;
    top: 0;
    left: 0;
    width: 101%;
    height: 100%;
    background-color: rgba(#09f, 0.3);
    pointer-events: none;
    opacity: 0;
    padding: 1em;
    @include padding();
    transition: all 0.2s;
  }
  &:hover {
    &:before {
      opacity: 1;
    }
  }
}
</style>
