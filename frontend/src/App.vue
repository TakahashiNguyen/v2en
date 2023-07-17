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
import { useMutation } from 'villus';
import { LOGOUT_MUTATION } from './graphql';
import { userMutation } from './router';

export default defineComponent({
  methods: {
    async logoutMutation(username: string, token: string) {
      const { execute } = useMutation(LOGOUT_MUTATION, {});
      await execute({ username: username, token: token });
    },
  },
  setup() {
    userMutation('');
    return { userMutation: userMutation };
  },
});
</script>
