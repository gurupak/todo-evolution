import { createAuthClient } from "better-auth/react";

/**
 * Better Auth client for React components
 * Provides hooks and utilities for authentication in client components
 * Points to /api/auth/* endpoints served by Next.js (same origin)
 */
export const authClient = createAuthClient({
  baseURL:
    process.env.FRONTEND_URL ||
    "https://noble-perfection-production-7c4a.up.railway.app", // Next.js app serves Better Auth at /api/auth/*
  fetchOptions: {
    credentials: "include", // Include cookies in requests (required for auth)
    cache: "no-store",
  },
});

export const { signIn, signUp, signOut, useSession } = authClient;
