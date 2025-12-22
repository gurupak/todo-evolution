import axios from "axios";
import { API_URL } from "./constants";

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  // Important: Allow credentials to be sent with requests
  // This is handled by the proxy, but keeping for clarity
  withCredentials: true,
});

// Add response interceptor to handle authentication errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 || error.response?.status === 403) {
      // Redirect to login or handle auth error
      console.log("Authentication error, redirecting to login");
      // You might want to redirect to login page here
    }
    return Promise.reject(error);
  }
);

export default apiClient;

// Better Auth uses cookies, not JWT tokens - no need for Authorization header
