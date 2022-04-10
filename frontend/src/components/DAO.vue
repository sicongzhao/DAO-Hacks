<template>
  <h1 @click="getDAOId">The user is {{ DAOPageData }}</h1>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'DAO',
	data () {
    return {
      DAOPageData: '',
    }
  },
  computed: {
    ...mapGetters([
      'DAOInfo',
			'DAOIndex'
    ]),
  },
  methods: {
    getDAOId(){
        // console.log(this.$route.params.daoid)
				console.log(this.DAOIndex)
    }
  },
	mounted () {
		this.DAOPageData = this.DAOInfo[this.DAOIndex]
	}
}
</script>
