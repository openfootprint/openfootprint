import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from './pages/index'
import Project from './pages/project'
import NewProject from './pages/new_project'
import ProjectSettings from './pages/project_settings'
import ProjectHome from './pages/project_home'

Vue.use(VueRouter)

export default new VueRouter({
  routes: [
    {
      path: '/',
      name: 'index',
      component: Index
    },
    {
      path: '/project/:id',
      component: Project,
      children: [
        {
          path: '',
          name: 'project_home',
          component: ProjectHome
        },
        {
          path: 'settings',
          name: 'project_settings',
          component: ProjectSettings
        },
      ]
    },
    {
      path: '/new',
      name: 'new',
      component: NewProject
    }
  ]
})