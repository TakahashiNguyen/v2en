<template>
  <q-item
    clickable
    tag="a"
    target="_blank"
    @click="
      eFunction();
      leftDrawer();
    "
    :data-cy="buttonName"
  >
    <q-item-section v-if="icon" avatar>
      <q-icon :name="icon" />
    </q-item-section>

    <q-item-section>
      <q-item-label>{{ title }}</q-item-label>
      <q-item-label caption>{{ caption }}</q-item-label>
    </q-item-section>
  </q-item>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import router from 'src/router';

export default defineComponent({
  props: {
    title: {
      type: String,
      required: true,
    },

    caption: {
      type: String,
      default: '',
      optional: true,
    },

    eFunction: {
      type: Function,
      default: () => router.push('/'),
      optional: true,
    },

    icon: {
      type: String,
      default: '',
      optional: true,
    },
    leftDrawer: {
      type: Function,
      required: true,
    },
  },
  setup(props) {
    return { buttonName: props.title + 'Button' };
  },
});
</script>
