<template>
  <div class="user-profile">
    <div v-if="error" class="user-indo">
      <h2>Data is deleted or doesn't exist</h2>
      <p>{{ error.message }}</p>
    </div>
    <div v-else class="user-info">
      <h2>{{ data.translator }}</h2>
      <p data-cy="originField">Origin: {{ data.origin }}</p>
      <p data-cy="translatedField">Translated: {{ data.translated }}</p>
    </div>

    <div v-if="!error" class="button-container">
      <q-btn
        data-cy="deleteButton"
        class="button"
        label="Delete data"
        @click="deleteData()"
      />
      <q-btn
        data-cy="modifyButton"
        class="button"
        label="Modify data"
        @click="modifyDataRouter(id)"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { DELETE_DATA, GET_DATA } from 'src/graphql';
import router from 'src/router';
import { useMutation, useQuery } from 'villus';
import { defineComponent } from 'vue';

export default defineComponent({
  methods: {
    modifyDataRouter(id: string) {
      router.push('/datas/modifying/' + id);
    },
    async deleteData() {
      await this.execute({
        removeDataId: this.data.id,
      });
      await this.$props.dataProcessor();
      router.back();
    },
  },
  props: {
    id: {
      type: String,
      required: true,
    },
    dataProcessor: {
      type: Function,
      required: true,
    },
  },
  async setup(props) {
    const getData = async () => {
      return await useQuery({
        query: GET_DATA,
        variables: {
          dataId: props.id,
        },
        cachePolicy: 'network-only',
      }).execute();
    };
    const { error, data } = await getData();
    const { execute } = useMutation(DELETE_DATA);

    return { error: error, data: data?.data, execute: execute };
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
