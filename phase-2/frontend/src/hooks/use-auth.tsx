"use client";

import { authClient } from "@/lib/auth-client";
import { useEffect, useRef } from "react";

/**
 * Custom hook for Better Auth session management
 * Provides authentication state and methods for client components
 */
export function useAuth() {
  const sessionResult = authClient.useSession();
  const hasLoadedOnce = useRef(false);

  useEffect(() => {
    if (sessionResult.data !== undefined && !hasLoadedOnce.current) {
      hasLoadedOnce.current = true;
    }
  }, [sessionResult.data]);

  return {
    session: sessionResult.data,
    user: sessionResult.data?.user,
    isLoading: sessionResult.isPending,
    isAuthenticated: !!sessionResult.data?.user,
    error: sessionResult.error,
    signIn: authClient.signIn,
    signUp: authClient.signUp,
    signOut: authClient.signOut,
  };
}
