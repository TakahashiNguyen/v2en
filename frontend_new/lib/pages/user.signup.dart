import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:frontend_new/main.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:vrouter/vrouter.dart';
import 'package:flutter_face_api/face_api.dart' as fau;

import '../graphql.dart';

class RegisterPage extends StatefulWidget {
  final GraphQLClient gqlCli;
  final SharedPreferences prefs;

  const RegisterPage({Key? key, required this.gqlCli, required this.prefs})
      : super(key: key);

  @override
  // ignore: library_private_types_in_public_api
  _RegisterPageState createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final _formKey = GlobalKey<FormState>();
  final _firstNameController = TextEditingController();
  final _lastNameController = TextEditingController();
  final _birthdayController = TextEditingController();
  final _genderController = TextEditingController();
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

  setImage(Uint8List? imageFile, int type) {
    if (imageFile == null) return;
    setState(() {
      userFace = base64Encode(imageFile);
    });
  }

  void _submitForm() async {
    final String firstName = _firstNameController.text;
    final String lastName = _lastNameController.text;
    final String birthday = _birthdayController.text;
    final String gender = _genderController.text;
    final String username = _usernameController.text;
    final String password =
        'UserPasswordAuthencation ${_passwordController.text}';

    final QueryResult result = await widget.gqlCli.mutate(registerMutation(
        username, password, lastName, firstName, gender, birthday, userFace));

    if (!result.hasException) {
      widget.prefs.setString('token', result.data?['addUser']);
      final user = await authPlugin(widget.prefs, widget.gqlCli);
      if (user.runtimeType != Null) {
        await widget.prefs.setString('token', user['token']);
        // ignore: use_build_context_synchronously
        context.vRouter.to('/profile');
      }
    }
  }

  @override
  Widget build(BuildContext context) {
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
                    'Create an account',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 20),
                  TextFormField(
                    controller: _firstNameController,
                    decoration: const InputDecoration(
                      labelText: 'First Name',
                    ),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Please enter your first name';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 20),
                  TextFormField(
                    controller: _lastNameController,
                    decoration: const InputDecoration(
                      labelText: 'Last Name',
                    ),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Please enter your last name';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 20),
                  TextFormField(
                    controller: _birthdayController,
                    decoration: const InputDecoration(
                      labelText: 'Birthday',
                    ),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Please enter your birthday';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 20),
                  TextFormField(
                    controller: _genderController,
                    decoration: const InputDecoration(
                      labelText: 'Gender',
                    ),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Please enter your gender';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 20),
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
                        flex: 4,
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
                      Expanded(
                        flex: 1,
                        child: InkWell(
                          child: Icon(
                            Icons.face_outlined,
                            color: (userFace != '') ? Colors.green : Colors.red,
                          ),
                          onTap: () async {
                            fau.FaceSDK.presentFaceCaptureActivity()
                                .then((result) {
                              var response = fau.FaceCaptureResponse.fromJson(
                                  json.decode(result))!;
                              if (response.image != null &&
                                  response.image!.bitmap != null) {
                                setImage(
                                    base64Decode(response.image!.bitmap!
                                        .replaceAll("\n", "")),
                                    fau.ImageType.LIVE);
                              }
                            });
                          },
                        ),
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
                    child: const Text('Sign up'),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
