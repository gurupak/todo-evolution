"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";

/**
 * Developer Section Component
 * API overview, MCP server info, code preview, and documentation link with animations
 * Per FR-024 to FR-029
 */
export function DeveloperSection() {
  const [isVisible, setIsVisible] = useState(false);
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsVisible(true);
          }
        });
      },
      {
        threshold: 0.1,
        rootMargin: "0px 0px -100px 0px",
      },
    );

    if (sectionRef.current) {
      observer.observe(sectionRef.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <section
      id="developers"
      ref={sectionRef}
      className="relative py-24 bg-white dark:bg-gray-900 overflow-hidden"
    >
      {/* Floating Code Circles Animation */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="code-circle code-circle-1">
          <code className="text-blue-500 dark:text-blue-400 font-mono text-lg">
            {"{ }"}
          </code>
        </div>
        <div className="code-circle code-circle-2">
          <code className="text-green-500 dark:text-green-400 font-mono text-lg">
            {"[ ]"}
          </code>
        </div>
        <div className="code-circle code-circle-3">
          <code className="text-purple-500 dark:text-purple-400 font-mono text-lg">
            {"< />"}
          </code>
        </div>
        <div className="code-circle code-circle-4">
          <code className="text-orange-500 dark:text-orange-400 font-mono text-lg">
            {"( )"}
          </code>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
            Built for Developers
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Integrate Todo-Evolution into your applications with our powerful
            REST API and Model Context Protocol (MCP) server.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left: API Info with fade-in from left */}
          <div
            className={`space-y-6 transition-all duration-700 ${
              isVisible
                ? "opacity-100 translate-x-0"
                : "opacity-0 -translate-x-12"
            }`}
          >
            <div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                REST API
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-6">
                Full-featured REST API with JWT authentication. Manage tasks,
                conversations, and user data programmatically.
              </p>

              {/* API Features - FR-028 */}
              <ul className="space-y-3">
                <li className="flex items-start">
                  <svg
                    className="w-6 h-6 text-blue-600 dark:text-blue-400 mr-3 mt-0.5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <span className="text-gray-700 dark:text-gray-300">
                    <strong>CRUD Operations:</strong> Create, read, update, and
                    delete tasks
                  </span>
                </li>
                <li className="flex items-start">
                  <svg
                    className="w-6 h-6 text-blue-600 dark:text-blue-400 mr-3 mt-0.5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <span className="text-gray-700 dark:text-gray-300">
                    <strong>Conversation Management:</strong> Access AI chat
                    history
                  </span>
                </li>
                <li className="flex items-start">
                  <svg
                    className="w-6 h-6 text-blue-600 dark:text-blue-400 mr-3 mt-0.5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <span className="text-gray-700 dark:text-gray-300">
                    <strong>User Isolation:</strong> Secure multi-tenant
                    architecture
                  </span>
                </li>
                <li className="flex items-start">
                  <svg
                    className="w-6 h-6 text-blue-600 dark:text-blue-400 mr-3 mt-0.5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <span className="text-gray-700 dark:text-gray-300">
                    <strong>Webhook Support:</strong> Real-time event
                    notifications
                  </span>
                </li>
              </ul>
            </div>

            {/* MCP Server Info - FR-029 */}
            <div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                MCP Server Integration
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Connect AI agents directly to Todo-Evolution using the Model
                Context Protocol. Enable LLMs to manage tasks on behalf of users
                with built-in security and context awareness.
              </p>
            </div>

            {/* Authentication - FR-025 */}
            <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
              <div className="flex items-start">
                <svg
                  className="w-6 h-6 text-blue-600 dark:text-blue-400 mr-3 mt-0.5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                  />
                </svg>
                <div>
                  <h4 className="font-semibold text-blue-900 dark:text-blue-300 mb-1">
                    JWT Authentication
                  </h4>
                  <p className="text-sm text-blue-800 dark:text-blue-400">
                    Secure token-based authentication with automatic refresh and
                    expiration handling.
                  </p>
                </div>
              </div>
            </div>

            {/* CTA - FR-027 */}
            <div className="flex gap-4">
              <Link
                href="/developers"
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold"
              >
                View Full Documentation
              </Link>
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="px-6 py-3 bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors font-semibold"
              >
                View on GitHub
              </a>
            </div>
          </div>

          {/* Right: Code Snippet - FR-026 with slide-in from right */}
          <div
            className={`bg-gray-900 dark:bg-gray-950 rounded-xl p-6 shadow-2xl border border-gray-700 transition-all duration-700 ${
              isVisible
                ? "opacity-100 translate-x-0"
                : "opacity-0 translate-x-12"
            }`}
            style={{
              transitionDelay: isVisible ? "300ms" : "0ms",
            }}
          >
            <div className="flex items-center justify-between mb-4">
              <span className="text-sm text-gray-400">Example API Call</span>
              <div className="flex space-x-2">
                <div className="w-3 h-3 rounded-full bg-red-500"></div>
                <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                <div className="w-3 h-3 rounded-full bg-green-500"></div>
              </div>
            </div>
            <pre className="text-sm text-gray-300 overflow-x-auto">
              <code>{`// Create a new task
const response = await fetch('/api/tasks', {
  method: 'POST',
  headers: {
    'Authorization': \`Bearer \${token}\`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'Implement user authentication',
    priority: 'HIGH',
    status: 'PENDING'
  })
});

const task = await response.json();
console.log('Task created:', task);`}</code>
            </pre>
          </div>
        </div>
      </div>
    </section>
  );
}
