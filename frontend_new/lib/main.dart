import 'package:vrouter/vrouter.dart';
import '../layouts/main.layout.dart';
import '../pages/my.github.dart';
import '../pages/user.login.dart';
import '../pages/user.signup.dart';
import '../pages/user.page.dart';
import '../pages/data.view.dart';
import '../pages/data.editor.dart';
import '../pages/data.page.dart';
import '../pages/todo.page.dart';
import '../pages/404.dart';

List<VRouteElement> routes = [
  VWidget(
    path: '/',
    widget: MainLayout(),
    children: [
      VWidget(
        path: '',
        widget: MyGithub(),
      ),
      VWidget(
        path: '/login',
        widget: UserLogin(),
      ),
      VWidget(
        path: '/signup',
        widget: UserSignup(),
      ),
      VGuard(
        path: '/profile',
        component: UserPage(),
        beforeEnter: (vRedirector) async {
          // check if user is authenticated
          // if not, redirect to login page
        },
      ),
      VWidget(
        path: '/datas',
        widget: DataView(),
        children: [
          VWidget(
            path: 'add',
            widget: DataEditor(),
          ),
          VWidget(
            path: 'modifying/:id',
            widget: DataEditor(),
            props: (vParameters) {
              return {'id': vParameters.pathParameters['id']!};
            },
          ),
          VWidget(
            path: ':id',
            widget: DataPage(),
            props: (vParameters) {
              return {'id': vParameters.pathParameters['id']!};
            },
          ),
        ],
        props: (vParameters) {
          return {'id': vParameters.pathParameters['id']!};
        },
        beforeEnter: (vRedirector) async {
          // check if user is authenticated
          // if not, redirect to login page
        },
      ),
      VWidget(
        path: '/todos',
        widget: TodoPage(),
        beforeEnter: (vRedirector) async {
          // check if user is authenticated
          // if not, redirect to login page
        },
      ),
    ],
  ),
  VWidget(
    path: '/:catchAll(.*)*',
    widget: NotFound(),
  ),
];
