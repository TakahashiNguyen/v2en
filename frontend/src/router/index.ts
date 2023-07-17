import {
  createMemoryHistory,
  createRouter,
  createWebHashHistory,
  createWebHistory,
} from 'vue-router';
import routes from './routes';
import { TOKEN_MUTATION, graphqlUrl } from 'src/graphql';
import { cache, useMutation, fetch, createClient } from 'villus';

const createHistory = process.env.SERVER
  ? createMemoryHistory
  : process.env.VUE_ROUTER_MODE === 'history'
  ? createWebHistory
  : createWebHashHistory;

const router = createRouter({
  scrollBehavior: () => ({ left: 0, top: 0 }),
  routes,
  history: createHistory(
    process.env.MODE === 'ssr' ? void 0 : process.env.VUE_ROUTER_BASE
  ),
});

export const userMutation = async (token: string | null) => {
  const { execute } = useMutation(TOKEN_MUTATION, {
    client: createClient({
      url: graphqlUrl,
      use: [cache(), fetch()],
    }),
  });
  try {
    if (!token) return '';
    const response = await execute({ token: token });
    return response.data.checkToken;
  } catch (error) {
    return '';
  }
};

router.beforeEach(async (to, from, next) => {
  const isAuthenticated = await userMutation(localStorage.getItem('token'));

  if (to.meta.requiresAuth && !isAuthenticated) next('/login');
  else next();
});

export default router;
