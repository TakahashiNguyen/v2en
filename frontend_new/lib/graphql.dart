import 'package:graphql_flutter/graphql_flutter.dart';

const graphqlURL = 'http://127.0.0.1:2564/graphql';

MutationOptions<Object?> loginMutation(String username, String password) {
  return MutationOptions(document: gql("""
  mutation LogIn(\$loginUser: LoginInput!) {
    LogIn(loginUser: \$loginUser)
  }
"""), variables: {
    'loginUser': {
      'username': username,
      'password': password,
    }
  });
}

MutationOptions<Object?> tokenMutation(String token) {
  return MutationOptions(document: gql("""
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
"""), variables: {'token': token});
}

MutationOptions<Object?> registerMutation(String username, String password,
    String lastName, String firstName, String gender, String birthday) {
  return MutationOptions(document: gql("""
  mutation AddUser(\$newUser: UserInput!) {
    addUser(newUser: \$newUser)
  }
"""), variables: {
    'newUser': {
      'username': username,
      'familyName': lastName,
      'givenName': firstName,
      'gender': gender,
      'birthDay': birthday,
      'password': password,
    }
  });
}

MutationOptions<Object?> logoutMutation(String username, String token) {
  return MutationOptions(document: gql("""
  mutation LogOut(\$username: String!, \$token: String!) {
    LogOut(username: \$username, token: \$token)
  }
"""), variables: {'username': username, 'token': token});
}

QueryOptions<Object?> dataQuery() {
  return QueryOptions(
    document: gql("""
  query Query {
    datas {
      id
      origin
      translated
      translator
      verified
    }
  }
"""),
    fetchPolicy: FetchPolicy.networkOnly,
  );
}

MutationOptions<Object?> dataAddMutation(String origin, String translated) {
  return MutationOptions(document: gql("""
  mutation AddData(\$newData: DataInput!) {
    addData(newData: \$newData) {
      id
      origin
      translated
      translator
      hashValue
      verified
    }
  }
"""), variables: {
    'newData': {
      'origin': origin,
      'translated': translated,
      'translator': 'human',
      'verified': false,
    }
  });
}
