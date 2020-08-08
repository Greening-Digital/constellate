import { createLocalVue } from '@vue/test-utils'
import Store from '../../../src/store'
import Vuex from 'vuex'

describe.skip('Store/Actions/fetchUserList', () => {
  describe('authed', () => {
    it('fetches a list of users from our API server ', async () => {
      //  instantivate Vue
      const localVue = createLocalVue()
      localVue.use(Vuex)
      const store = new Vuex.Store(Store)
      // call action
      await store.dispatch('fetchProfileList')
      // assert we have what we think we have
      expect(store.state.profileList).toHaveLength(3)
    })
  })

  describe.skip('not authed', () => {})
})

describe.skip('Store/Actions/fetchVisibleUserList', () => {
  describe('authed', () => {
    it('fetches a list of visible users from our API server ', async () => {
      //  instantivate Vue
      const localVue = createLocalVue()
      localVue.use(Vuex)
      const store = new Vuex.Store(Store)
      // call action
      await store.dispatch('fetchVisibleProfileList')
      // assert we have what we think we have
      expect(store.state.visibleProfileList).toHaveLength(2)
    })
  })

  describe.skip('not authed', () => {})
})

describe('Store/Getters/tagList', () => {
  it("returns a list of unique tags from a list of profiles", async () => {
    //  instantivate Vue
    const localVue = createLocalVue()
    localVue.use(Vuex)
    // console.log(Store.state)
    const visibleProfileList = [{
      "tags": [
        {
          "id": 2,
          "slug": "web",
          "name": "web"
        },
      ],
    },
    {
      "tags": [
        {
          "id": 2,
          "slug": "web",
          "name": "web"
        }
      ]
    }]

    // console.log(Store.state)
    const store = new Vuex.Store(Store)
    // call action
    // await store.dispatch('fetchVisibleProfileList')
    store.commit('SET_TAG_LIST', visibleProfileList)
    // assert we have what we think we have
    // expect(store.state.visibleProfileList).toHaveLength(2)
    expect(store.state.fullTagList).toHaveLength(1)
  })
}),
describe("Store/Actions/newProfileTag", () => {
  it("adds a tag to a profile", async () => {
    const localVue = createLocalVue()
    localVue.use(Vuex)
    // console.log(Store.state)
    const visibleProfileList = [{
      "id": 1,
      "name":"sample_user",
      "tags": [
        {
          "id": 2,
          "slug": "web",
          "name": "web"
        },
      ],
    },
    {
      "id": 1,
      "name":"second sample_user",
      "tags": [
        {
          "id": 2,
          "slug": "web",
          "name": "web"
        }
      ]
    }]
    const store = new Vuex.Store(Store)
    store.commit('SET_PROFILE', visibleProfileList[0])
    store.commit('setProfileList', visibleProfileList)
    store.dispatch('newProfileTag', 'new tag')
    expect(store.state.fullTagList).toHaveLength(2)
  })
}),
describe("Store/Actions/updateProfileTags", () => {
  it("adds removes tags no longer on a profile", async () => {
    const localVue = createLocalVue()
    localVue.use(Vuex)
    // console.log(Store.state)
    const sampleProfile = {
      "id": 1,
      "name":"sample_user",
      "tags": [
        {
          "id": 2,
          "slug": "web",
          "name": "web"
        },
      ],
    }
    const store = new Vuex.Store(Store)
    store.commit('SET_PROFILE', sampleProfile)
    store.commit('setProfileList', [sampleProfile])
    store.dispatch('updateProfileTags', [])
    expect(store.state.fullTagList).toHaveLength(0)

  })
})

