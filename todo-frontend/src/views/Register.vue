<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="w-full max-w-md bg-white rounded-2xl shadow-lg p-8">
      <!-- Header -->
      <h2 class="text-3xl font-bold text-gray-800 text-center mb-6">Create Account ✨</h2>
      <p class="text-gray-500 text-center mb-8">Register to manage your tasks</p>

      <!-- Email -->
      <div class="mb-4">
        <label class="block text-gray-600 mb-1">Email</label>
        <input
          v-model="email"
          type="email"
          placeholder="you@example.com"
          class="w-full px-4 py-2 border rounded-lg shadow-sm focus:ring-2 focus:ring-blue-400 focus:outline-none text-gray-800"
        />
      </div>

      <!-- Password -->
      <div class="mb-6">
        <label class="block text-gray-600 mb-1">Password</label>
        <input
          v-model="password"
          type="password"
          placeholder="Enter your password"
          class="w-full px-4 py-2 border rounded-lg shadow-sm focus:ring-2 focus:ring-blue-400 focus:outline-none text-gray-800"
        />
      </div>

      <!-- Register Button -->
      <button
        @click="handleRegister"
        class="w-full bg-green-500 hover:bg-green-600 text-white font-medium px-4 py-2 rounded-lg shadow transition"
      >
        📝 Register
      </button>

      <!-- Divider -->
      <div class="flex items-center my-6">
        <hr class="flex-1 border-gray-300" />
        <span class="mx-3 text-gray-400 text-sm">OR</span>
        <hr class="flex-1 border-gray-300" />
      </div>

      <!-- Already have account -->
      <p class="text-center text-gray-600">
        Already have an account?
        <a href="/login" class="text-blue-500 hover:underline">Login</a>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { register } from "../services/api";

const email = ref("");
const password = ref("");

const handleRegister = async () => {
  try {
    await register(email.value, password.value);
    alert("✅ Registration successful! Please login.");
    window.location.href = "/login";
  } catch (err) {
    alert(err.response?.data?.msg || "Registration failed");
  }
};
</script>
