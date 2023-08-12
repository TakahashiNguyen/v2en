import 'package:graphql_flutter/graphql_flutter.dart';

const graphqlURL = 'http://192.168.1.12:2564/graphql';

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

MutationOptions<Object?> registerMutation(
  String username,
  String password,
  String lastName,
  String firstName,
  String gender,
  String birthday,
  String userFace,
) {
  return MutationOptions(document: gql("""
  mutation Mutation(\$newUser: UserInput!) {
    addUser(newUser: \$newUser)
  }
"""), variables: {
    "newUser": {
      "birthDay": birthday,
      "familyName": lastName,
      "gender": gender,
      "givenName": firstName,
      "password": password,
      "userFace": userFace,
      "username": username
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

QueryOptions<Object?> datasQuery() {
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

QueryOptions<Object?> dataQuery(String id) {
  return QueryOptions(document: gql("""
  query Data(\$dataId: String!) {
    data(id: \$dataId) {
      id
      origin
      translated
      translator
      verified
    }
  }
"""), fetchPolicy: FetchPolicy.networkOnly, variables: {'dataId': id});
}

MutationOptions<Object?> dataRemoveMutation(String id) {
  return MutationOptions(document: gql("""
  mutation RemoveData(\$removeDataId: String!) {
    removeData(id: \$removeDataId)
  }
"""), variables: {'removeDataId': id});
}

QueryOptions<Object?> todosQuery() {
  return QueryOptions(document: gql("""
  query Todos {
    todos {
      id
      jobDescription
      deadline
      finished
    }
  }
"""), fetchPolicy: FetchPolicy.networkOnly);
}

MutationOptions<Object?> todoAddMutation(String jobDetailed) {
  return MutationOptions(document: gql("""
  mutation AddTodo(\$newTodo: TodoInput!) {
    addTodo(newTodo: \$newTodo) {
      jobDescription
      deadline
      finished
    }
  }
"""), variables: {
    'newTodo': {
      'jobDescription': jobDetailed,
      'deadline': '06-02-2006',
      'finished': false,
    },
  });
}

MutationOptions<Object?> todoUpdateMutation(String id) {
  return MutationOptions(document: gql("""
  mutation UpdateTodo(\$todoId: String!) {
    updateTodo(todoID: \$todoId)
  }
"""), variables: {'todoId': id});
}

MutationOptions<Object?> todoRemoveMutation(String id) {
  return MutationOptions(document: gql("""
  mutation Mutation(\$todoId: String!) {
    removeTodo(todoID: \$todoId)
  }
"""), variables: {'todoId': id});
}
