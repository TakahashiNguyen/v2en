import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:vrouter/vrouter.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter/services.dart';
import '../graphql.dart';
import '../main.dart';

class MainLayout extends StatelessWidget {
  final Widget child;
  final GraphQLClient gqlCli;
  final SharedPreferences prefs;

  const MainLayout(
      {Key? key,
      required this.child,
      required this.gqlCli,
      required this.prefs})
      : super(key: key);

  Future<Widget> fetchData(BuildContext context) async {
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.manual,
        overlays: [SystemUiOverlay.top]);

    final user = await authPlugin(prefs, gqlCli);

    final userLink = [
      {
        'title': 'Github',
        'caption': 'github.com/takahashinguyen',
        'icon': Icons.code,
        'eFunction': () {
          context.vRouter.to('/');
        }
      },
      ...user.runtimeType != bool
          ? [
              {
                'title': 'Profile',
                'eFunction': () {
                  context.vRouter.to('/profile');
                },
              },
              {
                'title': 'Todos',
                'eFunction': () {
                  context.vRouter.to('/todos');
                },
              },
              {
                'title': 'Datas',
                'eFunction': () {
                  context.vRouter.to('/datas');
                },
              },
              {
                'title': 'LogOut',
                'eFunction': () async {
                  final user = await authPlugin(prefs, gqlCli);
                  await gqlCli
                      .mutate(logoutMutation(user['username'], user['token']));
                  await prefs.remove('token');
                  // ignore: use_build_context_synchronously
                  context.vRouter.to('/login');
                },
              },
            ]
          : [
              {
                'title': 'Login',
                'eFunction': () {
                  context.vRouter.to('/login');
                },
              },
              {
                'title': 'Signup',
                'eFunction': () {
                  context.vRouter.to('/signup');
                },
              },
            ]
    ];

    final listLink = <ListTile>[
      for (Map<String, dynamic> e in userLink)
        ListTile(
          onTap: () {
            (e['eFunction'] ?? () {})();
          },
          title: Text(e['title'] ?? ''),
          subtitle: Text(e['caption'] ?? ''),
          leading: (Icon(e['icon'] as IconData?)),
          tileColor: Colors.grey[200],
        )
    ];

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.blue,
      ),
      drawer: Drawer(
        child: ListView(
          children: <Widget>[
            const ListTile(
              title: Text(
                'v2en',
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            ...listLink
          ],
        ),
      ),
      body: child,
    );
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Widget>(
      future: fetchData(context),
      builder: (BuildContext context, AsyncSnapshot<Widget> snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          // While waiting for the future to complete, show a loading indicator
          return const CircularProgressIndicator();
        } else if (snapshot.hasError) {
          // If an error occurred, show an error message
        }
        return snapshot.data ??
            const Scaffold(
              body: Column(
                children: [Text('Something went wrong.')],
              ),
            );
      },
    );
  }
}
