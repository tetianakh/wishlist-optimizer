import LanguagesClient from '../clients/LanguagesClient'

const languagesLoader = {
  created () {
    if (this.$store.availableLanguages && this.$store.availableLanguages.length > 0) {
      return
    }
    new LanguagesClient().getAvailableLanguages().then(languages => {
      this.$store.commit('setLanguages', languages)
    })
  }
}

export default languagesLoader
