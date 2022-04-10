<template>
  <div id="search-bar" class="bg-blue-50 py-12">
    <!-- <div> -->
			<!-- <label for="search" class="block text-sm font-medium text-gray-700">Quick search</label> -->
			<div class="mt-1 relative flex items-center w-10/12 mx-auto">
			<input type="text" name="search" id="search" v-model="search" class="h-12 shadow-sm block w-full pr-12 sm:text-sm border-black border-2 px-6" placeholder="Quick Search"/>
			<div class="absolute inset-y-0 right-0 flex py-1.5 pr-1.5">
					<kbd class="inline-flex items-center border border-gray-200 rounded px-2 text-sm font-sans font-medium text-gray-400"> ⌘K </kbd>
			</div>
			</div>
    </div>
	<!-- </div> -->
	<router-link :to="'/dao/'+i[0]" v-for="i in filteredList" :key="i[0]">
		<div>
		{{i[0]}}
		</div>
	</router-link>
	
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Home',
  data () {
    return {
      search: '',
    }
  },
  computed: {
    ...mapGetters([
      'DAOInfo',
    ]),
		filteredList() {
      return this.DAOInfo.filter(DAO => {
        return DAO[0].toLowerCase().includes(this.search.toLowerCase())
      })
    }
  },
  methods: {
    
  },
  mounted (){
    console.log(this.DAOInfo.length)
  }
}
</script>
