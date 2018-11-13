import axios from '../axios'

export default class WishlistClient {
  constructor () {
    this.http = axios
  }
  getWishlists () {
    return this.http.get('wishlists').then(resp => resp.data)
      .catch(e => {
        if (e.response.status !== 401) {
          console.error(e)
        }
      })
  }

  getWishlist (wishlistId) {
    return this.http.get(`wishlists/${wishlistId}`).then(resp => resp.data)
  }

  addNewWishlist (wishlistName) {
    const wishlist = {
      name: wishlistName,
      cards: []
    }
    return this.http.post('wishlists', wishlist).then(resp => resp.data)
  }

  addCard (wishlistId, card) {
    return this.http.post(`wishlists/${wishlistId}/cards`, card
    ).then(resp => resp.data)
  }

  removeCard (wishlistId, cardId) {
    return this.http.delete(`wishlists/${wishlistId}/cards/${cardId}`
    ).then(resp => resp.data)
  }

  updateCard (wishlistId, card) {
    return this.http.put(`wishlists/${wishlistId}/cards/${card.id}`, card
    ).then(resp => resp.data)
  }
  removeWishlist (wishlistId) {
    return this.http.delete(`wishlists/${wishlistId}`).then(resp => resp.data)
  }
}
