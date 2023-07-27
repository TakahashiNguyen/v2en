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
                                    todo: todo['jobDescription'],
                                    id: todo['id'],
                                    deadline: todo['deadline'],
                                    finished: todo['finished'],
                                    gqlCli: widget.gqlCli,
                                    refetch: refetch),
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
                                  await refetch!();
                                },
                                child: const Text('Add'))
                          ]))
                        ]));
            }));
  }
}

class TodoTag extends StatelessWidget {
  final String todo;
  final String id;
  final String deadline;
  final bool finished;
  final GraphQLClient gqlCli;
  final Future<QueryResult<Object?>?> Function()? refetch;

  const TodoTag({
    Key? key,
    required this.todo,
    required this.id,
    required this.deadline,
    required this.finished,
    required this.gqlCli,
    required this.refetch,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(8),
      margin: const EdgeInsets.symmetric(vertical: 4),
      decoration: BoxDecoration(
          color: Colors.blue, borderRadius: BorderRadius.circular(8)),
      child: Row(
        children: [
          InkWell(
            child: Icon(
              (finished) ? Icons.check_circle : Icons.circle,
              color: Colors.white,
            ),
            onTap: () async {
              await gqlCli.mutate(todoUpdateMutation(id));
              refetch!();
            },
          ),
          const SizedBox(width: 8),
          Text(
            todo,
            style: const TextStyle(
              color: Colors.white,
              fontWeight: FontWeight.bold,
            ),
          ),
          const Spacer(),
          InkWell(
            child: const Icon(
              Icons.delete,
              color: Colors.white,
            ),
            onTap: () async {
              await gqlCli.mutate(todoRemoveMutation(id));
              refetch!();
            },
          ),
        ],
      ),
    );
  }
}
