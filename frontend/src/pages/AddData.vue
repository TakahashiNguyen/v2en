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
import { useMutation } from 'villus';

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
  },

  async setup(props) {
    if (!props.user) router.push('/login');

    const originField = ref('');
    const translatedField = ref('');

    const { execute } = useMutation(ADD_DATA);

    const submitForm = async () => {
      try {
        const variables = {
          newData: {
            origin: originField.value,
            translated: translatedField.value,
            translator: 'human',
            verified: false,
          },
        };
        const response = (await execute(variables)).data.addData;

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
