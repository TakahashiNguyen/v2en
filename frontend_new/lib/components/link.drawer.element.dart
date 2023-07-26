import 'package:flutter/material.dart';

class EssentialLink extends StatelessWidget {
  final String title;
  final String caption;
  final Function eFunction;
  final String icon;
  final Function leftDrawer;

  const EssentialLink({super.key, 
    required this.title,
    required this.caption,
    this.eFunction = _defaultFunction,
    this.icon = '',
    required this.leftDrawer,
  });

  static void _defaultFunction() {
    // Default function implementation
  }

  @override
  Widget build(BuildContext context) {
    return ListTile(
      onTap: () {
        eFunction();
        leftDrawer();
      },
      title: Text(title),
      subtitle: Text(caption),
      leading: icon.isNotEmpty ? Icon(icon as IconData?) : null,
    );
  }
}
