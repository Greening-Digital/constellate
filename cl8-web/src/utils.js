import debugLib from 'debug'
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

export {
  linkify,
  fetchCurrentUser
}
