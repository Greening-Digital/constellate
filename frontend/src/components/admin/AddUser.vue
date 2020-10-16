<template>
  <div v-if="loading" class>
    <div class="spinner">
      <img src="../../assets/loading.svg" alt="loading" />
    </div>
  </div>
  <div v-else class="cf bg-white">
    <div class="editprofile cf bg-white">
      <nav class="pa3 ph3 ph4-ns bb b--light-gray flex items-center">
        <span class="w-100">{{ $t('message.shared.addUser') }}</span>
        <a
          href="#"
          v-on:submit.prevent="onSubmit"
          @click="onSubmit"
          class="fr v-btm f6 mr3 link br2 ph3 pv2 dib white bg-green hover-bg-green"
          >{{ $t('message.shared.save') }}</a
        >
        <router-link
          :to="{ name: 'home' }"
          class="fr v-btm f6 link br2 ph3 pv2 dib white bg-gray hover-bg-dark-gray"
          >{{ $t('message.shared.cancel') }}</router-link
        >
      </nav>
    </div>
    <div class="fl pa2">
      <div class="pa3 center w-80-l cf">
        <div>
          <form class v-if="profile">
            <div class="cf w-100" style="min-height: 11em">
              <div class="fl w-100 w-25-ns mb3">
                <v-gravatar
                  :email="profile.email"
                  :size="200"
                  class="gravatar b--light-silver ba w-80 mr4"
                />

                <div class="w-40 w-100-ns fn-ns dib v-btm mt2">
                  <div
                    class="f6 dim br2 dib w-80 white mb2"
                    v-bind:class="{
                      'bg-green': profile.visible,
                      'bg-red': !profile.visible
                    }"
                  >
                    <input
                      type="checkbox"
                      class="dib w-20 mv2 ml2"
                      id="visible-checkbox"
                      v-model="profile.visible"
                    />
                    <label for="visible-checkbox" class="dib w-70">{{
                      $t('message.shared.visible')
                    }}</label>
                  </div>
                </div>
              </div>

              <!-- Warning message box -->
              <div class="fl w-100 w-75-ns mt0 pt0">
                <div
                  v-if="warning"
                  class="flex items-center pa3 bg-light-blue mb2"
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
                  <span class="lh-title ml2">{{ warning }}</span>
                </div>

                <!-- Error message box -->
                <div
                  v-if="error"
                  class="flex items-center pa3 bg-light-red mb2"
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
                  <span class="lh-title ml2">{{ error }}</span>
                </div>

                <ul class="list mt0 pt0 f4 pa0 border-box">
                  <li class="list name">
                    <label class="f5" for>{{
                      $t('message.addUser.name')
                    }}</label>
                    <input class="w-100 mt1 pa1" v-model="profile.name" />
                  </li>

                  <li class="list email mt2">
                    <label class="f5" for>{{
                      $t('message.addUser.email')
                    }}</label>
                    <input class="w-100 mt1 pa1" v-model="profile.email" />
                  </li>
                  <li class="list phone mt2">
                    <label class="f5 mb2" for>{{
                      $t('message.addUser.phone')
                    }}</label>
                    <input class="w-100 mt1 pa1" v-model="profile.phone" />
                  </li>
                  <li class="list website mt2">
                    <label class="f5" for>
                      {{ $t('message.shared.website') }}
                      <small>{{ $t('message.addUser.websiteMessage') }}</small>
                    </label>
                    <input class="w-100 mt1 pa1" v-model="profile.website" />
                  </li>
                </ul>

                <ul class="list mt0 pt0 pa0">
                  <li class="list twitter">
                    <label class="f5" for>
                      {{ $t('message.shared.twitter') }}
                      <small></small>
                    </label>
                    <input class="w-100 mt1" v-model="profile.twitter" />
                  </li>
                  <li class="list facebook mt2">
                    <label class="f5" for>
                      {{ $t('message.shared.facebook') }}
                      <small>{{ $t('message.addUser.twitterMessage') }}</small>
                    </label>
                    <input class="w-100 mt1" v-model="profile.facebook" />
                  </li>
                  <li class="list linkedin mt2">
                    <label class="f5" for>
                      {{ $t('message.shared.linkedIn') }}
                      <small>{{ $t('message.addUser.linkedInMessage') }}</small>
                    </label>
                    <input class="w-100 mt1" v-model="profile.linkedin" />
                  </li>

                  <li class="list mt2">
                    <label class="f5" for>
                      {{ $t('message.shared.about') }}
                      <small>
                        ({{ $t('message.shared.markdownMessage') }}
                        <a href="https://daringfireball.net/projects/markdown/"
                          >markdown</a
                        >)
                      </small>
                    </label>
                    <textarea
                      class="w-100 mt1 pa1 ba b--light-gray"
                      v-model="profile.bio"
                      :placeholder="$t('message.shared.bioPlaceholder')"
                      name
                      id
                      cols="30"
                      rows="10"
                    ></textarea>
                  </li>
                </ul>
              </div>
            </div>
            <div class="cf pt2 bg-white mb3">
              <label class="typo__label">{{ $t('message.shared.tags') }}</label>
              <p class="f6 mb3">
                <em>{{ $t('message.shared.tagMessage') }}</em>
              </p>
              <profile-tags-component
                :data.sync="profile.tags"
                :options="profileTags"
                @newtag="addTag"
              ></profile-tags-component>
            </div>

            <ul class="list mt0 pt0 f4 pa0 border-box bg-washed-green pa3">
              <li class="list send-invite pt3">
                <input
                  type="checkbox"
                  id="send-invite"
                  class="mr2"
                  v-model="profile.sendInvite"
                />
                <label for="send-invite" class="f5">{{
                  $t('message.addUser.sendInvite')
                }}</label>
              </li>
              <li class="list is-admin pt3">
                <input
                  type="checkbox"
                  id="is-Admin"
                  class="mr2"
                  v-model="profile.admin"
                />
                <label for="is-Admin" class="f5">{{
                  $t('message.addUser.isAdmin')
                }}</label>
              </li>
            </ul>
          </form>
        </div>
        <div class="editprofile cf bg-white">
          <nav class="pv3 bb b--light-gray flex items-center">
            <a
              href="#"
              v-on:submit.prevent="onSubmit"
              @click="onSubmit"
              class="fr v-btm f6 mr3 link br2 ph3 pv2 dib white bg-green hover-bg-green"
              >{{ $t('message.shared.save') }}</a
            >
            <router-link
              :to="{ name: 'home' }"
              class="fr v-btm f6 link br2 ph3 pv2 dib white bg-gray hover-bg-dark-gray"
              >{{ $t('message.shared.cancel') }}</router-link
            >
          </nav>
        </div>
      </div>
    </div>

    <the-footer />
  </div>
