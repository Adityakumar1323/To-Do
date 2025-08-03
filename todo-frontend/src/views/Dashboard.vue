<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navbar -->
    <Navbar @logout="logout" />

    <!-- Main content -->
    <div class="max-w-3xl mx-auto bg-white shadow-xl rounded-2xl p-8 mt-10">
      <h1 class="text-3xl font-bold text-gray-800 mb-6">📋 My Tasks</h1>

      <!-- Add Task -->
      <div class="flex mb-6">
        <input
          v-model="newTodo"
          placeholder="Enter a new task..."
          class="flex-1 border px-4 py-3 rounded-lg text-gray-800 shadow-sm focus:ring-2 focus:ring-indigo-400"
        />
        <button
          @click="addTodo"
          class="ml-3 bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-3 rounded-lg shadow transition"
        >
          ➕ Add
        </button>
      </div>

      <!-- Task List -->
      <ul v-if="todos.length > 0" class="space-y-4">
        <li
          v-for="todo in todos"
          :key="todo.id"
          class="flex justify-between items-center bg-gray-100 px-5 py-4 rounded-xl shadow hover:shadow-md transition"
        >
          <div>
            <h2
              class="font-semibold text-lg text-gray-900"
              :class="{ 'line-through text-gray-400': todo.completed }"
            >
              {{ todo.title }}
            </h2>
            <p class="text-sm text-gray-500 mt-1">
              {{ todo.completed ? "✅ Completed" : "⏳ Pending" }}
            </p>
          </div>

          <div class="space-x-2">
            <button
              v-if="!todo.completed"
              @click="completeTodo(todo.id)"
              class="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded-lg shadow transition"
            >
              Mark Done
            </button>
            <button
              @click="deleteTodo(todo.id)"
              class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded-lg shadow transition"
            >
              Delete
            </button>
          </div>
        </li>
      </ul>

      <p v-else class="text-center text-gray-500 mt-6">
        No tasks yet. Add your first one 🚀
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import API from "../services/api";
import Navbar from "../components/Navbar.vue";

const todos = ref([]);
const newTodo = ref("");
const router = useRouter();

// Fetch todos (only once on mount)
const fetchTodos = async () => {
  try {
    const { data } = await API.get("/todo/");
    todos.value = data;
  } catch (err) {
    console.error("❌ Fetch todos failed", err);
  }
};

const addTodo = async () => {
  if (!newTodo.value.trim()) return;
  try {
    await API.post("/todo/", { title: newTodo.value });
    newTodo.value = "";
    fetchTodos();
  } catch (err) {
    console.error("❌ Failed to add todo", err);
  }
};

const completeTodo = async (id) => {
  try {
    await API.put(`/todo/${id}/complete`);
    fetchTodos();
  } catch (err) {
    console.error("❌ Failed to complete todo", err);
  }
};

const deleteTodo = async (id) => {
  try {
    await API.delete(`/todo/${id}`);
    fetchTodos();
  } catch (err) {
    console.error("❌ Failed to delete todo", err);
  }
};

// Logout (clear tokens + redirect)
const logout = () => {
  localStorage.clear();
  router.push("/login");
};

// Load tasks only once
onMounted(fetchTodos);
</script>
