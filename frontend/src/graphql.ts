import gql from 'graphql-tag';

export const graphqlUrl = 'http://[::1]:3000/graphql';

export const TOKEN_MUTATION = gql`
  mutation CheckToken($token: String!) {
    checkToken(token: $token) {
      username
      familyName
      givenName
      gender
      birthDay
      token
    }
  }
`;

export const LOGIN_MUTATION = gql`
  mutation AddUser($loginUser: LoginInput!) {
    LogIn(loginUser: $loginUser) {
      username
      familyName
      givenName
      gender
      birthDay
      token
    }
  }
`;

export const LOGOUT_MUTATION = gql`
  mutation LogOut($username: String!, $token: String!) {
    LogOut(username: $username, token: $token)
  }
`;

export const SIGN_UP_MUTATION = gql`
  mutation AddUser($newUser: UserInput!) {
    addUser(newUser: $newUser) {
      username
      familyName
      givenName
      gender
      birthDay
      token
    }
  }
`;

export const DATAS_QUERY = gql`
  query Query {
    datas {
      id
      origin
      translated
      translator
      verified
    }
  }
`;

export const GET_DATA = gql`
  query Data($dataId: Float!) {
    data(id: $dataId) {
      id
      origin
      translated
      translator
      verified
    }
  }
`;

export const DELETE_DATA = gql`
  mutation RemoveData($removeDataId: Float!) {
    removeData(id: $removeDataId)
  }
`;

export const MODIFY_DATA = gql`
  mutation ModifyData($modifyDataId: Float!, $newData: DataInput!) {
    modifyData(id: $modifyDataId, newData: $newData)
  }
`;

export const ADD_DATA = gql`
  mutation AddData($newData: DataInput!) {
    addData(newData: $newData) {
      id
      origin
      translated
      translator
      hashValue
      verified
    }
  }
`;
