<template>
  <div>
    <h1>Todo List</h1>
    <div v-if="isDone">
      <div v-for="(todo, index) in data.todos" :key="index">
        <input type="checkbox" v-model="todo.finished" />
        <span :class="{ completed: todo.finished }">{{
          todo.jobDescription
        }}</span>
        <button @click="deleteTodo(index)">Delete</button>
      </div>
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
    const { data, isDone, execute } = useQuery({
      query: TODO_GET,
      cachePolicy: 'network-only',
    });
    const newTodoText = ref('');

    return {
      data: data,
      isDone: isDone,
      newTodoText: newTodoText,
      todoQueryExecute: execute,
    };
  },
  methods: {
    async addTodo() {
      if (this.newTodoText.trim() !== '') {
        await useMutation(TODO_ADD, {}).execute({
          newTodo: {
            jobDescription: this.newTodoText.trim(),
            deadline: '06-02-2006',
            finished: false,
          },
        });
        await this.todoQueryExecute();
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
