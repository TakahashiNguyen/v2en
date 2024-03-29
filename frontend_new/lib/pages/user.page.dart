import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:shared_preferences/shared_preferences.dart';

class UserProfile extends StatelessWidget {
  final dynamic userDynamic;
  final GraphQLClient gqlCli;
  final SharedPreferences prefs;

  const UserProfile(
      {Key? key,
      required this.userDynamic,
      required this.gqlCli,
      required this.prefs})
      : super(key: key);

  Future<Widget> fetchData(BuildContext context) async {
    final user = await userDynamic(prefs, gqlCli);
    final userDisplay = {
      'name': user['username'],
      'birthday': user['birthDay'],
      'gender': user['gender'],
    };

    return Container(
      decoration: BoxDecoration(
        border: Border.all(color: Colors.grey),
      ),
      padding: const EdgeInsets.all(10),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            userDisplay['name'],
            style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 10),
          Text('Birthday: ${userDisplay['birthday']}'),
          Text('Gender: ${userDisplay['gender']}'),
        ],
      ),
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
