import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="text-center space-y-6 p-8">
        <h1 className="text-6xl font-bold text-slate-900">Todo App</h1>
        <p className="text-xl text-slate-600">
          Manage your tasks with ease
        </p>
        <div className="flex gap-4 justify-center mt-8">
          <Link
            href="/auth/signin"
            className="px-6 py-3 bg-slate-900 text-white rounded-lg hover:bg-slate-800 transition"
          >
            Sign In
          </Link>
          <Link
            href="/auth/signup"
            className="px-6 py-3 bg-white text-slate-900 border border-slate-300 rounded-lg hover:bg-slate-50 transition"
          >
            Sign Up
          </Link>
        </div>
      </div>
    </div>
  );
}
