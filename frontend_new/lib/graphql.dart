import 'package:graphql_flutter/graphql_flutter.dart';

const graphqlURL = 'http://127.0.0.1:2564/graphql';

MutationOptions<Object?> loginMutation(String username, String password) {
  return MutationOptions(
    document: gql("""
  mutation LogIn(\$loginUser: LoginInput!) {
    LogIn(loginUser: \$loginUser)
  }
"""),
    variables: {
      'loginUser': {
        'username': username,
        'password': password,
      },
    },
  );
}

MutationOptions<Object?> tokenMutation(String token) {
  return MutationOptions(
    document: gql("""
  mutation CheckToken(\$token: String!) {
    checkToken(token: \$token) {
      username
      familyName
      givenName
      gender
      birthDay
      token
    }
  }
"""),
    variables: {'token': token},
  );
}
