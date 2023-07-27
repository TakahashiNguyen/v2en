import 'package:flutter/material.dart';
import 'package:frontend_new/graphql.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:vrouter/vrouter.dart';

// ignore: must_be_immutable
class DataEditor extends StatelessWidget {
  final TextEditingController originController = TextEditingController();
  final TextEditingController translatedController = TextEditingController();
  final GraphQLClient gqlCli;
  late String id;

  DataEditor({super.key, required this.gqlCli});

  Future<void> submitForm(BuildContext context) async {
    // Implement the logic to handle form submission
    String origin = originController.text;
    String translated = translatedController.text;

    // Perform necessary actions with the form data
    final data = await gqlCli.mutate(dataAddMutation(origin, translated));
    originController.text = translatedController.text = '';
    // ignore: use_build_context_synchronously
    context.vRouter.to('/datas/${data.data!['addData']['id']}');
  }


  Future<Widget> fetchData(BuildContext context) async {
    id = context.vRouter.pathParameters['id'] ?? '';
    final data = (await gqlCli.query(dataQuery(id))).data?['data'] ?? '';
    originController.text = data != '' ? data['origin'] : '';
    translatedController.text = data != '' ? data['translated'] : '';

    return Scaffold(
      body: Center(
        child: SizedBox(
          width: 300,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              TextFormField(
                controller: originController,
                decoration: const InputDecoration(
                  labelText: 'Origin',
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter origin';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: translatedController,
                decoration: const InputDecoration(
                  labelText: 'Translated',
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter translated';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: () async => {await submitForm(context)},
                child: const Text('Add'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return GraphQLProvider(
        client: ValueNotifier(gqlCli),
        child: FutureBuilder<Widget>(
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
        ));
  }
}
