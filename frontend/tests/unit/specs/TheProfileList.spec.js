
import { mount, createLocalVue } from '@vue/test-utils'
import VueRouter from 'vue-router'
import VueFuse from 'vue-fuse'
import { cloneDeep } from 'lodash'

import TheProfileList from '@/components/TheProfileList.vue'
import debugLib from 'debug'
const debug = debugLib('cl8.TheProfileList.spec')

let sampleData = [{
  admin: 'true',
  bio: '',
  email: 'someone@domain.com',
  visible: 'yes',
  id: 'rec1a',
  clusters: [],
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
  clusters: [
    {
      "id": 2,
      "slug": "open-energy",
      "name": "open energy"
    },
  ],
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
  let wrapper, mockStore, localVue

  describe('no filtering by tag', () => {
    beforeEach(() => {
      mockStore = {
        getters: {
          profileList: sampleData,
        },
        dispatch: jest.fn(),
        commit: jest.fn()
      }

      localVue = createLocalVue()
      localVue.use(VueRouter)
      const router = new VueRouter()

      wrapper = mount(TheProfileList, {
        localVue,
        mocks: {
          $store: mockStore,
          stubs: ['router-view'],
          $t: () => { }
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

  describe('filtered by tag', () => {

    beforeEach(() => {
      mockStore = {
        getters: {
          profileList: sampleData,
          activeTags: ['dgen']
        },
        dispatch: jest.fn(),
        commit: jest.fn()
      }

      localVue = createLocalVue()
      localVue.use(VueRouter)
      localVue.use(VueFuse)
      const router = new VueRouter()

      wrapper = mount(TheProfileList, {
        localVue,
        mocks: {
          $store: mockStore,
          stubs: ['router-view'],
          $t: () => { }
        },

      })
    })


    it('renders a list of profiles matching the tag', async () => {
      expect(wrapper.html()).toBeTruthy()
      console.log(wrapper.html())

      await wrapper.vm.checkAgainstSearch()
      expect(wrapper.findAll('.list .peep').length).toBe(1)
    })
  })
  describe('filtered by cluster', () => {
    beforeEach(() => {
      mockStore = {
        getters: {
          profileList: sampleData,
          activeClusters: ['open energy']
        },
        dispatch: jest.fn(),
        commit: jest.fn()
      }

      localVue = createLocalVue()
      localVue.use(VueRouter)
      localVue.use(VueFuse)
      const router = new VueRouter()

      wrapper = mount(TheProfileList, {
        localVue,
        mocks: {
          $store: mockStore,
          stubs: ['router-view'],
          $t: () => { }
        },
      })
    })


    it('renders a list of profiles matching the cluster', async () => {
      expect(wrapper.html()).toBeTruthy()

      await wrapper.vm.checkAgainstSearch()
      expect(wrapper.vm.matchingTags()).toHaveLength(1)
      expect(wrapper.findAll('.list .peep').length).toBe(1)
    })
    it.only('it dispatches a call to updateActiveClusters on click', async () => {
      expect(wrapper.html()).toBeTruthy()

      await wrapper.vm.checkAgainstSearch()
      expect(wrapper.vm.matchingTags()).toHaveLength(1)
      expect(wrapper.get('button[data-name="open energy"]').trigger('click'))
      expect(mockStore.dispatch).toHaveBeenCalledWith('updateActiveClusters', "open energy")
    })
  })

})
