<template>
  <div>
    <div v-if="error" class="user-indo">
      <h2>Something went wrong</h2>
      <p>{{ error.message }}</p>
    </div>
    <div v-else>
      <h1>Todo List</h1>
      <div v-if="isDone">
        <div v-for="(todo, index) in data.todos" :key="index">
          <input type="checkbox" v-model="todo.finished" />
          <span :class="{ completed: todo.finished }">{{
            todo.jobDescription
          }}</span>
          <button @click="deleteTodo(todo.id)">Delete</button>
        </div>
      </div>
      <form @submit.prevent="addTodo">
        <input type="text" v-model="newTodoText" />
        <button type="submit">Add</button>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { useMutation, useQuery } from 'villus';
import { defineComponent, ref } from 'vue';
import { TODO_GET, TODO_ADD, TODO_REMOVE } from 'src/graphql';

export default defineComponent({
  async setup() {
    const { data, isDone, execute, error } = useQuery({
      query: TODO_GET,
      cachePolicy: 'network-only',
    });
    const newTodoText = ref('');

    return {
      data: data,
      error: error,
      isDone: isDone,
      newTodoText: newTodoText,
      todoQueryExecute: execute,
    };
  },
  methods: {
    async addTodo() {
      if (this.newTodoText.trim() !== '') {
        const { error } = await useMutation(TODO_ADD, {}).execute({
          newTodo: {
            jobDescription: this.newTodoText.trim(),
            deadline: '06-02-2006',
            finished: false,
          },
        });
        await this.todoQueryExecute();
        this.newTodoText = '';
        if (error) this.error = error;
      }
    },
    async deleteTodo(index: string) {
      const { error } = await useMutation(TODO_REMOVE, {}).execute({
        todoId: index,
      });
      await this.todoQueryExecute();
      if (error) this.error = error;
    },
  },
});
</script>

<style>
.completed {
  text-decoration: line-through;
}
</style>
