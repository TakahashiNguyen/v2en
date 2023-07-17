<template>
  <Suspense>
    <router-view
      :userMutation="userMutation"
      :logoutMutation="logoutMutation"
    />
  </Suspense>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useClient, useMutation, fetch, cache } from 'villus';
import { LOGOUT_MUTATION, graphqlUrl } from './graphql';
import { userMutation } from './router';

export default defineComponent({
  methods: {
    async logoutMutation(username: string, token: string) {
      const { execute } = useMutation(LOGOUT_MUTATION, {});
      await execute({ username: username, token: token });
    },
  },
  setup() {
    useClient({
      url: graphqlUrl,
      use: [cache(), fetch()],
    });
    return { userMutation: userMutation };
  },
});
</script>
