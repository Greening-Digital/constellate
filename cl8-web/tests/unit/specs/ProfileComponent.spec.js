import Vue from 'vue'
import { mount } from '@vue/test-utils'

import ProfileDetail from '@/components/profile/ProfileDetail'

let sampleData = {
  admin: 'true',
  blurb: '',
  email: 'gavin@dgen.net',
  facebook: '',
  linkedin: 'linkedin.com/in/gavinstarks',
  name: 'Gavin Starks',
  phone: '',
  photo: "https://dl.airtable.com/9A3XP2U7TvWKZVAZXtc0_large_me.jpg",

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
  let mockStore

  beforeEach(() => {
    mockStore = {
      getters: {
        profile: sampleData,
        currentUser: sampleData,
      },
      dispatch: jest.fn(),
      commit: jest.fn()
    }
  })

  it('shows a user provided photo if present', () => {
    const wrapper = mount(ProfileDetail, {
      mocks: {
        $store: mockStore,
        $t: () => {}
      }
    })
    expect(wrapper.findAll('img.supplied-photo').length).toBe(1)
    expect(wrapper.findAll('.gravatar').length).toBe(0)
  })
  it('otherwise shows a gravatar image', () => {
    let copyData = JSON.parse(JSON.stringify(sampleData))
    copyData.photo = null
    mockStore.getters.profile = copyData
    let wrapper = mount(ProfileDetail, {
      mocks: {
        $store: mockStore,
        $t: () => {}
      }
    })
    expect(wrapper.findAll('img.supplied-photo').length).toBe(0)
    expect(wrapper.findAll('.gravatar').length).toBe(1)
  })
})
