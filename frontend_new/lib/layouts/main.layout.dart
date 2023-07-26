import 'package:flutter/material.dart';
import 'package:get/get.dart';

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
    // final user = authPlugin(opContext: null);

    final userLinks = true is Object
        ? [
            {
              'title': 'Profile',
              'eFunction': () {
                Get.toNamed('/profile');
              },
            },
            {
              'title': 'Todos',
              'eFunction': () {
                Get.toNamed('/todos');
              },
            },
            {
              'title': 'Datas',
              'eFunction': () {
                Get.toNamed('/datas');
              },
            },
            {
              'title': 'LogOut',
              'eFunction': () async {
                // localStorage.removeItem('token');
                // await logoutMutation(user['username'], user['token']);
                Get.offAllNamed('/login');
              },
            },
          ]
        : [
            {
              'title': 'Login',
              'eFunction': () {
                Get.toNamed('/login');
              },
            },
            {
              'title': 'Signup',
              'eFunction': () {
                Get.toNamed('/signup');
              },
            },
          ];

    final linksList = [
      {
        'title': 'Github',
        'caption': 'github.com/takahashinguyen',
        'icon': 'code',
      },
      ...userLinks
    ];

    final listLink = <ListTile>[
      for (Map<String, dynamic> e in linksList)
        ListTile(
          onTap: () {
            (e['eFunction'] ?? () {})();
          },
          title: Text(e['title'] ?? ''),
          subtitle: Text(e['caption'] ?? ''),
          leading: const Icon(Icons.home),
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
