import debugLib from 'debug'
import axios from 'axios'
const debug = debugLib('cl8.utils')

function hasPhoto (profile) {

  if (!profile) {
    return false
  }

  debug({photoPhoto: profile.photo})
  if (profile.photo != null && profile.photo.length > 0) {
    return true
  }
  // otherwise just return false
  return false
}

function linkify (url, prefix) {
  // check if link already starts with 'http:', return if so
  let pattern = RegExp(/https?:/)
  if (pattern.test(url)) {
    return url
  }

  if (prefix) {
    return `${prefix}/${url}`
  } // looks like we need to add it outselves. We can't assume https

  return `http://${url}`
}

async function fetchCurrentUser(store) {
  debug('currentProfile', store.getters.currentUser)
  if (!localStorage.token) {
    return false
  }
  if (!store.getters.currentUser && localStorage.token) {
    await store.dispatch('createUserSession')
  }

  return store.getters.currentUser
}

function tagList(profileList) {
  debug('profileList length', profileList.length)
  let tags = []

  const profileTags = profileList.map((profile) => {
    if (profile.tags) {
      return profile.tags
    }
      else return []
  })


  profileTags.forEach((tagSet) => {
    tagSet.forEach((tag) => {

      let tagNames
      if (tags.length > 0) {
        const tagNames = tags.map(x => { return  x.name})
        if (!tagNames.includes(tag.name)) {
          tags.push(tag)
        }
      } else {
        tags.push(tag)
      }
    })
  })

  return tags
}

const instance = axios.create({
  timeout: 60000,
  // `xsrfHeaderName` is the name of the http header
  // that carries the xsrf token value
  xsrfCookieName: 'csrftoken', // default
  xsrfHeaderName: 'X-CSRFTOKEN', // default

})


export {
  linkify,
  fetchCurrentUser,
  tagList,
  hasPhoto,
  instance
}
