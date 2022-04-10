<template>
  <div class="w-full">
		
		<div class="w-full h-60 bg-cover bg-center" :style="{ backgroundImage: 'url(' + DAOPageData['dao_cover'] + ')' }"></div>
		<div class="h-12 flex mt-10">
			<div class="flex items-center text-4xl font-black">
				{{DAOPageData['dao_name']}}
			</div>
			<div class="w-12 h-12 ml-3 shadow-[#106ae0] shadow-ct flex item-center">
				<img class="w-10 h-10 m-auto" :src="DAOPageData['dao_avatar']" alt="">
			</div>
		</div>

		<div class="w-full flex">
				<div class="flex-col flex-auto flex flex-auto max-w-4xl text-lg pr-16">
					<div class="text-left " v-html="DAOPageData['dao_full_des']"></div>
				</div>

				<div class="max-w-xl min-w-fit flex-none flex-col w-128 mt-5">
					<div class="w-full shadow-[#106ae0] shadow-ct flex-col item-center px-6 pb-6">
						<h4 class="m-0 text-left">Summay</h4>
						<div class="w-full flex">
							<div class="w-24 h-24 bg-gray-50 flex-auto flex-col pt-4">
								<div class="leading-none text-sm mb-1">Total<br>Proposals</div>
								<div class="font-semibold text-2xl " v-if="DAOPageData['total_proposals']!=''">{{ Number(DAOPageData['total_proposals']).toFixed(0)}}</div>
								<div class="font-semibold text-gray-300 text-2xl" v-else>N/A</div>
							</div>
							<div class="w-24 h-24 bg-gray-50 flex-auto flex-col pt-4">
								<div class="leading-none  text-sm mb-1">Total<br>Votes</div>
								<div class="font-semibold text-2xl " v-if="DAOPageData['total_votes']!=''">{{ Number(DAOPageData['total_votes']).toFixed(0)}}</div>
								<div class="font-semibold text-gray-300 text-2xl " v-else>N/A</div>
							</div>
							<div class="w-24 h-24 bg-gray-50 flex-auto flex-col pt-4">
								<div class="leading-none  text-sm mb-1">Total<br>Voters</div>
								<div class="font-semibold text-2xl " v-if="DAOPageData['total_unique_voters']!=''">{{ Number(DAOPageData['total_unique_voters']).toFixed(0)}}</div>
								<div class="font-semibold text-gray-300 text-2xl " v-else>N/A</div>
							</div>
							<div class="w-24 h-24 bg-gray-50 flex-auto flex-col pt-4">
								<div class="leading-none  text-sm mb-1">Avg<br>Votes</div>
								<div class="font-semibold text-2xl " v-if="DAOPageData['total_proposals']!=''">{{ Number(DAOPageData['votes_per_member']).toFixed(2)}}</div>
								<div class="font-semibold text-gray-300 text-2xl " v-else>N/A</div>
							</div>
						</div>

						<div class="w-full flex">
							<div class="w-24 h-24 bg-gray-50 flex-auto flex-col pt-4">
								<div class="leading-none text-sm mb-1">Gini<br>Coefficient</div>
								<div class="font-semibold text-2xl " v-if="DAOPageData['gini']!=''">{{ Number(DAOPageData['gini']).toFixed(3)}}</div>
								<div class="font-semibold text-gray-300 text-2xl" v-else>N/A</div>
							</div>
							
							<div class="w-24 h-24 bg-gray-50 flex-auto flex-col pt-4">
								<div class="leading-none  text-sm mb-1">Token<br>Rate</div>
								<div class="font-semibold text-2xl " v-if="DAOPageData['token_rate_mean']!=''">{{ Number(DAOPageData['token_rate_mean']).toFixed(3)}}</div>
								<div class="font-semibold text-gray-300 text-2xl " v-else>N/A</div>
							</div>

							<div class="w-24 h-24 bg-gray-50 flex-auto flex-col pt-4">
								<div class="leading-none  text-sm mb-1">Voter<br>Rate</div>
								<div class="font-semibold text-2xl " v-if="DAOPageData['voter_rate_mean']!=''">{{ Number(DAOPageData['voter_rate_mean']).toFixed(3)}}</div>
								<div class="font-semibold text-gray-300 text-2xl " v-else>N/A</div>
							</div>

							<div class="w-24 h-24 bg-gray-50 flex-auto flex-col pt-4">
								<div class="leading-none  text-sm mb-1">Agreement<br>Coefficient</div>
								<div class="font-semibold text-2xl " v-if="DAOPageData['agreement_coefficient_mean']!=''">{{ Number(DAOPageData['agreement_coefficient_mean']).toFixed(3)}}</div>
								<div class="font-semibold text-gray-300 text-2xl " v-else>N/A</div>
							</div>
						</div>
					</div>

					<div class="w-full shadow-[#106ae0] shadow-ct flex-col px-6 pb-4 mt-6">
						<h4 class="m-0 text-left">Tags</h4>
						<div class="flex flex-wrap">
							<div class="px-2 h-8 bg-indigo-500 text-white font-bold flex items-center mr-2 mb-2" v-if="DAOPageData['gini']!=''&&Number(DAOPageData['gini'] < 0.9)">Relative Equal!</div>
							<div class="px-2 h-8 bg-yellow-500 text-white font-bold flex items-center mr-2 mb-2" v-if="DAOPageData['token_rate_mean']!=''&&Number(DAOPageData['token_rate_mean'] > 0.7)&&DAOPageData['voter_rate_mean']!=''&&Number(DAOPageData['voter_rate_mean'] > 0.7)">Coincide!</div>
							<div class="px-2 h-8 bg-green-500 text-white font-bold flex items-center mr-2 mb-2" v-if="DAOPageData['agreement_coefficient_mean']!=''&&Number(DAOPageData['agreement_coefficient_mean'] < 1.2)">Members Win!</div>
							<div class="px-2 h-8 bg-sec-color-1 text-white font-bold flex items-center mr-2 mb-2" v-if="DAOPageData['agreement_coefficient_mean']!=''&&Number(DAOPageData['agreement_coefficient_mean'] > 1.5)">Tokens Win!</div>
							<div class="px-2 h-8 bg-theme-color-1 text-white font-bold flex items-center mr-2 mb-2" v-if="DAOPageData['voter_rate_mean']!='' && Number(DAOPageData['votes_per_member'] > 4)">Active Community!</div>
						</div>
						
					</div>

					<div class="w-full shadow-[#106ae0] shadow-ct flex-col items-center px-6 mt-6" v-if="histData != null">
						<h4 class="m-0 text-left">Token Distribution</h4>
						<!-- {{typeof(members)}}{{members['token_dist_1']}} -->
						
						<HistogramSlider
							style="margin: 0 auto"
							:width="460"
							:bar-height="160"
							:data="histData"
							:drag-interval="true"
							:force-edges="false"
							:colors="['#4facfe', '#00f2fe']"
							:min="1"
							:max="10000"
							:grid-num="4"
							:bar-radius="2"
						/>
						<div class="h-6"></div>
					</div>

					<div class="w-full shadow-[#106ae0] shadow-ct flex-col item-center px-6 pb-6 mt-6">
						<h4 class="m-0 text-left">Information</h4>
						<div class="flex justify-between items-center py-3" v-if="DAOPageData['treasury_addr_1'] != ''">
							<div class="font-medium">Treasury</div>
							<div class="">{{DAOPageData['treasury_addr_1']}}</div>
						</div>
						
						<div class="flex justify-between items-center py-3" v-if="DAOPageData['treasury_addr_2'] != ''">
							<div class="font-medium">Treasury</div>
							<div class="">{{DAOPageData['treasury_addr_2']}}</div>
						</div>

						<div class="flex justify-between items-center py-3" v-if="DAOPageData['treasury_addr_3'] != ''">
							<div class="font-medium">Treasury</div>
							<div class="">{{DAOPageData['treasury_addr_3']}}</div>
						</div>

						<div class="flex justify-between items-center py-3" v-if="DAOPageData['governance_type'] != ''">
							<div class="font-medium">Governance Type</div>
							<div class="">{{DAOPageData['governance_type']}}</div>
						</div>

						<div class="flex justify-between items-center py-3" v-if="DAOPageData['governance_url'] != ''">
							<div class="font-medium">Governance URL</div>
							<a class="underline" :href="DAOPageData['governance_url']" target="_blank">{{DAOPageData['governance_addr']}}</a>
						</div>

						<div class="flex justify-between items-center py-3" v-if="DAOPageData['token_address'] != ''">
							<div class="font-medium">Token</div>
							<div class="">{{DAOPageData['token_address']}}</div>
						</div>

						<div class="flex justify-between items-center py-3" v-if="DAOPageData['token_scan'] != ''">
							<div class="font-medium">Token Scan</div>
							<a class="underline" :href="DAOPageData['token_scan']" target="_blank">link</a>
						</div>

						<div class="flex justify-between items-center py-3" v-if="DAOPageData['total_supply'] != ''">
							<div class="font-medium">Total Supply</div>
							<div class="">{{DAOPageData['total_supply']}}</div>
						</div>

					</div>
				</div>
			</div>
	</div>


