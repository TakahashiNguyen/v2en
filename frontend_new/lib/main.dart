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
            VWidget(path: null, widget: HomeScreen()),
            VWidget(path: 'settings', widget: SettingsScreen()),
          ],
        ),
        VWidget(path: '/:catchAll(.*)*', widget: const Error404Page())
      ],
    ),
  );
}

abstract class BaseWidget extends StatelessWidget {
  String get title;

  String get buttonText;

  String get to;

  @override
  Widget build(BuildContext context) {
    return Material(
      child: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(title),
            SizedBox(height: 50),
            ElevatedButton(
              onPressed: () => context.vRouter.to(to),
              child: Text(buttonText),
            ),
          ],
        ),
      ),
    );
  }
}

class HomeScreen extends BaseWidget {
  @override
  String get title => 'Home';

  @override
  String get buttonText => 'Go to Settings';

  @override
  String get to => '/settings';
}

class SettingsScreen extends BaseWidget {
  @override
  String get title => 'Settings';

  @override
  String get buttonText => 'Go to Home';

  @override
  String get to => '/';
}
