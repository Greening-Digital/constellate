/* eslint-disable */
import router from './routes'
import fbase from './fbase'
import axios from 'axios'

const debug = require('debug')('cl8.store')

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
  timeout: 60000
})

const state = {
  user: null,
  loading: false,
  searchTerm: '',
  searchTags: [],
  profile: null,
  profilePhoto: null,
  profileShowing: false,
  profileList: [],
  visibleProfileList: [],
  requestUrl: null,
  signInData: {
    message: null,
    email: null
  },
  token: null
}

const getters = {
  currentUser: function(state) {
    return state.user
  },
  isLoading: function(state) {
    return state.loading
  },
  isAdmin: function(state) {
    if (state.user == null) return false
    if (state.visibleProfileList == null) return false

    // Legacy profiles from Airtable have 'yes' in the admin field
    const truthy = ['yes', true]
    return state.visibleProfileList
      .filter(profile => truthy.includes(profile.admin))
      .map(profile => profile.id)
      .includes(state.user.id)
  },
  currentTerm: function(state) {
    return state.searchTerm
  },
  activeTags: function(state) {
    debug('activeTags', state.searchTags)
    return state.searchTags
  },
  profile: function(state) {
    return state.profile
  },
  //
  profilePhoto: function(state) {
    return state.profilePhoto
  },
  profileList: function(state) {
    debug('getting profileList')
    return state.profileList
  },
  profileShowing: function(state) {
    return state.profileShowing
  },
  visibleProfileList: function(state) {
    debug('getting visibleProfileList')
    return state.visibleProfileList
  },
  requestUrl: function(state) {
    return state.requestUrl
  },
  signInData: function(state) {
    return state.signInData
  },
  token: function(state) {
    return localStorage.token
  }
}

const mutations = {
  CLEAR_USER: function(state) {
    state.profile = null
    state.user = null
    state.token = null
    localStorage.token = null
  },
  stopLoading: function(state) {
    state.loading = false
  },
  startLoading: function(state) {
    state.loading = true
  },
  setTerm: function(state, payload) {
    debug('setTerm', payload)
    debug('setTerm', typeof payload)
    state.searchTerm = payload
  },
  setTags: function(state, payload) {
    debug('setTags', payload)
    state.searchTags = payload
  },
  SET_AUTH_TOKEN: function(state, payload) {
    debug('SET_AUTH_TOKEN', payload)
    state.token = payload
    localStorage.token = payload
  },
  SET_PROFILE: function(state, payload) {
    debug('SET_PROFILE', payload)
    state.profileShowing = true
    state.profile = payload
  },
  setProfilePhoto: function(state, payload) {
    debug('setProfilePhoto', payload)
    state.profile.photo = [payload]
  },
  setProfileList: function(state, payload) {
    debug('setProfileList', payload)
    state.profileList = payload
  },
  setVisibleProfileList: function(state, payload) {
    debug('setVisibleProfileList', payload)
    state.visibleProfileList = payload
  },
  toggleProfileShowing: function(state) {
    debug('profileShowing', state.profileShowing)
    state.profileShowing = !state.profileShowing
  },
  setRequestUrl: function(state, payload) {
    debug('setrequestUrl', payload)
    state.requestUrl = payload
  },
  SET_USER: function(state, payload) {
    debug('SET_USER', payload)
    state.user = payload
  }
}

