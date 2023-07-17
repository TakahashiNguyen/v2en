<template>
  <q-page class="justify-center">
    <div class="account-page center-of-parent">
      <div class="account-form">
        <h1 class="account-title">Welcome back!</h1>
        <h2 class="account-subtitle">We're so excited to see you again!</h2>
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="emailOrUsername" class="form-label">Username</label>
            <input
              id="emailOrUsername"
              v-model="emailOrUsername"
              type="text"
              class="form-control"
              required
            />
          </div>
          <div class="form-group">
            <label for="password" class="form-label">Password</label>
            <input
              id="password"
              v-model="password"
              type="password"
              class="form-control"
              required
            />
          </div>
          <button type="submit" class="btn btn-primary btn-block">Login</button>
        </form>
        <div class="forgot-password">
          <a href="#">Forgot your password?</a>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useMutation } from 'villus';
import router from 'src/router';
import { LOGIN_MUTATION } from 'src/graphql';

export default defineComponent({
  props: {
    user: {
      type: [Object, String],
      required: true,
    },
  },

  setup(props) {
    if (props.user) router.push('/profile');

    const emailOrUsername = ref('');
    const password = ref('');

    const { execute } = useMutation(LOGIN_MUTATION);

    const submitForm = async () => {
      try {
        const variables = {
          loginUser: {
            username: emailOrUsername.value,
            password: password.value,
          },
        };
        const response = await execute(variables);

        localStorage.setItem('token', response.data.LogIn);

        window.location.reload();
      } catch (error) {
        console.error(error);
      }
    };

    return {
      emailOrUsername,
      password,
      submitForm,
    };
  },
});
</script>
