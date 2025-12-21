import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

/**
 * Middleware - Currently disabled for debugging
 * Authentication check handled in page components
 */
export function middleware(request: NextRequest) {
  // Pass through all requests - auth handled client-side
  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*"],
};
