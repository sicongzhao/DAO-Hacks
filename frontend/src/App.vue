<template>
  <div class="bg-gray-100 min-h-screen max-h-screen overflow-y-auto">
    <div class="flex-col max-w-7xl mx-auto bg-white">
      <div id="header" class="flex justify-between content-center items-center py-6">
        <router-link to="/">
          <div class="flex text-2xl font-black ">DAOHUBS</div>
        </router-link>
        <div class="flex flex-wrap">
          <sw-auth
            partner-key="055fe390a0fb1cf439023af499ce015dda50421f"
            use-dev="true"
            id="root"
            use-button-options="true"
          ></sw-auth>
        </div>
      </div>
      <router-view />
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { InitSwAuth } from "@skill-wallet/auth";
InitSwAuth();

export default {
  name: 'App',
  
  components: {
    // HelloWorld
  },
  computed: {
    ...mapGetters([
      'DAOInfo',
    ]),
  },
  methods: {
    userId(){
      const sw = JSON.parse(sessionStorage.getItem('skillWallet') || '{}');
      console.log(sw)
    },
    async getDAOInfo() {
      await this.$store.dispatch("getDAOInfo");
    },
  },
  mounted (){
    window.addEventListener('onSkillwalletLogin',this.userId)
    this.getDAOInfo()
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
}
</style>
