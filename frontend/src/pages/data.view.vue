<template>
  <div v-if="error" class="user-indo">
    <h2>Something went wrong</h2>
    <p>{{ error.message }}</p>
  </div>
  <div v-else>
    <q-list v-if="$route.path === '/datas'">
      <q-btn
        style="width: 100%"
        label="Add data"
        @click="$router.push('/datas/add')"
        data-cy="addDataButton"
      />
      <div v-if="isDone">
        <EssentialData
          v-for="link in essentialLinks.datas"
          :key="link"
          v-bind="link"
        />
      </div>
    </q-list>
    <router-view :user="user" :id="id" :dataProcessor="dataProcessor" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import EssentialData from '../components/EssentialData.vue';
import { useQuery } from 'villus';
import { DATAS_QUERY } from 'src/graphql';

export default defineComponent({
  components: {
    EssentialData,
  },

  props: {
    id: { type: String },

    user: {
      type: [Object, String],
      required: true,
    },
  },

  async setup() {
    const { error, data, execute, isDone } = useQuery({
      query: DATAS_QUERY,
      cachePolicy: 'network-only',
    });

    return {
      essentialLinks: data,
      error: error,
      isDone: isDone,
      dataProcessor: execute,
    };
  },
});
</script>
