import Link from "next/link";
import { UserMenu } from "./user-menu";

interface HeaderProps {
  user: { id: string; name?: string; email: string } | null;
}

/**
 * Header component with branding and user menu
 * Displayed at the top of protected pages (dashboard)
 */
export function Header({ user }: HeaderProps) {
  return (
    <header className="bg-white dark:bg-gray-800 shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link href="/dashboard" className="flex items-center space-x-3">
              <div className="bg-blue-600 text-white w-10 h-10 rounded-lg flex items-center justify-center font-bold text-xl">
                T
              </div>
              <span className="text-xl font-bold text-gray-900 dark:text-white">
                Todo App
              </span>
            </Link>
          </div>

          <UserMenu user={user} />
        </div>
      </div>
    </header>
  );
}
