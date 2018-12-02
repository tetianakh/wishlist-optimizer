var conditionsOptions = {
  data () {
    return {
      conditionOptions: [
        { value: 'MT', text: 'Mint' },
        { value: 'NM', text: 'Near Mint' },
        { value: 'EX', text: 'Excellent' },
        { value: 'GD', text: 'Good' },
        { value: 'LP', text: 'Light Played' },
        { value: 'PL', text: 'Played' },
        { value: 'PO', text: 'Poor' }
      ]
    }
  },
  methods: {
    humanizeCondition (value) {
      if (value === null) {
        return null
      }
      for (let condition of this.conditionOptions) {
        if (condition.value === value) {
          return condition.text
        }
      }
      console.warn('Unknown condition: ', value)
      return null
    }
  }
}

export default conditionsOptions
