import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:frontend_new/graphql.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:vrouter/vrouter.dart';
import 'package:flutter_face_api/face_api.dart' as fau;

class LoginPage extends StatefulWidget {
  final GraphQLClient gqlCli;
  final SharedPreferences prefs;

  const LoginPage({Key? key, required this.gqlCli, required this.prefs})
      : super(key: key);

  @override
  // ignore: library_private_types_in_public_api
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _formKey = GlobalKey<FormState>();
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();
  late String userFace = '';

  @override
  void initState() {
    super.initState();
    initPlatformState();
  }

  Future<void> initPlatformState() async {
    fau.FaceSDK.init();
  }

  void _submitForm() async {
    final String username = _usernameController.text;
    final String password = userFace == ''
        ? 'UserPasswordAuthencation ${_passwordController.text}'
        : userFace;

    final QueryResult result =
        await widget.gqlCli.mutate(loginMutation(username, password));

    if (!result.hasException) {
      widget.prefs.setString('token', result.data?["LogIn"]);
      // ignore: use_build_context_synchronously
      context.vRouter.to('/');
    }
  }

  Future<Widget> fetchData(BuildContext context) async {
    return Scaffold(
      body: Center(
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Form(
              key: _formKey,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const SizedBox(height: 20),
                  const Text(
                    'Welcome back!',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 20),
                  const Text(
                    'We\'re so excited to see you again!',
                    style: TextStyle(fontSize: 16),
                  ),
                  const SizedBox(height: 40),
                  TextFormField(
                    controller: _usernameController,
                    decoration: const InputDecoration(
                      labelText: 'Username',
                    ),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Please enter your username';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 20),
                  Row(
                    children: [
                      Expanded(
                        child: TextFormField(
                          controller: _passwordController,
                          obscureText: true,
                          decoration: const InputDecoration(
                            labelText: 'Password',
                          ),
                          validator: (value) {
                            if (value == null || value.isEmpty) {
                              return 'Please enter your password';
                            }
                            return null;
                          },
                        ),
                      ),
                      InkWell(
                        child: const Icon(
                          Icons.face_outlined,
                          color: Colors.blue,
                        ),
                        onTap: () async {
                          fau.FaceSDK.presentFaceCaptureActivity()
                              .then((result) {
                            var response = fau.FaceCaptureResponse.fromJson(
                                json.decode(result))!;
                            if (response.image != null &&
                                response.image!.bitmap != null) {
                              userFace =
                                  'UserFaceAuthencation ${response.image!.bitmap!}';
                              _submitForm();
                            }
                          });
                        },
                      ),
                    ],
                  ),
                  const SizedBox(height: 40),
                  ElevatedButton(
                    onPressed: () {
                      if (_formKey.currentState!.validate()) {
                        _submitForm();
                      }
                    },
                    child: const Text('Login'),
                  ),
                  const SizedBox(height: 20),
                  TextButton(
                    onPressed: () {
                      // TODO: Implement forgot password logic
                    },
                    child: const Text('Forgot your password?'),
                  ),
                ],
              ),
            ),
          ),
        ),
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
