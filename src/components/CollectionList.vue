<template>

<v-container grid-list-md text-xs-center>
    <v-layout row wrap>
      <v-flex xs12>
        <v-card>
          <v-card-title><h2>Collection Data</h2></v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            No Data Sets Available
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
</v-container>

</template>

<script>
  // import Component from "../component_location"

  export default {

    components: {},

    props: [],

    data () {
      return {

      }
    },

    methods: {

    },

    computed: {

      collections () {
        console.log(this.$store.state.collections)
        return this.$store.state.collections
      }

    },

    mounted () {

      this.$store.dispatch('getCollections')

    }
  }

</script>

<style>

</style>
