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
import router from 'src/router';
import gql from 'graphql-tag';
import { useQuery } from 'villus';

const DATAS_QUERY = gql`
  query Query {
    datas {
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
  components: {
    EssentialData,
  },

  props: {
    id: { type: Number },

    user: {
      type: [Object, String],
      required: true,
    },

    data: {
      type: [Object],
    },
  },

  async setup(props) {
    if (!props.user) router.push('/login');

    const essentialLinks = ref([]);

    const { execute } = useQuery({ query: DATAS_QUERY });

    const dataProcessor = async (response: any) => {
      const result = await execute();
      essentialLinks.value = result.data.datas;
      if (response) essentialLinks.value = { ...result.data.datas, response };
    };
    await dataProcessor();

    return {
      essentialLinks,
      dataProcessor,
    };
  },
});
</script>
