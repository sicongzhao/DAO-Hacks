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
	<div class="flex h-12 justify-end w-10/12 mx-auto">
		<div class="flex-none flex w-112 justify-between mr-10 text-right items-end font-semibold text-gray-400">
			<div class="w-16" title="Total number of proposals.">Proposals</div>
			<div class="w-16" title="Total number of voters who at least voted for 1 proposal.">Voters</div>
			<div class="w-16" title="Total number of token holders.">Holders</div>
			<div class="w-16" title="GINI Coefficient, evaluates the gap of wealth.">GINI</div>
			<div class="w-16" title="Agreement Coefficient, evaluates how well a group agree with each other.">AC</div>
		</div>
	</div>
	<router-link :to="'/dao/'+dao['dao_id']" v-for="(dao, index) in filteredList" :key="index" @click="updateDAOIndex(index)">
		<div class="h-20 my-3 w-10/12 mx-auto shadow-[#106ae0] shadow-ct flex items-center">
		<!-- <div class="h-20 w-20 items-center"> -->
			<img class="w-16 h-16 ml-2 flex-none" :src="dao['dao_avatar']" :alt="dao['dao_des']">
			<!-- </div> -->
			<div class="flex-col text-left ml-3 w-2/5 flex-none">
				<div class="text-lg font-black">{{dao['dao_name']}}</div>
				<div class="text-sm font-bold text-gray-400" :title="dao['dao_des']">{{dao['dao_des'].substring(0, 200)}}</div>
			</div>
			<div class="flex-auto h-12 w-10"></div>
			<div class="flex-none flex w-112 justify-between mr-10 text-right">

				<div class="w-16 font-semibold" v-if="dao['total_proposals']!=''">{{ Number(dao['total_proposals']).toFixed(0)}}</div>
				<div class="w-16 font-semibold text-gray-300" v-else>N/A</div>

				<div class="w-16 font-semibold" v-if="dao['total_unique_voters']!=''">{{ Number(dao['total_unique_voters']).toFixed(0)}}</div>
				<div class="w-16 font-semibold text-gray-300" v-else>N/A</div>


				<div class="w-16 font-semibold" v-if="dao['total_holders']!=''">{{ dao['total_holders']}}</div>
				<div class="w-16 font-semibold text-gray-300" v-else>N/A</div>


				<div class="w-16 font-semibold" v-if="dao['gini']!=''">{{ Number(dao['gini']).toFixed(3)}}</div>
				<div class="w-16 font-semibold text-gray-300" v-else>N/A</div>
				
				<div class="w-16 font-semibold" v-if="dao['agreement_coefficient_mean']!=''">{{ Number(dao['agreement_coefficient_mean']).toFixed(3)}}</div>
				<div class="w-16 font-semibold text-gray-300" v-else>N/A</div>

			</div>
			
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
			'DAOPageData',
			'DAOIndex'
    ]),
		filteredList() {
      return this.DAOInfo.filter(dao => {
        return dao['dao_name'].toLowerCase().includes(this.search.toLowerCase())
      })
    }
  },
  methods: {
    goToDAOPage(index){
			console.log(index)
			this.DAOPageData = this.DAOInfo[index]
		},
		async updateDAOIndex(DAOIndex){
      await this.$store.dispatch('updateDAOIndex', DAOIndex)
    },
  },
  mounted (){
    console.log(this.DAOInfo.length)
  }
}
</script>