</template>

<script>
import ProfileTagsComponent from '@/components/profile/ProfileTagsComponent.vue'
import TheFooter from '@/components/TheFooter.vue'

import { includes } from 'lodash'
import { hasPhoto } from '@/utils'
import debugLib from 'debug'

const debug = debugLib('cl8.AddUser')

export default {
  name: 'AddUser',
  components: {
    ProfileTagsComponent,
    TheFooter
  },
  data() {
    return {
      items: [],
      tagList: [],
      unsyncedTags: [],
      localPhoto: null,
      warning: null,
      error: null,
      loading: false,
      profile: {
        name: '',
        email: '',
        phone: '',
        website: '',
        twitter: '',
        facebook: '',
        linkedin: '',
        bio: '',
        visible: true,
        sendInvite: false,
        pitchable: false,
        tags: []
      }
    }
  },
  computed: {
    user() {
      return this.$store.getters.currentUser
        ? this.$store.getters.currentUser
        : false
    },
    profileTags: function () {
      let tagList = []

      if (this.items.length > 0) {
        this.items.forEach(function (peep) {
          if (typeof peep.fields !== 'undefined') {
            if (typeof peep.tags !== 'undefined') {
              peep.tags.forEach(function (t) {
                let tagListNames = tagList.map(function (tt) {
                  return tt.name
                })
                if (!includes(tagListNames, t.name)) {
                  tagList.push(t)
                }
              })
            }
          }
        })
      }
      if (this.unsyncedTags.length > 0) {
        this.unsyncedTags.forEach(function (t) {
          tagList.push(t)
        })
      }
      return tagList
    }
  },
  methods: {
    addTag(newTag) {
      let tempVal =
        newTag.substring(0, 2) + Math.floor(Math.random() * 10000000)
      const tag = {
        name: newTag,
        code: tempVal,
        id: 'tempval' + tempVal
      }
      this.profile.tags.push(tag)
      this.unsyncedTags.push(tag)
    },
    onSubmit: async function () {
      this.error = null
      this.warning = null

      if (this.profile.name.length == 0) {
        this.warning = 'Please enter a name for the new user'
        return
      }

      if (this.profile.email.length == 0) {
        this.warning = 'Please enter an email address for the new user'
        return
      }

      debug('creating profile')
      this.loading = true
      try {
        // console.log(this.profile)
        const resp = await this.$store.dispatch('addUser', this.profile)
        // Any response is a warning as `addUser` will redirect to the new
        // profile if all goes well
        // this.warning = resp
      } catch (err) {
        debug('Error creating account', err)
        this.error = err.message
      }
      this.loading = false
    },
    hasPhoto
  }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style media="screen" lang="scss" scoped>
@import '../../../../node_modules/tachyons/css/tachyons.css';
p span.list {
  display: inline-block;
}

.gravatar:hover {
  cursor: not-allowed;
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
