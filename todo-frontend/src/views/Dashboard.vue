<template>
  <div class="min-h-screen bg-gray-50 py-10 px-6">
    <div class="max-w-3xl mx-auto bg-white shadow-xl rounded-2xl p-8">
      <!-- Header -->
      <h1 class="text-4xl font-extrabold text-center text-gray-900 mb-6">
        🚀 My Task Manager
      </h1>
      <p class="text-center text-gray-500 mb-8">
        Stay organized and boost your productivity.
      </p>

      <!-- Add Todo -->
      <div class="flex mb-8">
        <input
          v-model="newTodo"
          placeholder="What needs to be done?"
          class="flex-1 border px-4 py-3 rounded-lg text-gray-800 shadow-sm focus:ring-2 focus:ring-indigo-400"
        />
        <button
          @click="addTodo"
          class="ml-3 bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-3 rounded-lg shadow transition"
        >
          ➕ Add Task
        </button>
      </div>

      <!-- Alert / Toast -->
      <transition name="toast">
        <div
          v-if="alertMessage"
          :class="alertType === 'success' ? 'bg-green-500' : 'bg-red-500'"
          class="fixed top-5 right-5 text-white px-6 py-3 rounded-lg shadow-lg font-medium z-50"
        >
          {{ alertMessage }}
        </div>
      </transition>

      <!-- Todo List -->
      <transition-group name="list" tag="ul" class="space-y-4">
        <li
          v-for="todo in todos"
          :key="todo.id"
          class="flex justify-between items-center bg-gray-100 px-5 py-4 rounded-xl shadow hover:shadow-md transition"
        >
          <!-- Task Info -->
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

          <!-- Actions -->
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
      </transition-group>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";

const todos = ref([]);
const newTodo = ref("");
const alertMessage = ref("");
const alertType = ref("success");

const fetchTodos = async () => {
  try {
    const { data } = await api.get("/todo/");
    todos.value = data;
  } catch {
    showAlert("❌ Failed to fetch todos", "error");
  }
};

const addTodo = async () => {
  if (!newTodo.value) return;
  try {
    await api.post("/todo/", { title: newTodo.value });
    newTodo.value = "";
    fetchTodos();
    showAlert("✅ Todo added successfully!", "success");
  } catch {
    showAlert("❌ Failed to add todo", "error");
  }
};

const completeTodo = async (id) => {
  try {
    await api.put(`/todo/${id}/complete`);
    fetchTodos();
    showAlert("🎉 Task completed!", "success");
  } catch {
    showAlert("❌ Failed to complete todo", "error");
  }
};

const deleteTodo = async (id) => {
  try {
    await api.delete(`/todo/${id}`);
    fetchTodos();
    showAlert("🗑 Todo deleted successfully", "success");
  } catch {
    showAlert("❌ Failed to delete todo", "error");
  }
};

const showAlert = (msg, type = "success") => {
  alertMessage.value = msg;
  alertType.value = type;
  setTimeout(() => (alertMessage.value = ""), 3000);
};

onMounted(fetchTodos);
</script>

<style>
.line-through {
  text-decoration: line-through;
  transition: color 0.3s ease, text-decoration 0.3s ease;
}

/* Toast animation */
.toast-enter-active {
  animation: bounceIn 0.6s;
}
.toast-leave-active {
  animation: fadeOut 0.5s forwards;
}

@keyframes bounceIn {
  0% { transform: translateY(-30px); opacity: 0; }
  50% { transform: translateY(10px); opacity: 1; }
  70% { transform: translateY(-5px); }
  100% { transform: translateY(0); }
}

@keyframes fadeOut {
  to { opacity: 0; transform: translateY(-20px); }
}

/* Smooth list transitions */
.list-enter-active, .list-leave-active {
  transition: all 0.4s ease;
}
.list-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}
.list-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
