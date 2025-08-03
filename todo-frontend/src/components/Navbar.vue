<template>
  <nav class="bg-indigo-600 text-white px-6 py-3 flex justify-between items-center shadow">
    <!-- Logo -->
    <h1 class="text-xl font-bold">✅ ToDo App</h1>

    <!-- Right Side -->
    <div class="flex items-center gap-4">
      <!-- Show user info if available -->
      <span v-if="userName" class="font-medium">Hi, {{ userName }} 👋</span>
      <img 
        v-if="userPicture" 
        :src="userPicture" 
        alt="profile" 
        class="w-8 h-8 rounded-full border"
      />

      <!-- Logout Button -->
      <button 
        @click="logout" 
        class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded-lg text-sm transition">
        Logout
      </button>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from "vue-router";
import { ref, onMounted } from "vue";

const router = useRouter();
const userName = ref("");
const userPicture = ref("");

// ✅ Load user info from localStorage
onMounted(() => {
  userName.value = localStorage.getItem("user_name") || "";
  userPicture.value = localStorage.getItem("user_picture") || "";
});

// ✅ Logout
const logout = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("user_email");
  localStorage.removeItem("user_name");
  localStorage.removeItem("user_picture");
  router.push("/login"); // redirect to login
};
</script>
