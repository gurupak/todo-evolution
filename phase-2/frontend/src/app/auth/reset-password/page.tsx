"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { authClient } from "@/lib/auth-client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

/**
 * Reset Password page
 * Allows users to set a new password using a reset token
 */
export default function ResetPasswordPage() {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [tokenValid, setTokenValid] = useState(true);
  
  const searchParams = useSearchParams();
  const token = searchParams.get("token");
  const email = searchParams.get("email");

  // Validate the reset token when the page loads
  useEffect(() => {
    if (!token) {
      setError("Invalid or missing reset token");
      setTokenValid(false);
      return;
    }

    // In a real app, you would validate the token with the backend
    // For now, we'll assume the token is valid if it exists
    if (token && token.length > 0) {
      setTokenValid(true);
    } else {
      setError("Invalid reset token");
      setTokenValid(false);
    }
  }, [token]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");
    setMessage("");

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      setIsLoading(false);
      return;
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters");
      setIsLoading(false);
      return;
    }

    try {
      // Use Better Auth's reset password functionality
      const result = await authClient.resetPassword({
        newPassword: password,
        token: token!,
        email: email || "", // Email is also needed for verification
      });

      if (result?.error) {
        setError(result.error.message || "Failed to reset password");
      } else {
        setMessage("Password reset successfully! You can now sign in with your new password.");
      }
    } catch (err) {
      console.error("Reset password error:", err);
      setError("An error occurred. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  if (!tokenValid) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 p-4">
        <div className="max-w-md w-full space-y-8">
          <div className="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-md text-center">
            <h2 className="text-xl font-bold text-red-600 dark:text-red-400">
              Invalid Reset Link
            </h2>
            <p className="mt-2 text-gray-600 dark:text-gray-400">
              The password reset link is invalid or has expired.
            </p>
            <div className="mt-6">
              <Link
                href="/auth/forgot-password"
                className="text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300 font-medium"
              >
                Request a new reset link
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 p-4">
      <div className="max-w-md w-full space-y-8">
        <div className="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-md">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              Reset Your Password
            </h2>
            <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
              Enter your new password below
            </p>
          </div>

          <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
            {error && (
              <div className="bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300 p-3 rounded-md text-sm">
                {error}
              </div>
            )}

            {message ? (
              <div className="bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300 p-3 rounded-md text-sm">
                {message}
              </div>
            ) : (
              <>
                <div>
                  <Label htmlFor="password" className="text-gray-700 dark:text-gray-300">
                    New Password
                  </Label>
                  <Input
                    id="password"
                    name="password"
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    disabled={isLoading}
                    className="mt-1 block w-full"
                    placeholder="Enter new password"
                  />
                </div>

                <div>
                  <Label htmlFor="confirmPassword" className="text-gray-700 dark:text-gray-300">
                    Confirm New Password
                  </Label>
                  <Input
                    id="confirmPassword"
                    name="confirmPassword"
                    type="password"
                    required
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    disabled={isLoading}
                    className="mt-1 block w-full"
                    placeholder="Confirm new password"
                  />
                </div>

                <div>
                  <Button
                    type="submit"
                    disabled={isLoading}
                    className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                  >
                    {isLoading ? "Resetting..." : "Reset Password"}
                  </Button>
                </div>
              </>
            )}

            {!message && (
              <div className="text-center">
                <Link
                  href="/auth/signin"
                  className="text-sm text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300 font-medium"
                >
                  Back to sign in
                </Link>
              </div>
            )}
          </form>
        </div>
      </div>
    </div>
  );
}