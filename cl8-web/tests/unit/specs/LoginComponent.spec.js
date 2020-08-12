
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

  describe.only('requesting token with valid email', () => {

      beforeEach(() => {
        // set up state as if email was sent
        wrapper = mount(Login, {
          localVue,
          data() {
            return {
              email: 'valid.email@domain.com',
              emailSubmitted: true,
              formIsValid: true
            }
          },
          mocks: {
            $store: {
              getters: {
                isLoading: false,
                signInData: {
                  message: null,
                  email: 'valid.email@domain.com',
                }
              },
              dispatch: mockStore.dispatch
            }
          }
        })
      })

      it('shows new guidance after a user submits their email', async () => {
        expect(wrapper.get('p.next-step-guidance').toBeTruthy()
      })

      it('sends the provided token to finish sign in', async () => {

        // when we add the token, check that the action is dispatched
        wrapper.find('input[name="login-code"]').setValue(123456)
        wrapper.get('button[name="sign-in"]').trigger('click')

        expect(wrapper.vm.$store.dispatch).toHaveBeenCalledWith('login',
          {email: 'valid.email@domain.com', token: "123456"}
        )
      })
  })
})
