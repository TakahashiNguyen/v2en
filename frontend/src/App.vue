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
import { useClient, useMutation, cache, defaultPlugins } from 'villus';
import { LOGOUT_MUTATION } from './graphql';
import { authPlugin, userMutation } from './router';
import { graphqlUrl } from './url';

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
      use: [cache(), authPlugin, ...defaultPlugins()],
    });
    return { userMutation: userMutation };
  },
});
</script>
