import 'package:frontend_new/pages/user.login.dart';
import 'package:frontend_new/pages/welcome.page.dart';
import 'package:frontend_new/pages/notfound.dart';
import '../layouts/main.layout.dart';
import 'package:flutter/material.dart';
import 'package:vrouter/vrouter.dart';
import 'package:graphql_flutter/graphql_flutter.dart';

void main() {
  runApp(
    VRouter(
      debugShowCheckedModeBanner: false,
      routes: [
        VNester(
          path: '/',
          widgetBuilder: (child) => MainLayout(
            logoutMutation: () {},
            userMutation: () {},
            child: child,
          ),
          nestedRoutes: [
            VWidget(path: null, widget: const WelcomePage()),
            VWidget(path: '/login', widget: const LoginPage())
          ],
        ),
        VWidget(path: '/:catchAll(.*)*', widget: const Error404Page())
      ],
    ),
  );
}
