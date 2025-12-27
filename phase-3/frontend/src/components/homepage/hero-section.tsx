"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

/**
 * Hero Section Component
 * Main landing section with headline, subheadline, and dual CTAs with animations
 * Per FR-007 to FR-011
 */
export function HeroSection() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const scrollToDemo = () => {
    const demoSection = document.querySelector("#demo");
    if (demoSection) {
      demoSection.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <section
      id="home"
      className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-blue-900 dark:to-purple-900"
    >
      {/* Parallax Background - Will be enhanced in T021 */}
      <div className="absolute inset-0 bg-grid-pattern opacity-10"></div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-32 text-center">
        {/* Headline - FR-008 with slide-in from left */}
        <h1
          className={`text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 dark:text-white mb-6 transition-all duration-1000 ${
            mounted ? "opacity-100 translate-x-0" : "opacity-0 -translate-x-12"
          }`}
        >
          AI-Powered Task Management
          <br />
          <span
            className={`text-blue-600 dark:text-blue-400 inline-block transition-all duration-1000 ${
              mounted ? "opacity-100 translate-x-0" : "opacity-0 translate-x-12"
            }`}
            style={{ transitionDelay: "200ms" }}
          >
            That Understands You
          </span>
        </h1>

        {/* Subheadline - FR-009 with fade-in */}
        <p
          className={`text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-12 max-w-3xl mx-auto transition-all duration-1000 ${
            mounted ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
          }`}
          style={{ transitionDelay: "400ms" }}
        >
          Chat naturally with AI to manage tasks effortlessly. No complex forms,
          just conversation. Todo-Evolution brings intelligent task management
          to your workflow.
        </p>

        {/* CTAs - FR-010, FR-011 with fade-in */}
        <div
          className={`flex flex-col sm:flex-row gap-4 justify-center transition-all duration-1000 ${
            mounted ? "opacity-100 scale-100" : "opacity-0 scale-95"
          }`}
          style={{ transitionDelay: "600ms" }}
        >
          <Link
            href="/auth/signup"
            className="px-8 py-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-lg font-semibold shadow-lg hover:shadow-xl"
          >
            Get Started Free
          </Link>
          <button
            onClick={scrollToDemo}
            className="px-8 py-4 bg-white dark:bg-gray-800 text-gray-900 dark:text-white border-2 border-gray-300 dark:border-gray-600 rounded-lg hover:border-blue-600 dark:hover:border-blue-400 transition-colors text-lg font-semibold"
          >
            Watch Demo
          </button>
        </div>

        {/* Optional: Feature highlights with staggered fade-in */}
        <div
          className={`mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto transition-all duration-1000 ${
            mounted ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
          }`}
          style={{ transitionDelay: "800ms" }}
        >
          <div className="text-center">
            <div className="text-4xl mb-2">🤖</div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
              AI Assistant
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Natural language understanding
            </p>
          </div>
          <div className="text-center">
            <div className="text-4xl mb-2">⚡</div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
              Real-Time Sync
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Instant updates across devices
            </p>
          </div>
          <div className="text-center">
            <div className="text-4xl mb-2">🔒</div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
              Secure & Private
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Enterprise-grade security
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
