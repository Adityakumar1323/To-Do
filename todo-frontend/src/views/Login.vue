<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="w-full max-w-md bg-white rounded-2xl shadow-lg p-8">
      <!-- Header -->
      <h2 class="text-3xl font-bold text-gray-800 text-center mb-6">Welcome Back 👋</h2>
      <p class="text-gray-500 text-center mb-8">Login to manage your tasks</p>

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

      <!-- Login Button -->
      <button
        @click="handleLogin"
        class="w-full bg-blue-500 hover:bg-blue-600 text-white font-medium px-4 py-2 rounded-lg shadow transition"
      >
        🔑 Login
      </button>

      <!-- Divider -->
      <div class="flex items-center my-6">
        <hr class="flex-1 border-gray-300" />
        <span class="mx-3 text-gray-400 text-sm">OR</span>
        <hr class="flex-1 border-gray-300" />
      </div>

      <!-- Google Login -->
      <a
        :href="`${backendUrl}/api/auth/google/login`"
        class="w-full block text-center bg-red-500 hover:bg-red-600 text-white font-medium px-4 py-2 rounded-lg shadow transition"
      >
        Continue with Google
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import API from "../services/api";

const email = ref("");
const password = ref("");
const backendUrl = "http://127.0.0.1:5000"; // Flask backend

// ✅ handle normal login
const handleLogin = async () => {
  try {
    const { data } = await API.post("/auth/login", {
      email: email.value,
      password: password.value,
    });

    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token);
    if (data.email) {
      localStorage.setItem("user_email", data.email);
    }

    window.location.href = "/"; // redirect to dashboard
  } catch (err) {
    alert(err.response?.data?.msg || "Login failed");
  }
};

// ✅ handle Google redirect tokens
onMounted(() => {
  const params = new URLSearchParams(window.location.search);
  const accessToken = params.get("access_token");
  const refreshToken = params.get("refresh_token");
  const emailFromGoogle = params.get("email");

  if (accessToken && refreshToken) {
    localStorage.setItem("access_token", accessToken);
    localStorage.setItem("refresh_token", refreshToken);
    if (emailFromGoogle) {
      localStorage.setItem("user_email", emailFromGoogle);
    }

    // ✅ clear query params before redirect
    window.history.replaceState({}, document.title, "/");
    window.location.href = "/";
  }
});
</script>
