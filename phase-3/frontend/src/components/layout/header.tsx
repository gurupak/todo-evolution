"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { UserMenu } from "./user-menu";
import { ThemeToggle } from "@/components/theme/theme-toggle";

interface HeaderProps {
  user: { id: string; name?: string; email: string } | null;
}

/**
 * Header component with branding, navigation, and user menu
 * Displayed at the top of protected pages (dashboard, chat)
 *
 * @implements T053 - Add Chat navigation link
 */
export function Header({ user }: HeaderProps) {
  const pathname = usePathname();

  const navLinks = [
    { href: "/dashboard", label: "Dashboard" },
    { href: "/chat", label: "Chat" },
  ];

  return (
    <header className="bg-white dark:bg-gray-800 shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-8">
            {/* Logo/Brand */}
            <Link href="/dashboard" className="flex items-center space-x-3">
              <div className="bg-blue-600 text-white w-10 h-10 rounded-lg flex items-center justify-center font-bold text-xl">
                T
              </div>
              <span className="text-xl font-bold text-gray-900 dark:text-white">
                Todo App
              </span>
            </Link>

            {/* Navigation Links */}
            <nav className="hidden md:flex space-x-4">
              {navLinks.map((link) => {
                const isActive = pathname === link.href;
                return (
                  <Link
                    key={link.href}
                    href={link.href}
                    className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActive
                        ? "bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-200"
                        : "text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                    }`}
                  >
                    {link.label}
                  </Link>
                );
              })}
            </nav>
          </div>

          <div className="flex items-center space-x-4">
            <ThemeToggle />
            <UserMenu user={user} />
          </div>
        </div>
      </div>
    </header>
  );
}
