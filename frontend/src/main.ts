import Vue from 'vue';
import VueCookies from 'vue-cookies';

import Buefy from 'buefy';
import 'buefy/dist/buefy.css';

import App from './App.vue';
import router from './router';

import './game.css';

Vue.use(VueCookies);
Vue.use(Buefy);

Vue.config.productionTip = false;

Vue.prototype.$cookies.config(Infinity);

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
