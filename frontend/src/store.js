/* eslint-disable */
import router from './routes'
import { dedupedTagList, tagList, linkify, instance, clusterList } from './utils'

const debug = require('debug')('cl8.store')


const state = {
  user: null,
  loading: false,
  searchTerm: '',
  searchTags: [],
  searchClusters: [],
  profile: null,
  profilePhoto: null,
  profileShowing: false,
  profileList: [],
  fullTagList: [],
  fullClusterList: [],
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
    if (state.profileList == null) return false

    // Legacy profiles from Airtable have 'yes' in the admin field
    const truthy = ['yes', true]
    return state.profileList
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
  activeClusters: function (state) {
    debug('activeClusters', state.searchClusters)
    return state.searchClusters
  },
  profile: function(state) {
    return state.profile
  },
  profilePhoto: function(state) {
    return state.profilePhoto
  },
  profileList: function(state) {
    debug('getting profileList')
    return state.profileList
  },
  fullTagList: function (state) {
    // check for unsaved tags on the profile, and include
    // them if they are there
    if (state.profile) {
      const combined = state.fullTagList.concat(state.profile.tags)
      return dedupedTagList(combined)
    }
    else {
      return state.fullTagList
    }
  },

  fullClusterList: function (state) {
    debug('getting fullClusterList')
    return state.fullClusterList
  },
  profileShowing: function (state) {
    return state.profileShowing
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
  SET_TAGS: function (state, payload) {
    debug('SET_TAGS', payload)
    state.searchTags = payload
  },
  SET_CLUSTERS: function (state, payload) {
    debug('SET_CLUSTERS', payload)
    state.searchClusters = payload
  },
  SET_AUTH_TOKEN: function (state, payload) {
    debug('SET_AUTH_TOKEN', payload)
    state.token = payload
    localStorage.token = payload
  },
  SET_PROFILE: function(state, payload) {
    debug('SET_PROFILE', payload)
    debug('PROFILE TAGS', payload.tags.map(x => {return x.name}))
    state.profileShowing = true
    state.profile = payload
  },
  SET_PROFILE_TAGS: function (state, payload) {
    debug('SET_PROFILE_TAGS', payload)
    state.profile.tags = payload
  },
  SET_PROFILE_CLUSTERS: function (state, payload) {
    debug('SET_PROFILE_CLUSTERS', payload)
    state.profile.clusters = payload
  },
  SET_TAG_LIST: function (state, payload) {
    debug('SET_TAGS', payload)
    state.fullTagList = payload
  },
  SET_CLUSTER_LIST: function (state, payload) {
    debug('SET_CLUSTERS', payload)
    state.fullClusterList = payload
  },
  setProfilePhoto: function (state, payload) {
    debug('setProfilePhoto', payload)
    state.profile.photo = [payload]
  },
  SET_VISIBLE_PROFILE_LIST: function(state, payload) {
    debug('SET_VISIBLE_PROFILE_LIST', payload)
    state.profileList = payload
  },
  SET_PROFILE_LIST: function (state, payload) {
    debug('SET_PROFILE_LIST', payload)
    state.profileList = payload
  },
  toggleProfileShowing: function (state) {
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
    debug('action:submitEmail')
    const emailPayload = {
      email: payload
    }
    try {
      const emailsubmitted = await instance.post(
        '/auth/email/',
        emailPayload)

      if (emailsubmitted) {
        return true
      } else {
        return false
      }

    }catch(error) {
      return error
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

    const profileResponse = await instance.get('/api/profiles/me', {
      headers: { Authorization: `Token ${token}` }
    })
    context.commit('SET_USER', profileResponse.data)
    context.commit('SET_PROFILE', profileResponse.data)
  },
  updateActiveTags: function (context, payload) {
    debug('action:updateActiveTags')
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
    context.commit('SET_TAGS', tags)
  },
  updateActiveClusters: function (context, payload) {
    debug('action:updateActiveClusters')
    debug('updateActiveClusters', payload)
    let cluster = payload
    let clusters = context.state.searchClusters
    debug('clusters', clusters)
    if (clusters.indexOf(cluster) !== -1) {
      let index = clusters.indexOf(cluster)
      clusters.splice(index, 1)
    } else {
      clusters.push(cluster)
    }
    context.commit('SET_CLUSTERS', clusters)
  },
  fetchProfileList: async function (context) {
    debug('action:fetchProfileList')
    const token = context.getters.token || localStorage.token
    try {
      const response = await instance.get('/api/profiles', {
        headers: { Authorization: `Token ${token}` }
      })

      const profileArray = response.data
      context.commit('SET_PROFILE_LIST', profileArray)
    } catch (error) {
      debug('Error fetching profileList', error)
    }
  },
  fetchTags: async function (context) {
    debug('action:fetchTags')
    const token = context.getters.token || localStorage.token
    try {
      const response = await instance.get('/api/tags', {
        headers: { Authorization: `Token ${token}` }
      })
      context.commit('SET_TAG_LIST', response.data)
    } catch (error) {
      debug('Error fetching tagList', error)
    }
  },
  fetchClusters: async function (context) {
    debug('action:fetchClusters')
    try {
      const response = await instance.get('/api/clusters', {
        headers: { Authorization: `Token ${localStorage.token}` }
      })
      context.commit('SET_CLUSTER_LIST', response.data)
    } catch (error) {
      debug('Error fetching tagList', error)
    }
  },
  addUser: async function(context, payload) {
    debug('action:fetchProfile')
    payload.tags = payload.tags.map(function(obj) {
      return obj.name
    })
    const token = context.getters.token

    const response = await instance.post('/api/profiles/', payload, {
      headers: { Authorization: `Token ${token}` }
    })
    if (response.data) {
      context.dispatch('fetchProfileList')
      context.commit('SET_PROFILE', response.data)
      router.push({ name: 'home' })
    } else {
      return 'There was a problem creating the account'
    }
  },
  fetchProfile: async function(context, payload) {
    debug('action:fetchProfile')
    debug('fetching profile for id:', payload.id)
    const profile = await instance.get(`/api/profiles/${payload.id}`, {
      headers: { Authorization: `Token ${localStorage.token}` }
    })
    context.commit('SET_PROFILE', profile.data)
  },
  resendInvite: async function(context, payload) {
    debug('action:resendInvite')
    const token = context.getters.token
    const profileId = payload.id
    const response = await instance.post(
      `/api/profiles/${profileId}/resend_invite/`,
      profileId,
      {
        headers: {
          Authorization: `Token ${token}`,
        }
      }
    )
    return response
  },
  updateProfile: async function(context, payload) {
    debug('sending update to API', payload)

    // doing this round trip returns a JSON object we
    // can save back to the realtime database more easily,
    // and strips out properties we wouldn't want to save into it
    payload.tags = payload.tags.map(function (obj) {
      return obj.name
    })
    payload.clusters = payload.clusters.map(function (obj) {
      return obj.name
    })


    // add the http(s) if missing
    if (payload.website) {
      payload.website = linkify(payload.website)
    }



    const token = context.getters.token
    const profileId = payload.id

    const profile = await instance.put(`/api/profiles/${profileId}/`, payload, {
      headers: { Authorization: `Token ${token}` }
    })

    if (profile) {
      context.commit('SET_PROFILE', profile.data)
      context.dispatch('fetchprofileList')
      router.push({ name: 'home' })
    } else {
      return 'There was a problem saving changes to the profile.'
    }
  },
  updateProfilePhoto: async function(context, payload) {
    debug('action:updateProfilePhoto')
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

  newProfileTag: async function(context, payload) {
    debug('action:newProfileTag', payload)
    const newTag = payload
    let tempVal =
      newTag.substring(0, 2) + Math.floor(Math.random() * 10000000)
    const tag = {
      name: newTag,
      code: tempVal,
      id: 'tempval' + tempVal
    }
    let profile = context.getters.profile
    let tags = profile.tags 
    tags.push(tag)
  
    context.commit('SET_PROFILE_TAGS', tags)
  },
}

export default {
  state,
  getters,
  mutations,
  actions,
}
