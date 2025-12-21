import axios from "axios";
import { API_URL } from "./constants";

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  // No need for withCredentials since we're using same-origin proxy
});

// Better Auth uses cookies, not JWT tokens - no need for Authorization header
