import 'package:flutter/material.dart';

class MainLayout extends StatelessWidget {
  final List<Map<String, dynamic>> essentialLinks;
  final bool leftDrawerOpen;
  final Function toggleLeftDrawer;
  final dynamic user;

  MainLayout({
    required this.essentialLinks,
    required this.leftDrawerOpen,
    required this.toggleLeftDrawer,
    required this.user,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          AppBar(
            backgroundColor: Colors.blue,
            title: Row(
              children: [
                IconButton(
                  icon: Icon(Icons.menu),
                  onPressed: toggleLeftDrawer,
                ),
              ],
            ),
          ),
          Drawer(
            child: ListView(
              children: [
                ListTile(
                  title: Text(
                    'v2en',
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  tileColor: Colors.grey[200],
                ),
                ListView.builder(
                  shrinkWrap: true,
                  physics: NeverScrollableScrollPhysics(),
                  itemCount: essentialLinks.length,
                  itemBuilder: (context, index) {
                    return ListTile(
                      title: Text(essentialLinks[index]['title']),
                      onTap: () {
                        essentialLinks[index]['eFunction']();
                        toggleLeftDrawer();
                      },
                    );
                  },
                ),
              ],
            ),
          ),
          Expanded(
            child: Container(
              child: RouterView(user: user),
            ),
          ),
        ],
      ),
    );
  }
}

class RouterView extends StatelessWidget {
  final dynamic user;

  RouterView({required this.user});

  @override
  Widget build(BuildContext context) {
    // Implement your router view logic here
    return Container();
  }
}
