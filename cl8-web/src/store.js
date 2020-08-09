/* eslint-disable */
import router from './routes'
import axios from 'axios'
import { tagList } from './utils'
import { reject } from 'lodash'

const debug = require('debug')('cl8.store')

const instance = axios.create({
  timeout: 60000,
  // `xsrfHeaderName` is the name of the http header
  // that carries the xsrf token value
  xsrfCookieName: 'csrftoken', // default
  xsrfHeaderName: 'X-CSRFTOKEN', // default

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
  fullTagList: '',
  requestUrl: null,
  signInData: {
    message: null,
    email: null
  },
  token: localStorage.token || null
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
  fullTagList: function(state) {
    debug('getting fullTagList:', state.fullTagList.length)
    return state.fullTagList
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
    return state.token
  }
}

const mutations = {
  CLEAR_USER: function(state) {
    state.profile = null
    state.user = null
    state.token = null
    delete localStorage.token;
    debug('localStorage', localStorage);
    debug('state', state);

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
  SET_TAG_LIST: function(state, payload) {
    debug('profiles:', payload)
    state.fullTagList = tagList(payload)
    debug('tagList:', state.fullTagList.length)
  } ,
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

    const emailsubmitted = await instance.post(
      '/auth/email/',
      emailPayload)

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

      debug('prev token', context.getters.token)
      context.commit('SET_AUTH_TOKEN', token)
      debug('updated token', context.getters.token)
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

    const token = context.getters.token || localStorage.token
    debug('creating user session with token:', token)

    const profileResponse = await instance.get('api/profiles/me', {
      headers: { Authorization: `Token ${token}` }
    })
    context.commit('SET_USER', profileResponse.data)
    context.commit('SET_PROFILE', profileResponse.data)
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
      debug('profiles resp', response)
      const profileArray = response.data.filter(profile => profile.visible)
      context.commit('setVisibleProfileList', profileArray)
      context.commit('SET_TAG_LIST', profileArray)

    } catch (error) {
      debug('Error fetching visibleProfileList', error)
    }
  },
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
    debug('fetching profile for id:', payload.id)
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
  },
  updateProfileTags: function(context, payload) {
    // update the profile locally, without saving
    // given that we have updateProfle above, we may be better
    // with save Profile to send data to the server and update for local store changes
    const profile = context.getters.profile
    profile.tags = payload
    context.commit('SET_PROFILE', profile)
    context.dispatch('updateProfileList', profile)
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
      context.commit('SET_PROFILE', response.data)
      context.dispatch('updateProfileList', response.data)
      router.push({ name: 'home' })
    } else {
      return 'Something went wrong with uploading the photo.'
    }
  },
  updateProfileList: function(context, payload)   {
      let profiles = context.getters.visibleProfileList
      debug(`profiles count: ${profiles.length}`)
      let newProfileList = reject(profiles, function(prof) {
        return prof.id === payload.id
      })
      debug(`newProfiles count: ${newProfileList.length}`)
      newProfileList.push(payload)
      debug(`updated newProfiles count: ${newProfileList.length}`)
      context.commit('setVisibleProfileList', newProfileList)
      context.commit('SET_TAG_LIST', newProfileList)

  },
  newProfileTag: async function(context, payload) {
    debug('new tag', payload)
    const newTag = payload
    let tempVal =
      newTag.substring(0, 2) + Math.floor(Math.random() * 10000000)
    const tag = {
      name: newTag,
      code: tempVal,
      id: 'tempval' + tempVal
    }
    const profile = context.getters.profile
    profile.tags.push(tag)
    // const tags = context.getters.fullTagList
    context.commit('SET_PROFILE', profile)
    context.dispatch('updateProfileList', profile)
  },
}


export default {
  state,
  getters,
  mutations,
  actions
}
