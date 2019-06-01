import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from './pages/index'
import Project from './pages/project'
import NewProject from './pages/new_project'

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
    },
    {
      path: '/new',
      name: 'New Project',
      component: NewProject
    }
  ]
})