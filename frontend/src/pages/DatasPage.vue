<template>
  <q-list v-if="$route.path === '/datas'">
    <q-btn
      style="width: 100%"
      label="Add data"
      @click="$router.push('/datas/add')"
    />
    <EssentialData v-for="link in essentialLinks" :key="link" v-bind="link" />
  </q-list>

  <router-view :user="user" :id="id" :dataProcessor="dataProcessor" />
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import EssentialData from '../components/EssentialData.vue';
import { useQuery } from 'villus';
import { DATAS_QUERY } from 'src/graphql';

export default defineComponent({
  components: {
    EssentialData,
  },

  props: {
    id: { type: Number },

    user: {
      type: [Object, String],
      required: true,
    },
  },

  async setup() {
    const essentialLinks = ref([]);

    const dataProcessor = async () => {
      const { error, data } = await useQuery({ query: DATAS_QUERY }).execute({
        cachePolicy: 'network-only',
      });
      if (!error) essentialLinks.value = data.datas;
    };
    await dataProcessor();

    return {
      essentialLinks,
      dataProcessor,
    };
  },
});
</script>
