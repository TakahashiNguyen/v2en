import 'package:flutter/material.dart';
import 'package:frontend_new/graphql.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:vrouter/vrouter.dart';

class DataView extends StatefulWidget {
  final Widget child;
  final GraphQLClient gqlCli;

  const DataView({super.key, required this.child, required this.gqlCli});

  @override
  // ignore: library_private_types_in_public_api
  _DataViewState createState() => _DataViewState();
}

class _DataViewState extends State<DataView> {
  bool error = false;
  String errorMessage = '';
  List<dynamic> essentialLinks = [];

  @override
  void initState() {
    super.initState();
  }

  Future<Widget> fetchData(BuildContext context) async {
    final qdata = (await widget.gqlCli.query(dataQuery()));
    var dataList = <ListTile>[];

    if (!qdata.hasException) {
      dataList = <ListTile>[
        for (Map<String, dynamic> e in qdata.data?['datas'])
          ListTile(
            title: Text(e['origin'] + ' >> ' + e['translated']),
            subtitle: Text(
                // ignore: prefer_interpolation_to_compose_strings
                'translator: ' +
                    e['translator'] +
                    '; verified: ' +
                    (e['verified'] ? 'true' : 'false')),
          )
      ];
    } else {
      error = true;
    }

    return Scaffold(
      body: error
          ? Column(children: [
              const Text(
                'Something went wrong',
                style: TextStyle(fontSize: 24),
              ),
              Text(
                errorMessage,
                style: const TextStyle(fontSize: 16),
              )
            ])
          : Container(
              // ignore: use_build_context_synchronously
              child: context.vRouter.path == '/datas'
                  ? Column(children: [
                      ElevatedButton(
                        style: ButtonStyle(
                          fixedSize: MaterialStateProperty.all(
                              const Size(double.infinity, 48)),
                        ),
                        onPressed: () {
                          // Implement the equivalent of $router.push('/datas/add') in Dart
                        },
                        child: const Text('Add data'),
                      ),
                      ...dataList
                    ])
                  : Container(child: widget.child),
            ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Widget>(
      future: fetchData(context),
      builder: (BuildContext context, AsyncSnapshot<Widget> snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
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
