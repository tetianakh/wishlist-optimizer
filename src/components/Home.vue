<template>
<page>
  <div class="row">
    <div class="col-lg-8 text">
      <h3>About VampiricTutor.com</h3>
      <p>On VampiricTutor.com you can find the cheapest offers for Magic, The Gathering™ cards on <a href="https://www.cardmarket.com/en/Magic" target="_blank">Cardmarket.eu</a>.</p>
      <p>First add the cards you want to buy to a wishlist (you can add the cards individually or upload a .txt file with a deck list), then click the "Get Prices" button and wait for the program to fetch data from <a href="https://www.cardmarket.com/en/Magic" target="_blank">Cardmarket.eu</a>.  Once the calculation is finished, you'll get top 10 sellers with the cheapest prices for the cards in your wishlist (without a shipping cost).</p>
      <p>If you sign in to Vampiric Tutor with your Google account, you'll be able to save multiple wishlists for future use.</p>
      <p>VampiricTutor.com was created by <a href="https://github.com/tetianakh" target="_blank">tetianakh</a> and <a href="https://www.cardmarket.com/en/Magic/Users/SknerusMcKwacz">SknerusMcKwacz</a> who were looking for a way to get the most out of <a href="https://www.cardmarket.com/en/Magic" target="_blank">Cardmarket.eu</a>. It is free of charge. If you find it useful, please consider supporting us by making a <a href="https://paypal.me/vampirictutor" target="_blank">donation via PayPal</a>.</p>
      <p>This web site is opensourced <a href="https://github.com/tetianakh/wishlist-optimizer">on github</a>. Feature requests and bug reports are welcome.</p>
    </div>

    <div class="col-lg-4">
      <h3>Your Wishlists</h3>

      <div class="row centered">
          <b-button class="margin" size="sm" variant="success" @click="addNewWishlist">
            {{ newWishlistButtonName }}</b-button>
      </div>

      <table class="table table-hover">
        <tbody>
          <tr v-for="(wishlist, idx) in wishlists" :key="wishlist.id">
            <td @click="openWishlist(wishlist.id)" class="hoverable">{{ wishlist.name }}</td>
            <td><font-awesome-icon icon="trash" @click="deleteWishlist(wishlist.id, idx)" class="hoverable"/></td>
          </tr>
        </tbody>
      </table>

    </div>
  </div>
</page>
</template>

<script>
import WishlistClient from '../clients/WishlistClient'
import Page from './Page'
import tokenStore from '../store/token'
import draftStore from '../store/draft'

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
  computed: {
    authenticated () {
      return tokenStore.isAuthenticated()
    },
    newWishlistButtonName () {
      if (draftStore.hasDraft) {
        return "Go to Unsaved Wishlist"
      }
      return "Add New Wishlist"
    }
  },
  mounted () {
    if (this.authenticated) {
      this.loadWishlists()
    }
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
      this.$router.push({ name: 'Draft' })
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
  margin-top: 15px;
}

h2 {
  margin-bottom: 20px;
}

.text {
  text-align: justify;
}

</style>
