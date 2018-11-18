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
    <b-form-file v-model="file" :state="Boolean(file)" placeholder="Choose a file..."></b-form-file>
  </b-modal>
</template>

<script>
export default {
  data () {
    return {
      file: null,
      errorMessage: null,
      fileReader: null,
      content: null
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
      this.content = this.fileReader.result
      console.log(this.content)
    }
  }
}
</script>

<style lang="css">
</style>
