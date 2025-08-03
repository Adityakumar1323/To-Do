<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center">
    <div class="w-full max-w-md bg-white shadow-lg rounded-xl p-8">
      <!-- Navbar / App Title -->
      <h1 class="text-center text-2xl font-bold text-indigo-600 mb-6">
        🚀 Task Manager
      </h1>

      <h2 class="text-xl font-semibold text-gray-800 text-center mb-4">Login</h2>

      <!-- Email / Password Login -->
      <form @submit.prevent="handleLogin" class="space-y-4">
        <input
          v-model="email"
          type="email"
          placeholder="Email"
          class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-400"
          required
        />
        <input
          v-model="password"
          type="password"
          placeholder="Password"
          class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-400"
          required
        />
        <button
          type="submit"
          class="w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 transition"
        >
          Login
        </button>
      </form>

      <!-- Google Login -->
      <button
        @click="googleLogin"
        class="w-full bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded-lg flex items-center justify-center mt-4"
      >
        <img
          src="https://developers.google.com/identity/images/g-logo.png"
          alt="Google Logo"
          class="w-5 h-5 mr-2"
        />
        Sign in with Google
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { login } from "../services/api";

const email = ref("");
const password = ref("");
const router = useRouter();
const route = useRoute();

const handleLogin = async () => {
  try {
    const { data } = await login(email.value, password.value);
    handleAuthSuccess(data);
  } catch (err) {
    alert(err.response?.data?.msg || "❌ Login failed");
  }
};

// ✅ Redirect user to backend Google login
const googleLogin = () => {
  window.location.href =
    "https://to-do-5-e2go.onrender.com/api/auth/google/login";
};

// ✅ Save tokens + redirect
const handleAuthSuccess = (data) => {
  localStorage.setItem("access_token", data.access_token);
  localStorage.setItem("refresh_token", data.refresh_token);
  localStorage.setItem("user_email", data.email || "");
  localStorage.setItem("user_name", data.name || "");
  localStorage.setItem("user_picture", data.picture || "");
  router.push("/"); // redirect to dashboard
};

// ✅ Handle Google redirect (tokens in query params)
onMounted(() => {
  if (route.query.access && route.query.refresh) {
    handleAuthSuccess({
      access_token: route.query.access,
      refresh_token: route.query.refresh,
      email: route.query.email,
      name: route.query.name,
      picture: route.query.picture,
    });

    // ✅ Clean URL params after storing tokens
    router.replace("/");
  }
});
</script>
