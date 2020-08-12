import { createLocalVue, enableAutoDestroy } from '@vue/test-utils'
import Store from '../../../src/store'
import Vuex from 'vuex'

enableAutoDestroy(afterEach)


describe.skip('Store/Actions/fetchUserList', () => {
  describe('authed', () => {
    it('fetches a list of users from our API server ', async () => {
      //  arrange
      const localVue = createLocalVue()
      localVue.use(Vuex)
      const store = new Vuex.Store(Store)
      // act
      await store.dispatch('fetchProfileList')
      // assert
      expect(store.state.profileList).toHaveLength(3)
    })
  })

  describe.skip('not authed', () => {})
})

describe.skip('Store/Actions/fetchVisibleUserList', () => {
  describe('authed', () => {
    it('fetches a list of visible users from our API server ', async () => {
      //  arrange
      const localVue = createLocalVue()
      localVue.use(Vuex)
      const store = new Vuex.Store(Store)
      // act
      await store.dispatch('fetchVisibleProfileList')
      // assert
      expect(store.state.visibleProfileList).toHaveLength(2)
    })
  })

  describe.skip('not authed', () => {})
})

describe('Store/Getters/tagList', () => {

  let localVue, visibleProfileList, store

  beforeEach(() => {

    localVue = createLocalVue()
    localVue.use(Vuex)

    visibleProfileList = [{
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

  store = new Vuex.Store(Store)
  store.commit('SET_TAG_LIST', visibleProfileList)

  })


  it("returns a list of unique tags from a list of profiles", async () => {

    expect(store.state.fullTagList).toHaveLength(1)
  })
}),
describe.skip("Store/Actions/newProfileTag", () => {
  it("adds just one tag to a profile with no tags", async () => {
    const localVue = createLocalVue()
    localVue.use(Vuex)

    const sampleProfile = {
      "id": 1,
      "name":"sample_user",
      "tags": [],
    }
    const store = new Vuex.Store(Store)
    store.commit('SET_PROFILE', sampleProfile)
    store.commit('setProfileList', [sampleProfile])
    expect(store.state.fullTagList).toHaveLength(0)
    expect(store.state.fullTagList).toHaveLength(0)
    await store.dispatch('newProfileTag', 'new tag')

    expect(store.state.fullTagList).toHaveLength(1)
    expect(store.state.profile.tags).toHaveLength(1)
  })

  it("adds just tag to a profile", async () => {
  
  const localVue = createLocalVue()
    localVue.use(Vuex)

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
    expect(store.state.profile.tags).toHaveLength(2)
  })
}),
describe("Store/Actions/updateProfileTags", () => {
  it("adds an active tag to a profile", async () => {
    const localVue = createLocalVue()
    localVue.use(Vuex)
    const sampleProfile = {
      "id": 1,
      "name":"sample_user",
      "tags": []
    }
    const store = new Vuex.Store(Store)
    store.commit('SET_PROFILE', sampleProfile)
    store.commit('setProfileList', [sampleProfile])
    store.dispatch('updateProfileTags', [
      {
        "id": 2,
        "slug": "web",
        "name": "web"
      },
    ])
    expect(store.state.fullTagList).toHaveLength(1)
  })
  it("removes tags no longer on a profile", async () => {
    const localVue = createLocalVue()
    localVue.use(Vuex)
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

