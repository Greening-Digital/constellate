
import { mount, createLocalVue} from '@vue/test-utils'

import ProfilePhoto from '@/components/profile/ProfilePhoto'
import Gravatar from 'vue-gravatar'
import debugLib from 'debug'

const debug = debugLib('cl8.ProfilePhoto.spec')

let sampleProfile = {
    visible: 'yes',
    id: 'recxxxxxxxxxxxxxx',
}

describe('ProfilePhoto', () => {
  it('tries to render a gravatar if no photo provided', () => {
    const localVue = createLocalVue()

    localVue.component('v-gravatar', Gravatar);
    const wrapper = mount(ProfilePhoto, {
      mocks: {
        $store: {
          getters: {
            profile: sampleProfile,
            currentUser: sampleProfile
          },
          commit: jest.fn(),
        },
        $t: () => {}
      },
      stubs: ['router-link'],
      localVue
    })
    expect(wrapper.findAll('.gravatar').length).toBe(1)
  })
  it('shows a photo if the profile has it', () => {
    const profileWithPic = {
      photo: 'sample-photo.png',
      id: 'recxxxxxxxxxxxxxx',
    }

    const wrapper = mount(ProfilePhoto, {
      mocks: {
        $store: {
          getters: {
            profile: profileWithPic,
            user: profileWithPic
          },
          commit: jest.fn(),
        },
        $t: () => {}
      },
      stubs: ['router-link', 'v-gravatar']
    })
    expect(wrapper.findAll('img.supplied-photo').length).toBe(1)
  })
  it('shows a local photo once added', async () => {

    const wrapper = mount(ProfilePhoto, {
      mocks: {
        $store: {
          getters: {
            profile: sampleProfile,
            user: sampleProfile
          },
          commit: jest.fn(),
        },
        $t: () => {},
      },
      stubs: ['router-link', 'v-gravatar']
    })

    // simulate an upload with set data
    // then await to allow for the Vue.nextTick()
    // event to trigger, uploading the DOM to show provided local image
    // for more, see:
    // https://vue-test-utils.vuejs.org/guides/testing-async-components.html
    await wrapper.setData({ localPhoto: "blob:somefilename-url" })

    // call html() as a sanity check to see what's being rendered
    // debug(wrapper.html())
    expect(wrapper.vm.localPhoto).toBe("blob:somefilename-url")
    expect(wrapper.findAll('img.local-photo').length).toBe(1)
  })
})
