import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('../layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('../pages/my.github.vue') },
      {
        path: '/login',
        component: () => import('../pages/user.login.vue'),
      },
      {
        path: '/signup',
        component: () => import('../pages/user.signup.vue'),
      },
      {
        path: '/profile',
        component: () => import('../pages/user.page.vue'),
        meta: { requiresAuth: true },
      },
      {
        path: '/datas',
        component: () => import('../pages/data.view.vue'),
        children: [
          {
            path: 'add',
            component: () => import('../pages/data.editor.vue'),
          },
          {
            path: 'modifying/:id',
            component: () => import('../pages/data.editor.vue'),
            props: true,
          },
          {
            path: ':id',
            component: () => import('../pages/data.page.vue'),
          },
        ],
        props: route => ({
          id: String(route.params.id),
        }),
        meta: { requiresAuth: true },
      },
      {
        path: '/todos',
        component: () => import('../pages/todo.page.vue'),
        meta: { requiresAuth: true },
      },
    ],
  },

  {
    path: '/:catchAll(.*)*',
    component: () => import('../pages/404.vue'),
  },
];

export default routes;
