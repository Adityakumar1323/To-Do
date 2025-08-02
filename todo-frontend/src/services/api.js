import axios from "axios";

// ✅ Switch between local dev & Render automatically
const backendUrl =
  import.meta.env.MODE === "development"
    ? "http://127.0.0.1:5000/api"
    : "https://to-do-5-e2go.onrender.com/api";

const api = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:5000/api",
});

// ✅ Attach token to every request
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ✅ Automatically refresh access token when expired
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refreshToken = localStorage.getItem("refresh_token");
      if (refreshToken) {
        try {
          const { data } = await api.post(
            "/auth/refresh",
            {},
            { headers: { Authorization: `Bearer ${refreshToken}` } }
          );

          localStorage.setItem("access_token", data.access_token);

          // retry request with new token
          originalRequest.headers["Authorization"] = `Bearer ${data.access_token}`;
          return api(originalRequest);
        } catch (err) {
          console.error("Refresh token failed", err);
          localStorage.clear();
          window.location.href = "/login";
        }
      }
    }
    return Promise.reject(error);
  }
);

export default api;

// ---------- Auth APIs ----------
export const register = (email, password) =>
  api.post("/auth/register", { email, password });

export const login = (email, password) =>
  api.post("/auth/login", { email, password });

export const googleLogin = () => {
  // ✅ dynamic Google login URL
  const googleUrl =
    import.meta.env.MODE === "development"
      ? "http://127.0.0.1:5000/api/auth/google/login"
      : "https://to-do-5-e2go.onrender.com/api/auth/google/login";

  window.location.href = googleUrl;
};

// ---------- Todo APIs ----------
export const getTodos = () => api.get("/todo/");
export const createTodo = (title) => api.post("/todo/", { title });
export const updateTodo = (id, title) => api.put(`/todo/${id}`, { title });
export const deleteTodo = (id) => api.delete(`/todo/${id}`);
