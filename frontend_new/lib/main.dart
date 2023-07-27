import 'package:frontend_new/graphql.dart';
import 'package:frontend_new/pages/user.login.dart';
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
      await gqlCli.mutate(tokenMutation(token != null ? token as String : ''));
  if (!user.hasException) {
    prefs.setString('token', user.data?['checkToken']['token']);
    return user.data?['checkToken'];
  }
  return false;
}

void main() async {
  final HttpLink httpLink = HttpLink(graphqlURL);
  final prefs = await SharedPreferences.getInstance();
  final token = prefs.get('token');
  final AuthLink authLink = AuthLink(getToken: () => 'Bearer $token');
  final Link link = authLink.concat(httpLink);
  final GraphQLClient gqlCli = GraphQLClient(link: link, cache: GraphQLCache());

  runApp(VRouter(debugShowCheckedModeBanner: false, routes: [
    VNester(
      path: '/',
      widgetBuilder: (child) =>
          MainLayout(gqlCli: gqlCli, prefs: prefs, child: child),
      nestedRoutes: [
        VWidget(path: null, widget: const WelcomePage()),
        VWidget(
            path: '/login', widget: LoginPage(gqlCli: gqlCli, prefs: prefs)),
        VWidget(
            path: '/signup', widget: RegisterPage(gqlCli: gqlCli, prefs: prefs))
      ],
    ),
    VWidget(path: '/:catchAll(.*)*', widget: const Error404Page())
  ]));
}
