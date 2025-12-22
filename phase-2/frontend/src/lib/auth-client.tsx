import { createAuthClient } from "better-auth/react";

/**
 * Better Auth client for React components
 * Provides hooks and utilities for authentication in client components
 * Points to /api/auth/* endpoints served by Next.js (same origin)
 */
export const authClient = createAuthClient({
  baseURL: typeof window !== 'undefined'
    ? window.location.origin
    : process.env.NEXT_PUBLIC_FRONTEND_URL || "http://localhost:3000", // Use the current origin in browser, fallback for SSR
  fetchOptions: {
    credentials: "include", // Include cookies in requests (required for auth)
    cache: "no-store",
  },
});

export const { signIn, signUp, signOut, useSession, forgotPassword, resetPassword } = authClient;
