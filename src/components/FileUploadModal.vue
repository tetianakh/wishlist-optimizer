<template lang="html">
  <b-modal id="uploadFileModal" ok-title="Upload" @ok="handleFileUpload">
    <template slot="modal-title">
      Select a file to upload:
    </template>
    <b-alert variant="danger"
         dismissible
         :show="errorMessage !== null"
         @dismissed="errorMessage=null">
        {{ errorMessage }}
    </b-alert>
    <b-form-file v-model="file" :state="Boolean(file)" accept=".txt" placeholder="Choose a file..."></b-form-file>
    <b-form-checkbox v-model="removeBasics" class="margin">Remove basic lands</b-form-checkbox>
  </b-modal>
</template>

<script>
import { NEW_CARDS } from '../events'

const BASICS = ['mountain', 'island', 'plains', 'swamp', 'forest']

export default {
  data () {
    return {
      file: null,
      errorMessage: null,
      fileReader: null,
      removeBasics: true
    }
  },
  methods: {
    handleFileUpload (event) {
      if (!this.file) {
        event.preventDefault()
        this.errorMessage = 'Please select a file to upload'
        return
      }
      console.log(this.file)
      this.fileReader = new FileReader()
      this.fileReader.onloadend = this.handleFileRead
      this.fileReader.readAsText(this.file)
    },
    handleFileRead (e) {
      const content = this.fileReader.result
      const result = []
      if (!content) {
        return
      }
      for (let line of content.split('\n')) {
        line = line.split(' ')
        const quantity = parseInt(line[0].trim())
        // quantity cannot be 0 or NaN
        if (!quantity) {
          continue
        }
        // make sure there are no multiple spaces between words
        const name = line.slice(1).map(word => word.trim()).join(' ')
        if (BASICS.includes(name.toLowerCase())) {
          continue
        }
        const card = {
          quantity: quantity,
          name: name,
          languages: []
        }
        result.push(card)
      }
      if (result.length > 0) {
        this.$emit(NEW_CARDS, result)
      }
    }
  }
}
</script>

<style lang="css">
</style>
