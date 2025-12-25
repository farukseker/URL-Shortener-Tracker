import { createRouter, createWebHistory } from 'vue-router'
import BaseView from '../views/BaseView.vue'
import default_layout from '../layouts/default.vue' 


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: default_layout,
      meta: {
        title: 'Url Tracker'
      },
      children: [
        {
          path: '',
          name: 'home',
          component: BaseView
        },
        {
          path: '/add',
          name: 'add-url',
          component: () => import('../views/AddUrlView.vue'),
          meta: { title: 'Create New Url Tracker' }
        },
        {
          path: '/r/:url_code',
          name: 'manage-url',
          props:true,
          component: () => import('../views/UrlView.vue'),
          meta: { title: 'Manage Url' }
        },
        {
          path: '/categories',
          name: 'category-manage',
          component: () => import('../views/CategoryManage.vue'),
          meta: { title: 'Manage Categories' }

        }
      ]

    },

    
    // {
    //   path: '/about',
    //   name: 'about',
    //   component: () => import('../views/AboutView.vue'),
    // },
  ],
})

export default router
