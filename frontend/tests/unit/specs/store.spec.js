import { createLocalVue, enableAutoDestroy } from '@vue/test-utils'

import Store from '@/store'

import Vuex from 'vuex'

import { cloneDeep } from 'lodash'
import { instance } from '@/utils'

enableAutoDestroy(afterEach)

describe('Store/Getters/tagList', () => {

  let localVue, profileList, store

  beforeEach(() => {

    localVue = createLocalVue()
    localVue.use(Vuex)
    profileList = [{
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
    let newStore = cloneDeep(Store);
    newStore.state.profileList = profileList
    newStore.state.fullTagList = [
      {
        "id": 2,
        "slug": "web",
        "name": "web"
      }
    ]
    store = new Vuex.Store(newStore)

  })

  it("returns a list of unique tags from a list of profiles", async () => {
    expect(store.getters.fullTagList).toHaveLength(1)
  })
}),


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

    describe.skip('not authed', () => { })
  })

describe.skip('Store/Actions/fetchVisibleUserList', () => {
  describe('authed', () => {
    it('fetches a list of visible users from our API server ', async () => {
      //  arrange
      const localVue = createLocalVue()
      localVue.use(Vuex)
      const store = new Vuex.Store(Store)
      // act
      await store.dispatch('fetchProfileList')
      // assert
      expect(store.state.profileList).toHaveLength(2)
    })
  })

  describe.skip('not authed', () => { })
})

describe.skip("Store/Actions/newProfileTag", () => {
  it("adds just one tag to a profile with no tags", async () => {
    const localVue = createLocalVue()
    localVue.use(Vuex)

    const sampleProfile = {
      "id": 1,
      "name": "sample_user",
      "tags": [],
    }
    const store = new Vuex.Store(Store)
    store.commit('SET_PROFILE', sampleProfile)
    store.commit('SET_PROFILE_LIST', [sampleProfile])
    expect(store.state.fullTagList).toHaveLength(0)
    expect(store.state.fullTagList).toHaveLength(0)
    await store.dispatch('newProfileTag', 'new tag')


    expect(store.state.fullTagList).toHaveLength(1)
    expect(store.state.profile.tags).toHaveLength(1)
  })

  it("adds just tag to a profile", async () => {

    const localVue = createLocalVue()
    localVue.use(Vuex)

    const profileList = [{
      "id": 1,
      "name": "sample_user",
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
      "name": "second sample_user",
      "tags": [
        {
          "id": 2,
          "slug": "web",
          "name": "web"
        }
      ]
    }]
    const store = new Vuex.Store(Store)
    store.commit('SET_PROFILE', profileList[0])
    store.commit('SET_PROFILE_LIST', profileList)
    store.dispatch('newProfileTag', 'new tag')
    expect(store.state.fullTagList).toHaveLength(2)
    expect(store.state.profile.tags).toHaveLength(2)
  })
}),
  describe("Store/Mutations/SET_PROFILE_TAGS", () => {

    let store

    beforeEach(() => {
      const localVue = createLocalVue()
      localVue.use(Vuex)
      store = new Vuex.Store(Store)
    })

    it("adds an active tag to a profile", async () => {

      const sampleProfile = {
        "id": 1,
        "name": "sample_user",
        "tags": []
      }

      store.commit('SET_PROFILE', sampleProfile)
      await store.dispatch('newProfileTag', "web")
      expect(store.getters.profile.tags).toHaveLength(1)
    })

    it("removes tags no longer on a profile", async () => {
      const sampleProfile = {
        "id": 1,
        "name": "sample_user",
        "tags": [
          {
            "id": 2,
            "slug": "web",
            "name": "web"
          },
        ],
      }

      store.commit('SET_PROFILE', sampleProfile)
      expect(store.getters.profile.tags).toHaveLength(1)
      store.commit('SET_PROFILE_TAGS', [])
      expect(store.getters.profile.tags).toHaveLength(0)
    })
  }),
  describe("Store/Actions/resendInvite", () => {
    let store, localVue, profileList

    beforeEach(() => {

      localVue = createLocalVue()
      localVue.use(Vuex)

      profileList = [
        {
          "id": "1"
        }
      ]
      let newStore = cloneDeep(Store);
      newStore.state.profileList = profileList
      store = new Vuex.Store(newStore)
    })


    it("sends a request to the API to resend a profile's invite email", async () => {

      instance.post = jest.fn(x => {
        return Promise.resolve({message: "OK"})
      })

      const res = await store.dispatch('resendInvite', profileList[0])
      // did we make a call to the API with our?
      expect(instance.post.mock.calls.length).toBe(1)
    })

  })

