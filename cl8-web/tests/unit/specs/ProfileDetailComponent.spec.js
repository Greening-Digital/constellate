
import { mount } from '@vue/test-utils'
import { cloneDeep } from 'lodash'


import ProfileDetail from '@/components/profile/ProfileDetail'

let sampleData = {
  admin: 'true',
  blurb: '',
  email: 'gavin@dgen.net',
  facebook: '',
  linkedin: 'linkedin.com/in/gavinstarks',
  name: 'Gavin Starks',
  phone: '',
  photo: 'https://dl.airtable.com/9A3XP2U7TvWKZVAZXtc0_large_me.jpg',
  tags: [
    {
      id: 'rec8AoQ0MPMJQxYKK',
      name: 'Open Data'
    },
    {
      id: 'rec0E1cKWxINp13lg',
      name: 'Air Quality'
    }
  ],
  twitter: 'agentGav',
  visible: 'yes',
  website: 'dgen.net',
  id: 'recxxxxxxxxxxxxxx',
}

describe('ProfileDetail', () => {

  let wrapper, mockStore

  function mountWrapper(component, mockStore) {
    return mount(component, {
      mocks: {
        $store: mockStore,
        $t: () => {}
      },
      stubs: ['router-link']
    })
  }


  beforeEach(() => {
    mockStore = {
      getters: {
        profile: sampleData,
        currentUser: sampleData
      },
      dispatch: jest.fn(),
      commit: jest.fn()
    }
  })


  it('shows a user provided photo if present', () => {
    wrapper = mountWrapper(ProfileDetail, mockStore)
    expect(wrapper.findAll('img.supplied-photo').length).toBe(1)
    expect(wrapper.findAll('.gravatar').length).toBe(0)
  })
  it('otherwise shows a gravatar image', () => {

    let copyData = JSON.parse(JSON.stringify(sampleData))
    copyData.photo = null
    mockStore.getters.profile = copyData
    mockStore.getters.currentUser = copyData
    wrapper = mountWrapper(ProfileDetail, mockStore)
    expect(wrapper.findAll('img.supplied-photo').length).toBe(0)
    expect(wrapper.findAll('.gravatar').length).toBe(1)
  })

  describe("showing clusters:", () => {

    let clusterProfileData

    describe("profile with active clusters", () => {
      beforeEach(() => {

        clusterProfileData = cloneDeep(sampleData);

        mockStore = {
          getters: {
            profile: clusterProfileData,
            currentUser: clusterProfileData
          },
          dispatch: jest.fn(),
          commit: jest.fn()
        }
      })

      it('shows a list of cluster if we have clusters', async () => {
        clusterProfileData.clusters = [
          {
            "id": 2,
            "slug": "open-energy",
            "name": "open energy"
          },
        ]
        mockStore.getters.profile = clusterProfileData
        mockStore.getters.currentUser = clusterProfileData

        wrapper = mountWrapper(ProfileDetail, mockStore)
        expect(wrapper.vm.hasActiveClusters()).toBe(true)
        expect(wrapper.get(".cluster-component")).toBeTruthy()
      })

      it('shows no cluster head', async () => {
        wrapper = mountWrapper(ProfileDetail, mockStore)
        expect(wrapper.vm.hasActiveClusters()).toBeFalsy()
        expect(wrapper.findAll(".cluster-component").length).toBe(0)
      })
    })
  })

  describe("resending invites:", () => {

    beforeEach(() => {
      mockStore.dispatch = jest.fn(function(x) {
        return new Promise((resolve, reject) => {
        resolve({data: { message: "Success message"}})
        reject({data: { message: "Fail message"}})
        })
      })
    })


    it("shows a resend invite button if the user is an admin", async () => {
      wrapper = mountWrapper(ProfileDetail, mockStore)
      expect(wrapper.findAll('.resend-invite').length).toBe(1)
    })

    it("does not show a resend button to regular users", async () => {
      let regUserData = JSON.parse(JSON.stringify(sampleData))
      regUserData.admin = false
      mockStore.getters.currentUser = regUserData
      wrapper = mountWrapper(ProfileDetail, mockStore)
      expect(wrapper.findAll('.resend-invite').length).toBe(0)
    })

    it("dispatches a sendInvite action on click", async() => {
      wrapper = mountWrapper(ProfileDetail, mockStore)
      wrapper.get("button.resend-invite").trigger('click')
      await wrapper.vm.$nextTick()
      expect(mockStore.dispatch).toHaveBeenCalledWith('resendInvite', mockStore.getters.profile)
    })

    it("updates status message on click", async () => {
      wrapper = mountWrapper(ProfileDetail, mockStore)
      wrapper.get("button.resend-invite").trigger('click')
      await wrapper.vm.$nextTick()
      expect(wrapper.vm.flashMessage).toMatch("Success message")
    })

    describe("showing and hiding the updated message box", () => {

      // Because we have animations in play, we need to do TWO calls to
      // `await wrapper.vm.$nextTick()`
      // after an interaction that would trigger an animated transition.
      // if we don't do this, the next tick end up rendering a stubbed out
      // animation, and the tests will fail

      it("shows a status message on click", async() => {
        wrapper = mountWrapper(ProfileDetail, mockStore)
        wrapper.get("button.resend-invite").trigger('click')
        // see above for why we have two calls next to each other
        await wrapper.vm.$nextTick()
        await wrapper.vm.$nextTick()
        expect(wrapper.get(".status-message")).toBeTruthy()
      })

      it("can be dismissed with a click", async() => {
        wrapper = mountWrapper(ProfileDetail, mockStore)
        wrapper.get("button.resend-invite").trigger('click')

        await wrapper.vm.$nextTick()
        await wrapper.vm.$nextTick()

        wrapper.get(".status-message .close").trigger('click')
        await wrapper.vm.$nextTick()
        await wrapper.vm.$nextTick()

        expect(wrapper.vm.flashMessage).toMatch("")
        expect(wrapper.vm.showFlashMessage).toBe(false)
      })
    })
  })
})
