import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('../layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('../pages/IndexPage.vue') },
      {
        path: '/login',
        component: () => import('../pages/LogIn.vue'),
      },
      {
        path: '/signup',
        component: () => import('../pages/SignUp.vue'),
      },
      {
        path: '/profile',
        component: () => import('../pages/UserPage.vue'),
        meta: { requiresAuth: true },
      },
      {
        path: '/datas',
        component: () => import('../pages/DatasPage.vue'),
        children: [
          {
            path: 'add',
            component: () => import('../pages/AddData.vue'),
          },
          {
            path: 'modifying/:id',
            component: () => import('../pages/AddData.vue'),
            props: true,
          },
          {
            path: ':id',
            component: () => import('../pages/DataView.vue'),
          },
        ],
        props: (route) => ({
          id: Number(route.params.id),
        }),
        meta: { requiresAuth: true },
      },
    ],
  },

  {
    path: '/:catchAll(.*)*',
    component: () => import('../pages/ErrorNotFound.vue'),
  },
];

export default routes;
