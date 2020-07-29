import Vue from 'vue'
import { mount } from '@vue/test-utils'

import ProfileTagsComponent from '@/components/profile/ProfileTagsComponent'

let sampleData = {
  fields: {
    admin: 'true',
    bio: '',
    email: 'someone@domain.com',
    tags: [
      {
        "id": 2,
        "slug": "web",
        "name": "web"
      },
      {
        "id": 3,
        "slug": "scoped-emissions",
        "name": "scoped emissions"
      }
    ],
    visible: 'yes',
  },
  id: 'recxxxxxxxxxxxxxx',
}

const sampleTagList = [
  {
    "id": 2,
    "slug": "web",
    "name": "web"
  },
  {
    "id": 3,
    "slug": "scoped-emissions",
    "name": "scoped emissions"
  },
  {
    "id": 5,
    "slug": "sustainable-software-engineering",
    "name": "sustainable software engineering"
  },
  {
    "id": 6,
    "slug": "dgen",
    "name": "dgen"
  },
  {
    "id": 7,
    "slug": "python",
    "name": "python"
  },
  {
    "id": 8,
    "slug": "carbon",
    "name": "carbon"
  },
  {
    "id": 9,
    "slug": "javascript",
    "name": "javascript"
  },
  {
    "id": 10,
    "slug": "community-management",
    "name": "community management"
  }
]

describe('ProfileTagsComponent', () => {
  it('shows a list of active tags', () => {
    const wrapper = mount(ProfileTagsComponent, {
      propsData: { data: sampleData.fields.tags, options: sampleTagList }
    })
    expect(wrapper.findAll('#tags button.active').length).toBe(2)
    // expect(wrapper.findAll('.gravatar').length).toBe(0)
  })
  it('shows a list of inactive tags too', () => {
    const wrapper = mount(ProfileTagsComponent, {
      propsData: { data: sampleData.fields.tags, options: sampleTagList}
    })
    expect(wrapper.findAll('#tags button').length).toBe(8)
    // expect(wrapper.findAll('.gravatar').length).toBe(1)
  })
})
