import Vue from 'vue'
import { mount } from '@vue/test-utils'

import ProfileSearchItem from '@/components/profile/ProfileSearchItem.vue'

const { axe, toHaveNoViolations } = require('jest-axe')
expect.extend(toHaveNoViolations)

let sampleData = {
  "admin": "true",
  "blurb": "",
  "email": "gavin@dgen.net",
  "facebook": "",
  "linkedin": "linkedin.com/in/gavinstarks",
  "name": "Gavin Starks",
  "phone": "",
  "photo": "https://dl.airtable.com/9A3XP2U7TvWKZVAZXtc0_large_me.jpg",
  "photo_thumbail": "https://dl.airtable.com/v3cYyYiiQ21uXBPgzesu_small_me.jpg",
  "tags": [
    {
      "id": "rec8AoQ0MPMJQxYKK",
      "name": "Open Data"
    },
    {
      "id": "rec0E1cKWxINp13lg",
      "name": "Air Quality"
    }
  ],
  "twitter": "agentGav",
  "visible": "yes",
  "website": "dgen.net",
  "id": "rec9zRtYSMEj8CoJk",
}

describe('ProfileSearchItem', () => {
  
  
  it('shows a user provided photo if present', () => {
    let wrapper = mount(ProfileSearchItem, {
      propsData: { item: sampleData }
    })
    expect(wrapper.findAll('img.supplied-photo').length).toBe(1)
    expect(wrapper.findAll('.gravatar').length).toBe(0)
  })
  it('otherwise shows a gravatar image', () => {
    let copyData = JSON.parse(JSON.stringify(sampleData))
    copyData.photo = null
    let wrapper = mount(ProfileSearchItem, {
      propsData: { item: copyData }
    })
    expect(wrapper.findAll('img.supplied-photo').length).toBe(0)
    expect(wrapper.findAll('.gravatar').length).toBe(1)
  })
  it.skip('passes a11y', async() => {
    let wrapper = mount(ProfileSearchItem, {
      propsData: { item: sampleData }
    })
    const results = await axe(wrapper.element)
    expect(results).toHaveNoViolations()
  })
})
