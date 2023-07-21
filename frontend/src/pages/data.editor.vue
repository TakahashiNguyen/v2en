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
              data-cy="originFieldInput"
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
              data-cy="translatedFieldInput"
            />
          </div>
          <button
            data-cy="dataSummit"
            type="submit"
            class="btn btn-primary btn-block"
          >
            Add
          </button>
        </form>
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import router from 'src/router';
import { useMutation, useQuery } from 'villus';
import { useRoute } from 'vue-router';
import { ADD_DATA, GET_DATA, MODIFY_DATA } from 'src/graphql';

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
      type: String,
      required: true,
      default: '',
    },
  },

  async setup(props) {
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
          cachePolicy: 'network-only',
        }).execute()
      ).data;
      if (!modifiedData) router.push('/datas');
      originField = ref(modifiedData?.data.origin);
      translatedField = ref(modifiedData?.data.translated);
      execute = useMutation(MODIFY_DATA).execute;
    }

    const submitForm = async () => {
      try {
        const variables = {
          modifyDataId: route.path.includes('/datas/modifying') ? props.id : '',
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
