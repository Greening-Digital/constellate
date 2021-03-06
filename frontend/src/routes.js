import Vue from 'vue'
import Router from 'vue-router'

import Login from '@/components/auth/Login'
import ResetPassword from '@/components/auth/ResetPassword'
import NewPassword from '@/components/auth/NewPassword'

import TheHomePanel from '@/components/TheHomePanel'

import AddUser from '@/components/admin/AddUser'
import ProfileEdit from '@/components/profile/ProfileEdit'
import ProfilePhoto from '@/components/profile/ProfilePhoto'

const debug = require('debug')('cl8.route')

Vue.use(Router)

const router = new Router({
  // adding this here, until we figure out a
  // sensible way to do the no hash urls, and still have django handle 404 codes.
  // mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      component: TheHomePanel,
      meta: { requiresAuth: true }
    },
    {
      path: '/profile/:profileId',
      name: 'viewProfile',
      component: TheHomePanel,
      meta: { requiresAuth: true }
    },
    {
      path: '/edit',
      name: 'editProfile',
      component: ProfileEdit,
      meta: { requiresAuth: true }
    },
    {
      path: '/photo',
      name: 'editProfilePhoto',
      component: ProfilePhoto,
      meta: { requiresAuth: true }
    },
    {
      path: '/signin',
      name: 'signin',
      component: Login
    },
    {
      path: '/reset-password',
      name: 'resetPassword',
      component: ResetPassword
    },
    {
      path: '/new-password',
      name: 'newPassword',
      component: NewPassword
    },
    {
      path: '/add-user',
      name: 'addUser',
      component: AddUser
    },
    {
      path: '*',
      redirect: 'home'
    }
  ]
})

export default router
