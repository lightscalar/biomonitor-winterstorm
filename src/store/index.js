import Vue from 'vue'
import Vuex from 'vuex'
import api from '../api/index'
Vue.use(Vuex)

export default new Vuex.Store ({

  state: {

    volumes: [],
    collections: [],
    sysStatus: 'OK',
    annotations: []

  },

  mutations: {

    setVolumes (state, volumes) {
      state.volumes = volumes
    },

    setAnnotations (state, annotations) {
      state.annotations = annotations
    },

    setCollections (state, collections) {
      console.log(collections)
      state.collections = collections
    },

    updateStatus (state, sysStatus) {
      state.sysStatus = sysStatus
    }


  },

  actions: {

    configureCard (context, config) {
      api.postResource('configurations', config).then(function (resp) {
        context.commit('updateStatus', resp.data['sysStatus'])
      })
    },

    getCollections (context) {
      api.listResource('collections').then( function (resp) {
        context.commit('setCollections', resp.data)
      })
    },

    getVolumes (context) {
      api.listResource('volumes').then( function (resp) {
        context.commit('setVolumes', resp.data)
      })
    },

    getAnnotations (context) {
      api.listResource('annotations').then( function (resp) {
        context.commit('setAnnotations', resp.data)
      })
    },

    uploadData (context, dataLocation) {
      api.postResource('uploads', dataLocation).then( function (resp) {
        context.commit('updateStatus', resp.data)
	router.push('/')
      })
    },

  },

})



