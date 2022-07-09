import Vue from 'vue';
import Router from 'vue-router';
import LemonGame from './views/LemonGame.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
    routes: [
    {
      path: '/',
      name: 'lemon',
      component: LemonGame,
    },
  ],
});
