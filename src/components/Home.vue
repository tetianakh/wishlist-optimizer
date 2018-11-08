<template>
<page>
  <table class="table table-hover">
    <h1>Wishlists</h1>

    <div class="row">
      <div class="col-lg-4 col-centered">
        <b-form inline>
          <b-input class="mb-2 mr-sm-2 mb-sm-0" placeholder="Wishlist Name" v-model="newWishlistName" />
          <button type="button" class="btn btn-success" @click="addNewWishlist">
      Add new wishlist</button>
        </b-form>
      </div>
    </div>

    <div class="row">
      <div class="col-lg-5 col-centered">

        <ul class="list-group list-group-flush list-group-item-action ">
          <li v-for="wishlist in wishlists" :key="wishlist.id" @click="openWishlist(wishlist.id)" class="list-group-item list-group-item-action hoverable">
            {{ wishlist.name }}</li>
        </ul>
      </div>
    </div>
  </table>
</page>
</template>

<script>
import WishlistClient from '../clients/WishlistClient'
import Page from './Page'

export default {
  components: {
    Page
  },
  data () {
    return {
      wishlists: [],
      client: new WishlistClient(),
      newWishlistName: null
    }
  },
  mounted () {
    this.client.getWishlists().then(resp => {
      this.wishlists = resp.wishlists
    }).catch(e => console.error(e))
  },
  methods: {
    openWishlist (wishlistId) {
      this.$router.push({
        name: 'wishlist',
        params: {
          id: wishlistId
        }
      })
    },
    addNewWishlist () {
      this.client.addNewWishlist(this.newWishlistName).then(resp => {
        this.$router.push({
          name: 'wishlist',
          params: {
            id: resp.wishlist.id
          }
        })
      })
    }
  }
}
</script>
<style>
.col-centered {
  margin: 10px auto;
  float: none;
}
</style>
