import 'package:frontend_new/pages/welcome.page.dart';
import 'package:frontend_new/pages/notfound.dart';
import '../layouts/main.layout.dart';
import 'package:flutter/material.dart';
import 'package:vrouter/vrouter.dart';

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
          ],
        ),
        VWidget(path: '/:catchAll(.*)*', widget: const Error404Page())
      ],
    ),
  );
}
