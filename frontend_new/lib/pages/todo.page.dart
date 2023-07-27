import 'package:flutter/material.dart';
import 'package:frontend_new/graphql.dart';
import 'package:graphql_flutter/graphql_flutter.dart';

class TodoPage extends StatefulWidget {
  final GraphQLClient gqlCli;

  const TodoPage({super.key, required this.gqlCli});

  @override
  // ignore: library_private_types_in_public_api
  _TodoPageState createState() => _TodoPageState();
}

class _TodoPageState extends State<TodoPage> {
  late final TextEditingController newTodoTextController;

  @override
  void initState() {
    super.initState();
    newTodoTextController = TextEditingController();
  }

  @override
  Widget build(BuildContext context) {
    newTodoTextController.text = '';
    return Scaffold(
        body: Query(
            options: todosQuery(),
            builder: (result, {fetchMore, refetch}) {
              return Scaffold(
                  body: result.hasException
                      ? Column(children: [
                          const Text('Something went wrong'),
                          Text(result.exception.toString())
                        ])
                      : Column(children: [
                          const Text('Todo List'),
                          if (!result.isLoading)
                            Column(children: [
                              for (final todo in result.data?['todos'])
                                TodoTag(
                                    key: ValueKey(todo),
                                    todo: todo['jobDescription'])
                            ])
                          else
                            const CircularProgressIndicator(),
                          Form(
                              child: Column(children: [
                            TextFormField(
                                controller: newTodoTextController,
                                decoration: const InputDecoration(
                                  labelText: 'Origin',
                                ),
                                validator: (value) {
                                  if (value == null || value.isEmpty) {
                                    return 'Please enter origin';
                                  }
                                  return null;
                                }),
                            ElevatedButton(
                                onPressed: () async {
                                  await widget.gqlCli.mutate(todoAddMutation(
                                      newTodoTextController.text));
                                  newTodoTextController.text = '';
                                  refetch!();
                                },
                                child: const Text('Add'))
                          ]))
                        ]));
            }));
  }
}

class TodoTag extends StatelessWidget {
  final String todo;

  const TodoTag({Key? key, required this.todo}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
        padding: const EdgeInsets.all(8),
        margin: const EdgeInsets.symmetric(vertical: 4),
        decoration: BoxDecoration(
            color: Colors.blue, borderRadius: BorderRadius.circular(8)),
        child: Row(children: [
          const Icon(
            Icons.check_circle,
            color: Colors.white,
          ),
          const SizedBox(width: 8),
          Text(todo,
              style: const TextStyle(
                  color: Colors.white, fontWeight: FontWeight.bold))
        ]));
  }
}
