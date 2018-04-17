<template>
  <v-container>
    <v-layout>
      <v-flex xs6 offset-xs3>
        <v-card>
          <v-card-title>
            <h2>Configure SD Card</h2>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-form v-model="valid">
              <v-text-field
                    label="Collection ID"
                    v-model="collectionID"
                    required
                    type='number'
                    ></v-text-field>
                <v-select
                    :items="volumes"
                    v-model="sdVolume"
                    label="Select SD Card"
                    ></v-select>
                  <v-select
                    :items="validHours"
                    v-model="collectionDuration"
                    label="Maximum Collection Duration (hours)"
                    ></v-select>
            </v-form>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-dialog v-model="dialog" persistent max-width="290">
              <v-btn color="red darken-4 white--text" dark slot="activator">
                Configure SD Card
              </v-btn>
              <v-card>
                <v-card-title class="headline">Configure SD Card?</v-card-title>
                <v-card-text>This will delete all data stored on the SD card located at
                  <b>{{sdVolume}}</b>. This action cannot be undone.</v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="red darken-1" flat @click.native="dialog = false">Cancel</v-btn>
                  <v-btn color="red darken-1" flat @click.native="configure()">Configure</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-card-actions>
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
        valid: true,
        collectionID: moment().format('MMDDYYYYHHmm'),
        collectionDuration: 6,
        sdVolume: '',
        validHours: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        dialog: false

      }
    },

    methods: {

      configure() {
        this.dialog = false
        console.log('Configuring card now.')
        var config = {id: this.collectionID, volume: this.sdVolume,
          duration: this.collectionDuration}
        this.$store.dispatch('configureCard', config)
        this.$router.push('/')
      }

    },

    computed: {

      volumes() {
        return this.$store.state.volumes
      }

    },

    mounted () {

      this.$store.dispatch('getVolumes')

    }
  }

</script>

<style>

</style>
