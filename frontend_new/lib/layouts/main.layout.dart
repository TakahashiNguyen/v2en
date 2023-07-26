import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../components/link.drawer.element.dart';

class MainLayout extends StatelessWidget {
  final Function userMutation;
  final Function logoutMutation;
  final Widget child;

  const MainLayout(
      {super.key,
      required this.userMutation,
      required this.logoutMutation,
      required this.child});

  @override
  Widget build(BuildContext context) {
    final leftDrawerOpen = false.obs;
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
      ...userLinks,
    ];

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.blue,
      ),
      drawer: Drawer(
        child: ListView(
          children: [
            ListTile(
              title: const Text(
                'v2en',
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                ),
              ),
              tileColor: Colors.grey[200],
            ),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: linksList.length,
              itemBuilder: (context, index) {
                return EssentialLink(
                  title: linksList[index]['title'] as String,
                  icon: linksList[index]['icon'] as String,
                  eFunction: linksList[index]['eFunction'] as Function,
                  leftDrawer: () {
                    leftDrawerOpen.value = false;
                  },
                  caption: '',
                );
              },
            ),
          ],
        ),
      ),
      body: child,
    );
  }
}

authPlugin({required opContext}) {}
