<template>
<page>
  <table class="table table-hover">
    <h1>Wishlists</h1>

    <div class="row centered">
      <div class="centered col-lg-6">

        <b-form inline @submit.prevent="addNewWishlist">
          <b-input class="mb-2 mr-sm-2 mb-sm-0"
            placeholder="Wishlist Name"
            v-model="newWishlistName"/>
          <button class="btn btn-success" type="submit">
      Add new wishlist</button>
        </b-form>

      </div>
    </div>

    <div class="row centered">
      <div class="col-lg-6 centered">
        <table>
          <tbody>
            <tr v-for="(wishlist, idx) in wishlists" :key="wishlist.id">
              <td @click="openWishlist(wishlist.id)" class="hoverable">{{ wishlist.name }}</td>
              <td><font-awesome-icon icon="trash" @click="deleteWishlist(wishlist.id, idx)" class="hoverable"/></td>
            </tr>
          </tbody>
        </table>
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
    this.loadWishlists()
  },
  methods: {
    loadWishlists () {
      this.client.getWishlists().then(resp => {
        if (resp) {
          this.wishlists = resp.wishlists
        }
      })
    },
    openWishlist (wishlistId) {
      this.$router.push({
        name: 'Wishlist',
        params: {
          id: wishlistId
        }
      })
    },
    addNewWishlist () {
      this.client.addNewWishlist(this.newWishlistName).then(resp => {
        this.$router.push({
          name: 'Wishlist',
          params: {
            id: resp.wishlist.id
          }
        })
      })
    },
    deleteWishlist (wishlistId, idx) {
      this.client.removeWishlist(wishlistId).then(() => {
        this.wishlists.splice(idx, 1)
      })
    }
  }
}
</script>
<style>

table {
  width:70%;
  margin-top: 30px;
}

</style>
