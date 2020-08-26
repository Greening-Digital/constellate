import Vue from 'vue'
import { mount, createLocalVue } from '@vue/test-utils'
import VueRouter from 'vue-router'


import TheProfileList from '@/components/TheProfileList.vue'
import debugLib from 'debug'
const debug = debugLib('cl8.TheProfileList.spec')

let sampleData = [{
  admin: 'true',
  bio: '',
  email: 'someone@domain.com',
  visible: 'yes',
  id: 'rec1a',
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
},
{
  admin: false,
  bio: '',
  email: 'someone.else@domain.com',
  visible: 'yes',
  id: 'rec2',
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
}]


describe('TheProfileList', () => {
  let wrapper, mockStore

  beforeEach(() => {
    mockStore = {
      getters: {
        profileList: sampleData,
      },
      dispatch: jest.fn(),
      commit: jest.fn()
    }

    const localVue = createLocalVue()
    localVue.use(VueRouter)
    const router = new VueRouter()

    wrapper = mount(TheProfileList, {
      localVue,
      mocks: {
        $store: mockStore,
        stubs: ['router-view']
      },

    })
  })
  it('renders the component', async () => {
    expect(wrapper.html()).toBeTruthy()
  })
  it('renders a list of profiles', async () => {
    expect(wrapper.html()).toBeTruthy()
    expect(wrapper.findAll('.list .peep').length).toBe(2)
  })
})
