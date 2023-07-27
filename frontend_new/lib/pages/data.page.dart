import 'package:flutter/material.dart';
import 'package:frontend_new/graphql.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:vrouter/vrouter.dart';

class DataDetailPage extends StatefulWidget {
  const DataDetailPage({super.key});

  @override
  // ignore: library_private_types_in_public_api
  _DataDetailPageState createState() => _DataDetailPageState();
}

class _DataDetailPageState extends State<DataDetailPage> {
  late final TextEditingController originController;
  late final TextEditingController translatedController;

  @override
  void initState() {
    super.initState();
    originController = TextEditingController();
    translatedController = TextEditingController();
  }

  @override
  Widget build(BuildContext context) {
    final id = context.vRouter.pathParameters['id'];
    return Scaffold(
      body: Query(
        options: dataQuery(id!),
        builder: (QueryResult result,
            {VoidCallback? refetch, FetchMore? fetchMore}) {
          if (result.hasException) {
            return Text(result.exception.toString());
          }

          if (result.isLoading) {
            return const CircularProgressIndicator();
          }

          final data = result.data!['data'];

          originController.text = data?['origin'];
          translatedController.text = data?['translated'];

          return Column(
            children: [
              TextField(
                controller: originController,
                decoration: const InputDecoration(
                  labelText: 'Origin',
                ),
              ),
              TextField(
                controller: translatedController,
                decoration: const InputDecoration(
                  labelText: 'Translated',
                ),
              ),
              ElevatedButton(
                onPressed: () {
                  // Implement the logic to modify the data
                  // Use the Mutation widget to execute the mutation
                },
                child: const Text('Modify'),
              ),
              ElevatedButton(
                onPressed: () {
                  // Implement the logic to delete the data
                  // Use the Mutation widget to execute the mutation
                  Navigator.pop(context);
                },
                child: const Text('Delete'),
              ),
            ],
          );
        },
      ),
    );
  }
}
