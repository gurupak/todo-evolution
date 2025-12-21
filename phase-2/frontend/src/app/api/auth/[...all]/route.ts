import { auth } from "src/lib/auth";

/**
 * Better Auth API route handler
 * Handles all authentication requests (/api/auth/*)
 */
export async function GET(request: Request) {
  return auth.handler(request);
}

export async function POST(request: Request) {
  return auth.handler(request);
}
