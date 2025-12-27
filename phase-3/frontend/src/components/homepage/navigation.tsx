"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ThemeToggle } from "@/components/theme/theme-toggle";
import { NAVIGATION_SECTIONS } from "@/lib/constants/navigation";
import { useSectionObserver } from "@/hooks/use-section-observer";

/**
 * Homepage Navigation Component
 * Sticky header with logo, in-page scroll anchor links, Sign In/Sign Up buttons, and ThemeToggle
 * Per FR-001, FR-002, FR-006
 */
export function Navigation() {
  const activeSection = useSectionObserver();
  const [isScrolled, setIsScrolled] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollToSection = (href: string) => {
    const element = document.querySelector(href);
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
    }
  };

  // Prevent hydration mismatch - always render with transparent background initially
  const navClasses = `fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
    mounted && isScrolled
      ? "bg-white/95 dark:bg-gray-900/95 backdrop-blur-sm shadow-md"
      : "bg-transparent"
  }`;

  return (
    <nav className={navClasses} suppressHydrationWarning>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-3">
            <div className="bg-blue-600 text-white w-10 h-10 rounded-lg flex items-center justify-center font-bold text-xl">
              T
            </div>
            <span className="text-xl font-bold text-gray-900 dark:text-white">
              Todo-Evolution
            </span>
          </Link>

          {/* Navigation Links - Desktop */}
          <div className="hidden md:flex items-center space-x-8">
            {NAVIGATION_SECTIONS.map((section) => (
              <button
                key={section.id}
                onClick={() => scrollToSection(section.href)}
                className={`text-sm font-medium transition-colors ${
                  activeSection === section.id
                    ? "text-blue-600 dark:text-blue-400"
                    : "text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400"
                }`}
              >
                {section.label}
              </button>
            ))}
          </div>

          {/* Right Side - Theme Toggle & Auth Buttons */}
          <div className="flex items-center space-x-4">
            <ThemeToggle />
            <Link
              href="/auth/signin"
              className="text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
            >
              Sign In
            </Link>
            <Link
              href="/auth/signup"
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
            >
              Sign Up
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
