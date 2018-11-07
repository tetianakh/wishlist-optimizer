<template lang="html">
  <table class='table table-hover'>
    <thead>
      <th>Seller Id</th>
      <th>Seller Name</th>
      <th>Seller Username</th>
      <th>Has # cards</th>
      <th>Total price</th>
    </thead>
    <tbody>
      <tr v-for="item in pricing" :key="item.seller.idUser">
        <td>{{ item.seller.idUser }}</td>
        <td>{{ item.seller.name.lastName ? item.seller.name.firstName  + ' ' + item.seller.name.lastName : item.seller.name.firstName }}</td>
        <td>{{ item.seller.username }}</td>
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
