<template>
  <div class="user-profile">
    <div v-if="error" class="user-indo">
      <h2>Data is deleted or doesn't exist</h2>
      <p>{{ error.message }}</p>
    </div>
    <div v-else class="user-info">
      <h2>{{ data.translator }}</h2>
      <p>Origin: {{ data.origin }}</p>
      <p>Translated: {{ data.translated }}</p>
    </div>

    <div v-if="!error" class="button-container">
      <q-btn class="button" label="Delete data" @click="execute()" />
      <q-btn class="button" label="Modify data" @click="modifyDataRouter(id)" />
    </div>
  </div>
</template>

<script lang="ts">
import gql from 'graphql-tag';
import router from 'src/router';
import { useMutation, useQuery } from 'villus';
import { defineComponent } from 'vue';

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

const DELETE_DATA = gql`
  mutation RemoveData($removeDataId: Float!) {
    removeData(id: $removeDataId)
  }
`;

export default defineComponent({
  methods: {
    modifyDataRouter(id: number) {
      router.push('/datas/modifying/' + id);
    },
  },
  props: {
    id: {
      type: Number,
      required: true,
    },
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

    const { error, data } = await useQuery({
      query: GET_DATA,
      variables: {
        dataId: props.id,
      },
      cachePolicy: 'network-only',
    }).execute();

    const { execute } = useMutation(DELETE_DATA);
    const deleteData = async () => {
      await execute({
        removeDataId: data.data.id,
      });
      await props.dataProcessor();
      router.back();
    };

    return { error: error, data: data?.data, execute: deleteData };
  },
});
</script>

<style scoped>
.button-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.button {
  width: 50%;
}
</style>
