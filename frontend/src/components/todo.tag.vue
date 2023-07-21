<template>
  <q-item :data-cy="jobDescription + 'Section'">
    <input
      type="checkbox"
      v-model="$props.finished"
      @click="updateTodo(id)"
      :data-cy="jobDescription + 'Checkbox'"
    />
    <span
      :class="{ completed: finished }"
      :data-cy="jobDescription + 'Field'"
      >{{ jobDescription }}</span
    >
    <button @click="deleteTodo(id)" :data-cy="jobDescription + 'DeleteButton'">
      Delete
    </button>
  </q-item>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    id: {
      type: String,
    },
    finished: {
      type: Boolean,
    },
    jobDescription: {
      type: String,
    },
    updateTodo: {
      type: Function,
      required: true,
    },
    deleteTodo: {
      type: Function,
      required: true,
    },
  },
});
</script>
