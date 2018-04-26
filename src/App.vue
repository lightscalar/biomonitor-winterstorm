<template>
  <v-app id="app">
    <v-toolbar app flat color='grey darken-4'>
      <router-link :to="{name: 'collection.index'}">
        <img src='static/imgs/heart-logo@2x.png' height=100 class='mt-5'>
      </router-link>
      <v-toolbar-title v-text='title' class='logo'></v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items class="hidden-sm-and-down">
        <v-tooltip bottom color='black'>
          <v-btn flat color='white' slot='activator' :to="'/'">
            <v-icon medium class='mr-1'>storage</v-icon>Collection Data
          </v-btn>
          <span>Review Collection Data</span>
        </v-tooltip>
        <v-tooltip bottom color='black'>
          <v-btn flat color='white' slot='activator' to="uploads">
            <v-icon medium class='mr-1'>file_upload</v-icon>Upload
          </v-btn>
          <span>Upload Collection Data from a Biomonitor SD Card</span>
        </v-tooltip>
        <v-tooltip bottom color='black'>
          <v-btn flat color='white' slot='activator' :to="'new-collection'">
            <v-icon medium class='mr-1'>add_circle</v-icon>New Collection
          </v-btn>
          <span>Configure SD Card for Collection</span>
        </v-tooltip>
      </v-toolbar-items>
    </v-toolbar>
    <v-content>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-content>
    <v-footer app></v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'App',

  data () {
    return {
      title: 'new vital signs'
    }
  }

  }
</script>

<style>
.logo {
    letter-spacing: 1em;
    color: #ffffff;
    font-family: 'PT Sans';
    font-weight: bold;
}
</style>

