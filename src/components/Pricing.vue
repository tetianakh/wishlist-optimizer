<template lang="html">
  <table class='table table-hover'>
    <thead>
      <th>Seller Username</th>
      <th>Has # cards</th>
      <th>Total price</th>
    </thead>
    <tbody>
      <tr v-for="item in pricing" :key="item.seller_id">
        <td><a :href="item.seller_url" target="_blank">{{ item.seller_username }}</a></td>
        <td>{{ item.total_count }}</td>
        <td>{{ item.total_price }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  props: ['pricing']
}
</script>

<style lang="css">
</style>
