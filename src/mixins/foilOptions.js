var foilOptions = {
  data () {
    return {
      foilOptions: [
        { value: true, text: 'yes' },
        { value: false, text: 'no' },
        { value: null, text: 'any' }
      ]
    }
  },
  filters: {
    humanize (value) {
      if (value === true) return 'yes'
      if (value === false) return 'no'
      return 'any'
    }
  }
}

export default foilOptions
