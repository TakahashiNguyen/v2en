import 'package:flutter/material.dart';
import 'package:frontend_new/graphql.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:vrouter/vrouter.dart';

class DataEditor extends StatelessWidget {
  final TextEditingController originController = TextEditingController();
  final TextEditingController translatedController = TextEditingController();
  final GraphQLClient gqlCli;

  DataEditor({super.key, required this.gqlCli});

  Future<void> submitForm(BuildContext context) async {
    // Implement the logic to handle form submission
    String origin = originController.text;
    String translated = translatedController.text;

    // Perform necessary actions with the form data
    await gqlCli.mutate(dataAddMutation(origin, translated));
    originController.text = translatedController.text = '';
    // ignore: use_build_context_synchronously
    context.vRouter.to('/datas');
  }

  @override
  Widget build(BuildContext context) {
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
}
