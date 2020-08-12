
import { mount, shallow, createLocalVue } from '@vue/test-utils'
import VeeValidate from 'vee-validate'
import Login from '@/components/auth/Login.vue'

// we need to augment our Vue object for this component test
// as we're not evaluating any setup in main.js
const localVue = createLocalVue()
const config = { events: 'blur' }
localVue.use(VeeValidate, config)

describe('Login.Vue', () => {

  // declare variable to overwrite
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

    test('login mounts with when loading ', () => {
      wrapper = mount(Login, {
        mocks: {
          $store: mockStore
        }
      })

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
        console.log(wrapper)
        expect(wrapper.find('button').element.disabled).toBe(true)
      })

      test.skip('the submit button should no longer be disabled with valid data', async () => {

          // set the email now
          // update the store here
          console.log(wrapper.localVue)


          await wrapper.vm.$nextTick()
          // set the value
          wrapper.find("input[name='email']").setValue("valid.email@domain.com")
           // for reasons which aren't obvious we need to set the data too,
          // wrapper.setData({email: "valid.email@domain.com"})
          wrapper.find("input[name='email']").trigger('blur')
        // Because validation occurs on blur
        // I think we need to simulate this
          await wrapper.vm.$nextTick()

          // console.log(wrapper.html())

          // console.log(otherMount.find('button').element.disabled)
          expect(wrapper.find('button').element.disabled).toBe(false)
        })

    })
  })
})