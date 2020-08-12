
import { mount, shallow, createLocalVue } from '@vue/test-utils'
import VeeValidate from 'vee-validate'
import Login from '@/components/auth/Login.vue'

import debugLib from 'debug'

const debug = debugLib('cl8.LoginComponent.spec')


// we need to augment our Vue object for this component test
// as we're not evaluating any setup in main.js
const localVue = createLocalVue()
const config = { events: 'blur' }
localVue.use(VeeValidate, config)

debug('localvue validator', localVue.$validator)

describe('Login.Vue', () => {

  // declare mutable variable
  let wrapper

  let mockStore = {
    getters: {
      isLoading: true,
      signInData: {
        message: null,
        email: null
      }
    },
    dispatch: jest.fn()
  }

  describe('mounting with expected data', () => {

    wrapper = mount(Login, {
      mocks: {
        $store: mockStore
      }
    })

    test('login mounts with when loading ', () => {

      expect(wrapper.html()).toMatchSnapshot()
      expect(wrapper.findAll('form').length).toBe(0)
    })

    test('shows login form when loaded', async () => {
      mockStore.getters.isLoading = false

      wrapper = mount(Login, {
        mocks: {
          $store: mockStore
        }
      })

      
      expect(wrapper.html()).toMatchSnapshot()
      expect(wrapper.findAll('form').length).toBe(1)
    })
  })


  describe('mounting and loading', () => {

    describe('with valid data', () => {
      mockStore.getters.isloading = false

      wrapper = mount(Login, {
        localVue,
        mocks: {
          $store: mockStore
        }
      })

      test('the submit button should be disabled with invalid data', () => {

        expect(wrapper.find('button').element.disabled).toBeTruthy()
      })

      test.skip('the submit button should no longer be disabled with valid data', async () => {

          // set the email now
          // update the store here
          await wrapper.vm.$nextTick()

          // set the value
          wrapper.find("input[name='email']").setValue("valid.email@domain.com")
          // for reasons which aren't obvious we need to set the data too,
          // wrapper.setData({email: "valid.email@domain.com"})
          wrapper.find("input[name='email']").trigger('blur')

          // Because validation occurs on blur
        // I think we need to simulate this
          await flushPromises();
          await wrapper.vm.$nextTick()


          expect(wrapper.find('button').element.disabled).toBe(false)
        })

    })
  })
})