</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'DAO',
	data () {
    return {
      members: '',
			// data: data,
			histData: null,
			maxHist: null,
    }
  },
	components: {
    // HistogramSlider
  },
  computed: {
    ...mapGetters([
      'DAOInfo',
			'DAOIndex'
    ]),
		DAOPageData () {
			return this.DAOInfo[this.DAOIndex]
			// return this.DAOInfo[3]
		},
		
  },
  methods: {
    getDAOId(){
        // console.log(this.$route.params.daoid)
				console.log(this.DAOIndex)
    },
		async getMemberDetail(dao_id) {
			let that = this
      let url = 'https://ru355oakp6.execute-api.us-west-2.amazonaws.com/default/daohack-members?dao_id=' + dao_id
      await fetch(url).then(function(response) {
        return response.json()
      }).then(function(data) {
        console.log(data)
				that.members = data.data[0]
        // commit("setDAOInfo", data.data) 
				that.histData = JSON.parse('['+data.data[0]['token_dist_1'].slice(1, -1)+']')
				that.histData.push(0)
				that.maxHist = Math.floor(Math.max(that.histData)*0.01)
				console.log(that.histData)
      });
    },
  },
	mounted () {
		// this.DAOPageData = this.DAOInfo[this.DAOIndex]
		
		// for dev purpose. delete before launch.
		// this.DAOPageData = this.DAOInfo[this.$route.params.daoid - 1]

		console.log(this.DAOPageData)
		this.getMemberDetail(this.$route.params.daoid)
		
		
	}
}
</script>

<style>
h2 {
	font-size: 1.25rem; /* 20px */
	line-height: 1.75rem; /* 28px */
	font-weight: 900;
	margin: 20px 0 6px 0;
	line-height: 60px;
}

h4 {
	font-size: 1.25rem; /* 20px */
	line-height: 1.75rem; /* 28px */
	font-weight: 900;
	line-height: 60px;
}

h3 {
	font-size: 1.25rem; /* 20px */
	line-height: 1.75rem; /* 28px */
	font-weight: 700;
	margin: 2px 0 6px 0;
	line-height: 48px;
}

p, li, ul {
	margin: 0 0 6px 0;
	line-height: 28px;
}
blockquote {
  background: #f9f9f9;
  border-left: 3px solid #000;
  margin: 1.5em 0px;
  padding: 0.5em 10px 0.5em 20px;
  quotes: "\201C""\201D""\2018""\2019";
}

blockquote p {
  display: inline;
	font-size: 1rem; /* 20px */
	line-height: 20px;
}
</style>
