<template>

  <v-container grid-list-md text-xs-center>
    <v-layout row wrap>
      <v-flex xs12>
        <v-card>

          <v-card-title><h2>Collection Data</h2></v-card-title>
          <v-divider></v-divider>

          <v-data-table
            :headers="headers"
            :items="collections"
            hide-actions
            class="elevation-1"
            >
            <template slot="items" slot-scope="props">
              <td class="text-xs-left">{{ props.item.id }}</td>
              <td class="text-xs-left">{{ props.item.uploadedAt }}</td>
              <td class="text-xs-left">{{ props.item.duration }}</td>
              <td class="text-xs-left">
                <v-btn :href='link(props.item)'>
                  <v-icon>
                    file_download
                  </v-icon>
                  Download</v-btn>
              </td>
            </template>
          </v-data-table>


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
        headers: [
          {text: 'Collection ID', name:'id', sortable: false, align:'left'},
          {text: 'Uploaded At', name:'uploadedAt', sortable: false},
          {text: 'Duration', name:'duration', sortable: false},
          {text: '', name:'link', sortable: false},
        ],
      }
    },

    methods: {

      link (item) {
        return 'static/zipped/'+item.id+'.zip'
      }

    },

    computed: {

      collections () {
        console.log(this.$store.state.collections)
        return this.$store.state.collections
      },


    },

    mounted () {

      this.$store.dispatch('getCollections')

    }
  }

</script>

<style>

</style>
