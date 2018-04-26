import Vue from 'vue'
import Router from 'vue-router'
import CollectionList from '@/components/CollectionList'
import Uploads from '@/components/Uploads'
import NewCollection from '@/components/NewCollection'

Vue.use(Router)

var routes = [
  {path: '/', name: 'CollectionList', component: CollectionList,
    name:'collection.index'},
  {path: '/uploads', name: 'Uploads', component: Uploads},
  {path: '/new-collection', name: 'NewCollection', component: NewCollection}]

export default new Router({
  routes: routes
})
