<template>
  <div>
    <h1>Todo List</h1>
    <div v-for="(todo, index) in todos" :key="index">
      <input type="checkbox" v-model="todo.completed" />
      <span :class="{ completed: todo.completed }">{{ todo.text }}</span>
      <button @click="deleteTodo(index)">Delete</button>
    </div>
    <form @submit.prevent="addTodo">
      <input type="text" v-model="newTodoText" />
      <button type="submit">Add</button>
    </form>
  </div>
</template>

<script lang="ts">
import { useMutation, useQuery } from 'villus';
import { defineComponent, ref } from 'vue';
import { TODO_GET, TODO_ADD } from 'src/graphql';

export default defineComponent({
  async setup() {
    const { data } = useQuery({
      query: TODO_GET,
      cachePolicy: 'network-only',
    });
    const newTodoText = ref('');

    return {
      todos: data.value,
      newTodoText: newTodoText,
    };
  },
  methods: {
    async addTodo() {
      if (this.newTodoText.trim() !== '') {
        const newTodo = (
          await useMutation(TODO_ADD, {}).execute({
            newTodo: {
              jobDescription: this.newTodoText.trim(),
              deadline: '06-02-2006',
              finished: false,
            },
          })
        ).data;
        this.newTodoText = '';
      }
    },
    deleteTodo(index: number) {
      this.todos.splice(index, 1);
    },
  },
});
</script>

<style>
.completed {
  text-decoration: line-through;
}
</style>
