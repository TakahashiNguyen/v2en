<template>
  <q-page class="justify-center">
    <div class="account-page center-of-parent">
      <div class="account-form">
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="emailOrUsername" class="form-label">Origin</label>
            <input
              id="emailOrUsername"
              v-model="originField"
              type="text"
              class="form-control"
              required
            />
          </div>
          <div class="form-group">
            <label for="password" class="form-label">Translated</label>
            <input
              id="password"
              v-model="translatedField"
              type="text"
              class="form-control"
              required
            />
          </div>
          <button type="submit" class="btn btn-primary btn-block">Add</button>
        </form>
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import router from 'src/router';
import gql from 'graphql-tag';
import { useMutation, useQuery } from 'villus';
import { useRoute } from 'vue-router';

const ADD_DATA = gql`
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
const MODIFY_DATA = gql`
  mutation ModifyData($modifyDataId: Float!, $newData: DataInput!) {
    modifyData(id: $modifyDataId, newData: $newData)
  }
`;
const GET_DATA = gql`
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

export default defineComponent({
  props: {
    user: {
      type: [Object, String],
      required: true,
    },
    dataProcessor: {
      type: Function,
      required: true,
    },
    id: {
      type: Number,
      required: true,
    },
  },

  async setup(props) {
    if (!props.user) router.push('/login');
    const route = useRoute();

    let originField = ref('');
    let translatedField = ref('');
    let { execute } = useMutation(ADD_DATA);

    if (route.path.includes('/datas/modifying')) {
      const modifiedData = (
        await useQuery({
          query: GET_DATA,
          variables: {
            dataId: props.id,
          },
        }).execute()
      ).data.data;
      originField = ref(modifiedData?.origin);
      translatedField = ref(modifiedData?.translated);
      execute = useMutation(MODIFY_DATA).execute;
    }

    const submitForm = async () => {
      try {
        const variables = {
          modifyDataId: props.id,
          newData: {
            origin: originField.value,
            translated: translatedField.value,
            translator: 'human',
            verified: false,
          },
        };
        const response = (await execute(variables)).data.addData ?? props;

        await props.dataProcessor();
        router.push('/datas/' + response.id);
      } catch (error) {
        console.error(error);
      }
    };

    return {
      originField,
      translatedField,
      submitForm,
    };
  },
});
</script>
