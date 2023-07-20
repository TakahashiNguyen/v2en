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
export default {
  data() {
    return {
      todos: [
        { text: 'Learn Quasar', completed: false },
        { text: 'Build a todo app', completed: false },
        { text: 'Deploy to production', completed: false },
      ],
      newTodoText: '',
    };
  },
  methods: {
    addTodo() {
      if (this.newTodoText.trim() !== '') {
        this.todos.push({ text: this.newTodoText, completed: false });
        this.newTodoText = '';
      }
    },
    deleteTodo(index: number) {
      this.todos.splice(index, 1);
    },
  },
};
</script>

<style>
.completed {
  text-decoration: line-through;
}
</style>
