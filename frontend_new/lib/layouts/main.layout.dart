import 'package:flutter/material.dart';
import 'package:vrouter/vrouter.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter/services.dart';

class MainLayout extends StatelessWidget {
  final Function userMutation;
  final Function logoutMutation;
  final Widget child;

  const MainLayout({
    Key? key,
    required this.userMutation,
    required this.logoutMutation,
    required this.child,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.manual,
        overlays: [SystemUiOverlay.top]);

    final user = authPlugin(opContext: null);

    final userLink = [
      {
        'title': 'Github',
        'caption': 'github.com/takahashinguyen',
        'icon': Icons.code,
        'eFunction': () {
          context.vRouter.to('/');
        }
      },
      ...user is Object
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
                  final prefs = await SharedPreferences.getInstance();
                  await prefs.remove('token');
                  // await logoutMutation(user['username'], user['token']);
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
}

authPlugin({required opContext}) {}
