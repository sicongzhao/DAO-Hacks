<template>
  <h1 @click="getDAOId">The user is {{ $route.params.daoid }}</h1>
</template>

<script>
export default {
  name: 'DAO',
  methods: {
    getDAOId(){
        console.log(this.$route.params.daoid)
    }
  }
}
</script>
