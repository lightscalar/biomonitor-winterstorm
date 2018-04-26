<template>

  <v-container>
    <v-layout>
      <v-flex xs6 offset-xs3>
        <v-card>
          <v-card-title>
            <h2>Upload Board Data</h2>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-form v-model="selectedCard">
              <v-select
                    :items="volumes"
                    v-model="sdVolume"
                    label="Select SD Card"
                    ></v-select>
                <v-select
                    :items="annotations"
                    v-model="annotationFile"
                    label="Select Annotation File"
                    ></v-select>
            </v-form>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions >
            <v-btn color='primary' @click.native='uploadData'>
              Upload Data
            </v-btn>
          </v-card-actions>

        </v-card>
      </v-flex>
    </v-layout>


    <v-dialog v-model="errorModal" max-width="290">
      <v-card>
        <v-card-title class="headline" color='red darken-2'>
          Oops...
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          You must specify the location of both the SD card and the associated
          annotation file.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1"
                 flat="flat" @click.native="errorModal=false">
            Okay, Sorry
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>

</template>

<script>
// import Component from "../component_location"

  export default {

    components: {},

    props: [],

    data () {
      return {
        selectedCard: '',
        sdVolume:'',
        annotationFile: '',
        errorModal: false
      }
    },

    methods: {

      uploadData () {
        // this.$store.dispatch('uploadData')
        if (this.sdVolume==''||this.annotationFile=='') {
          this.errorModal=true
        } else {
          this.$store.dispatch('uploadData', {
            volume: this.sdVolume,
            annotationFile: this.annotationFile
          })
        }
      }

    },

    computed: {

      volumes() {
        return this.$store.state.volumes
      },

      annotations() {
        return this.$store.state.annotations
      }

    },

    mounted () {

      this.$store.dispatch('getVolumes')
      this.$store.dispatch('getAnnotations')

    }

  }

</script>

<style>

</style>
