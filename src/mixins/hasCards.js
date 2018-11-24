var hasCards = {
  computed: {
    hasCards () {
      return this.wishlist && this.wishlist.cards && this.wishlist.cards.length > 0
    }
  }
}

export default hasCards
