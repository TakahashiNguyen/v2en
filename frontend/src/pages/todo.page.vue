<template>
  <div>
    <div v-if="error" class="user-indo">
      <h2>Something went wrong</h2>
      <p>{{ error.message }}</p>
    </div>
    <div v-else>
      <h1>Todo List</h1>
      <div v-if="isDone">
        <todoTag
          v-for="todo in data.todos"
          :key="todo"
          v-bind="todo"
          :delete-todo="deleteTodo"
          :update-todo="updateTodo"
        >
        </todoTag>
      </div>
      <form @submit.prevent="addTodo">
        <input type="text" v-model="newTodoText" data-cy="todoTextField" />
        <button type="submit" data-cy="todoSubmitButton">Add</button>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { useMutation, useQuery } from 'villus';
import { defineComponent, ref } from 'vue';
import { TODO_GET, TODO_ADD, TODO_REMOVE, TODO_UPDATE } from 'src/graphql';
import todoTag from 'src/components/todo.tag.vue';

export default defineComponent({
  components: {
    todoTag,
  },
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
    async updateTodo(index: string) {
      const { error } = await useMutation(TODO_UPDATE).execute({
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
