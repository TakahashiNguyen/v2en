import 'package:frontend_new/graphql.dart';
import 'package:frontend_new/pages/data.editor.dart';
import 'package:frontend_new/pages/data.page.dart';
import 'package:frontend_new/pages/data.view.dart';
import 'package:frontend_new/pages/todo.page.dart';
import 'package:frontend_new/pages/user.login.dart';
import 'package:frontend_new/pages/user.page.dart';
import 'package:frontend_new/pages/user.signup.dart';
import 'package:frontend_new/pages/welcome.page.dart';
import 'package:frontend_new/pages/notfound.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../layouts/main.layout.dart';
import 'package:flutter/material.dart';
import 'package:vrouter/vrouter.dart';
import 'package:graphql_flutter/graphql_flutter.dart';

authPlugin(SharedPreferences prefs, GraphQLClient gqlCli) async {
  final token = prefs.get('token');
  final QueryResult user =
      await GraphQLClient(link: HttpLink(graphqlURL), cache: GraphQLCache())
          .mutate(tokenMutation(token != null ? token as String : ''));
  if (!user.hasException) {
    prefs.setString('token', user.data?['checkToken']['token']);
    return user.data?['checkToken'];
  } else if (user.exception?.raw?[0]['message'] == 'Session not found' &&
      token != null) {
    prefs.remove('token');
    return await authPlugin(prefs, gqlCli);
  }
  return false;
}

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final HttpLink httpLink = HttpLink(graphqlURL);
  final prefs = await SharedPreferences.getInstance();
  final AuthLink authLink = AuthLink(getToken: () async {
    final user = await authPlugin(
        prefs, GraphQLClient(link: httpLink, cache: GraphQLCache()));
    if (user is Map) return 'Bearer ${user['token']}';
    return '';
  });
  final Link link = authLink.concat(httpLink);
  final GraphQLClient gqlCli = GraphQLClient(link: link, cache: GraphQLCache());

  runApp(VRouter(debugShowCheckedModeBanner: false, routes: [
    VNester(
      path: '/',
      widgetBuilder: (child) =>
          MainLayout(gqlCli: gqlCli, prefs: prefs, child: child),
      nestedRoutes: [
        VWidget(path: null, widget: const WelcomePage()),
        VWidget(path: 'login', widget: LoginPage(gqlCli: gqlCli, prefs: prefs)),
        VWidget(
            path: 'signup', widget: RegisterPage(gqlCli: gqlCli, prefs: prefs)),
        VWidget(
            path: 'profile',
            widget: UserProfile(
                userDynamic: authPlugin, gqlCli: gqlCli, prefs: prefs)),
        VNester(
          path: 'datas',
          widgetBuilder: (child) => DataView(gqlCli: gqlCli, child: child),
          nestedRoutes: [
            VWidget(path: null, widget: const CircularProgressIndicator()),
            VWidget(path: 'add', widget: DataEditor(gqlCli: gqlCli)),
            VWidget(path: ':id', widget: DataDetailPage(gqlCli: gqlCli)),
            VWidget(path: 'modified/:id', widget: DataEditor(gqlCli: gqlCli))
          ],
        ),
        VWidget(path: 'todo', widget: TodoPage(gqlCli: gqlCli))
      ],
    ),
    VWidget(path: '/:catchAll(.*)*', widget: const Error404Page())
  ]));
}