const actions = {
  // otherwise log user in here
  submitEmail: async function(context, payload) {
    const emailPayload = {
      email: payload
    }
    const emailsubmitted = await instance.post('/auth/email/', emailPayload)

    if (emailsubmitted) {
      return true
    } else {
      return false
    }
  },
  login: async function(context, payload) {
    try {
      const response = await instance.post('/auth/token/', payload)
      const token = response.data.token

      context.commit('SET_AUTH_TOKEN', token)
      await context.dispatch('createUserSession')

      if (context.getters.requestUrl) {
        debug('pushing to original req url: ', context.getters.requestUrl)
        router.push(context.getters.requestUrl)
      } else {
        debug('pushing to home')
        router.push({ name: 'home' })
      }
    } catch (error) {
      debug('Error logging in', error)
    }
  },
  logout: function(context) {
    context.commit('CLEAR_USER')
    router.push('signin')
  },
  createUserSession: async function(context, payload) {
    const token = context.getters.token

    const profileResponse = await instance.get('api/profiles/me', {
      headers: { Authorization: `Token ${token}` }
    })
    context.commit('SET_USER', profileResponse.data)
    context.commit('SET_PROFILE', profileResponse.data)
  },
  resetPassword: function(context, payload) {
    debug('send password reset for ', payload)
    fbase
      .auth()
      .sendPasswordResetEmail(payload)
      .then(function() {
        // Email sent.
        debug('password reset requested', payload)
      })
      .catch(function(error) {
        // An error happened.
        debug('Problem sending password: ', error)
      })
  },
  newPassword: function(context, payload) {
    console.log(payload)
    context.state.loading = true
    fbase
      .auth()
      .verifyPasswordResetCode(payload.code)
      .then(email => {
        fbase
          .auth()
          .confirmPasswordReset(payload.code, payload.password)
          .then(function(resp) {
            // TODO: Then do something with the response.
            context.state.signInData.message =
              'Password changed. Please sign in with new password'
            context.state.signInData.email = email
            router.push('signin')
            context.state.loading = false
          })
      })
      .catch(error => {
        console.error(error.code)
        console.error(error.message)
        context.state.loading = false
      })
    debug(context, payload)
  },
  updateActiveTags: function(context, payload) {
    debug('updateActiveTags', payload)
    let tag = payload
    let tags = context.state.searchTags
    debug('tags', tags)
    if (tags.indexOf(tag) !== -1) {
      let index = tags.indexOf(tag)
      tags.splice(index, 1)
    } else {
      tags.push(tag)
    }
    context.commit('setTags', tags)
  },
  fetchProfileList: async function(context) {
    try {
      const response = await instance.get('/api/profiles', {
        headers: { Authorization: `Token ${localStorage.token}` }
      })

      const profileArray = response.data
      context.commit('setProfileList', profileArray)
    } catch (error) {
      debug('Error fetching profileList', error)
    }
  },
  fetchVisibleProfileList: async function(context) {
    debug('fetching visible profiles')
    try {
      const response = await instance.get('/api/profiles', {
        headers: { Authorization: `Token ${localStorage.token}` }
      })
      const profileArray = response.data.filter(profile => profile.visible)
      context.commit('setVisibleProfileList', profileArray)
    } catch (error) {
      debug('Error fetching visibleProfileList', error)
    }
  },
  /**
   * Create a new Firebase user account and constellate user profile
   *
   * @param {*} context
   * @param {*} payload dictionary with new user data as follows
   *
   * Fields (as string if not noted otherwise):
   * - name
   * - email
   * - phone
   * - website (without protocol)
   * - twitter
   * - facebook
   * - linkedin
   * - bio (summary)
   * - visible (boolean)
   * - pitchable (boolean)
   */
  addUser: async function(context, payload) {
    payload.tags = payload.tags.map(function(obj) {
      return obj.name
    })
    const token = context.getters.token

    const response = await instance.post('/api/profiles/', payload, {
      headers: { Authorization: `Token ${token}` }
    })
    if (response.data) {
      context.dispatch('fetchVisibleProfileList')
      context.commit('SET_PROFILE', response.data)
      router.push({ name: 'home' })
    } else {
      return 'There was a problem creating the account'
    }
  },
  fetchProfile: async function(context, payload) {
    debug('fetching profile for:', payload)
    const profile = await instance.get(`/api/profiles/${payload.id}`, {
      headers: { Authorization: `Token ${localStorage.token}` }
    })
    context.commit('SET_PROFILE', profile.data)
  },
  updateProfile: async function(context, payload) {
    debug('sending update to API', payload)

    // doing this round trip returns a JSON object we
    // can save back to the realtime database more easily,
    // and strips out properties we wouldn't want to save into it
    payload.tags = payload.tags.map(function(obj) {
      return obj.name
    })
    const token = context.getters.token
    const profileId = payload.id

    const profile = await instance.put(`/api/profiles/${profileId}/`, payload, {
      headers: { Authorization: `Token ${token}` }
    })

    if (profile) {
      context.commit('SET_PROFILE', profile.data)
      context.dispatch('fetchVisibleProfileList')
      router.push({ name: 'home' })
    } else {
      return 'There was a problem saving changes to the profile.'
    }

    // if (!pushKey) {
    //   throw new Error(
    //     'this profile has no push key. this is needed for writing data'
    //   )
    // }

    // return fbase
    //   .database()
    //   .ref('userlist')
    //   .child(pushKey)
    //   .set(newProfile)
    //   .then(() => {
    //     debug('Succesfully saved')
    //     router.push({ name: 'home' })
    //   })
    //   .catch(error => {
    //     debug('Error saving profile: ', payload, 'failed', error)
    //   })
  },
  updateProfilePhoto: async function(context, payload) {
    const profileId = payload.profile.id
    const token = context.getters.token

    const photoPayload = new FormData()
    photoPayload.append('photo', payload.photo)
    photoPayload.append('id', profileId)

    const response = await instance.put(
      `/api/upload/${profileId}/`,
      photoPayload,
      {
        headers: {
          Authorization: `Token ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      }
    )

    if (response) {
      context.commit('SET_PROFILE', payload.profile)
      context.dispatch('fetchVisibleProfileList')
      router.push({ name: 'home' })
    } else {
      return 'Something went wrong with uploading the photo.'
    }
  }
}

export default {
  state,
  getters,
  mutations,
  actions
}
