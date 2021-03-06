// store.js example

import { createStore } from "vuex" 
// import { ethers } from "ethers";

const store = createStore({
  state:{
    account: null,
    error: null,
    DAOInfo: [],
    DAOPageData: [],
    DAOIndex: null,
  },
  getters: {
    account: (state) => state.account,
    error: (state) => state.error,
    DAOInfo: (state) => state.DAOInfo,
    DAOIndex: (state) => state.DAOIndex,
    DAOPageData: (state) => state.DAOPageData,
  },
  mutations: {
    setAccount(state, account) {
       state.account = account
    },
    setError(state, error) {
       state.error = error
    },
    setDAOInfo(state, DAOInfo) {
      state.DAOInfo = DAOInfo
    },
    setDAOPageData(state, DAOPageData) {
      state.DAOPageData = DAOPageData
    },
    setDAOIndex(state, DAOIndex) {
      state.DAOIndex = DAOIndex
    },
  },
  actions: {
    async connect({commit, dispatch}, connect) {
      try {
        /**
        MetaMask injects a global API into websites visited by its users at window.ethereum.
        This part use argument destructuring to verify the existence of window.ethereum, thus check the connection status
        **/ 
        const { ethereum } = window;
        console.log(ethereum)
        if (!ethereum) {
          commit("setError", "Metamask is not installed")
          return
        }
        if (!(await dispatch('checkIfConnected')) && connect) {
          await dispatch('requestAccess')
        }
        await dispatch('checkNetwork')
      } catch (error) {
        commit('setError', 'Account request refused.')
      }
    },
    async checkNetwork({commit, dispatch}) {
      let chainId = await window.ethereum.request({ method: "eth_chainId"})
      console.log('Chain Id: ', chainId)
      const mumbaiChainId = '0x13881'
      if (chainId !== mumbaiChainId) {
        if (!(await dispatch('switchNetwork'))) {
          commit('setError', 'You are not connected to the Polygon Mumbai Network!')
        }
      }
    },
    async switchNetwork() {
      try {
        await window.ethereum.request({
          method: 'wallet_switchEthereumChain',
          params: [{chainId: '0x13881'}]
        })
        return 1
      } catch (switchError) {
        return 0
      }
    },
    async checkIfConnected({commit}) {
      // const {ethereum} = window
      const accounts = await window.ethereum.request({ method: 'eth_accounts'})
      if (accounts.length !== 0) {
        commit('setAccount', accounts[0])
        console.log(accounts[0])
        return 1
      } else {
        return 0
      }
    },
    async requestAccess({commit}) {
      // const {ethereum} = window
      const accounts = await window.ethereum.request({
        method: 'eth_requestAccounts'
      })
      commit('setAccount', accounts[0])
    },

    async getDAOInfo({commit}) {
      let url = 'https://ru355oakp6.execute-api.us-west-2.amazonaws.com/default/daohack-daoinfo'
      await fetch(url).then(function(response) {
        return response.json()
      }).then(function(data) {
        console.log(data)
        let daoinfo = []
        data.data.forEach(ele => {
          if (ele['total_holders']!='') {
            daoinfo.push(ele)
          }
          
        });
        commit("setDAOInfo", daoinfo) 
      });
    },

    async updateDAOIndex({commit},DAOIndex){
      commit("setDAOIndex", DAOIndex) 
    }
  }
})

export default store