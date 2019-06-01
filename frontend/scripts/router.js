import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from './pages/index'
import Project from './pages/project'

Vue.use(VueRouter)

export default new VueRouter({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },
    {
      path: '/project/:id',
      name: 'Project',
      component: Project
    }
  ]
})