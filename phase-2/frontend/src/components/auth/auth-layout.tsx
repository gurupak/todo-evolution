import React from "react";

interface AuthLayoutProps {
  children: React.ReactNode;
  title: string;
  description?: string;
}

/**
 * Layout component for authentication pages (sign in, sign up)
 * Provides consistent styling and branding across auth flows
 */
export function AuthLayout({ children, title, description }: AuthLayoutProps) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            Todo App
          </h1>
          {description && (
            <p className="text-gray-600 dark:text-gray-300">{description}</p>
          )}
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-8">
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
            {title}
          </h2>
          {children}
        </div>

        <div className="text-center mt-6 text-sm text-gray-600 dark:text-gray-400">
          Phase II - Full-Stack Web Application
        </div>
      </div>
    </div>
  );
}
