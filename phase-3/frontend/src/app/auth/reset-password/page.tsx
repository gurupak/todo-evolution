import { Suspense } from "react";
import ResetPasswordContent from "./content";

/**
 * Reset Password page
 * Allows users to set a new password using a reset token
 */
export default function ResetPasswordPage() {
  return (
    <Suspense fallback={<div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 p-4">Loading...</div>}>
      <ResetPasswordContent />
    </Suspense>
  );
}