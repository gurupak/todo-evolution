"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { authClient } from "@/lib/auth-client";

export default function SignOutPage() {
  const router = useRouter();

  useEffect(() => {
    const signOutUser = async () => {
      try {
        // Sign out the user using Better Auth client
        await authClient.signOut();
      } catch (error) {
        console.error("Sign out error:", error);
      } finally {
        // Redirect to root page after signing out
        router.push("/");
        router.refresh();
      }
    };

    signOutUser();
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p className="mt-4 text-lg text-gray-600 dark:text-gray-400">
          Signing you out...
        </p>
      </div>
    </div>
  );
}