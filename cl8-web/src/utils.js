import debugLib from 'debug'
import lodash from 'lodash'

const debug = debugLib('cl8.utils')

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
  // Javscript's equality rules mean we need to stringify the objects
  // to ensure that tags are deduped.
  // TODO: this seems like a terrible way to check equality - surely there's a better way?
  debug('profileList', profileList)
  let tags = new Set()
  console.log(profileList)

  const profileTags = profileList.map((profile) => {
    if (profile.tags) {
      return profile.tags
    }
      else return []
  })

  profileTags.forEach((tagSet) => {
    tagSet.forEach((tag) => {
      debug(`adding tag ${tag.name}`)
      tags.add(JSON.stringify(tag))
    })
  })
  if (tags) {
    debug('tags', tags)
    return Array.from(tags).map((tagString) => { return JSON.parse(tagString)})
  } else {
    return []
  }
}

export {
  linkify,
  fetchCurrentUser,
  tagList
}
