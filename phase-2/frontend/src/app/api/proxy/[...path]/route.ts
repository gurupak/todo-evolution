import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";

/**
 * API Proxy Route
 * Proxies all requests to /api/proxy/* to the FastAPI backend
 * This allows the frontend and backend to appear on the same origin,
 * avoiding cross-origin cookie issues.
 *
 * The proxy forwards Better Auth session cookies from the Next.js app
 * to the FastAPI backend so it can validate sessions.
 */

const BACKEND_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

async function proxyRequest(request: NextRequest, path: string[]) {
  const pathname = path.join("/");
  const searchParams = request.nextUrl.searchParams.toString();
  const url = `${BACKEND_URL}/api/${pathname}${searchParams ? `?${searchParams}` : ""}`;

  // Get all cookies from Next.js request
  const cookieStore = await cookies();

  // Better Auth uses different cookie names, get all cookies that start with "better-auth" or "__Secure-better-auth"
  const allCookies = cookieStore.getAll();
  console.log("Proxy: All cookies:", allCookies.map(c => c.name).join(", "));

  // Filter for Better Auth related cookies
  const betterAuthCookies = allCookies.filter(cookie =>
    cookie.name.includes('better-auth')
  );

  console.log("Proxy: Better Auth cookies found:", betterAuthCookies.length);

  // Build Cookie header from Better Auth cookies
  const cookieHeaders: string[] = [];
  betterAuthCookies.forEach(cookie => {
    cookieHeaders.push(`${cookie.name}=${cookie.value}`);
  });

  const cookieHeader = cookieHeaders.join("; ");

  // Forward the request to FastAPI with cookies
  const response = await fetch(url, {
    method: request.method,
    headers: {
      "Content-Type": "application/json",
      // Forward Better Auth session cookies to FastAPI
      ...(cookieHeader ? { Cookie: cookieHeader } : {}),
      // Forward other headers that might be needed
      "Accept": "application/json",
      // Forward authorization header if present
      ...(request.headers.get("authorization") ? { "Authorization": request.headers.get("authorization")! } : {}),
      // Forward user-agent for security checks
      "User-Agent": request.headers.get("user-agent") || "NextJS-Proxy",
    },
    body:
      request.method !== "GET" && request.body
        ? await request.text()
        : undefined,
  });

  // Get response data
  const data = await response.text();

  console.log("Proxy: FastAPI response status:", response.status);
  if (response.status !== 200) {
    console.log("Proxy: FastAPI error response:", data);
  }

  // Create Next.js response with the same status and data
  const nextResponse = new NextResponse(data, {
    status: response.status,
    headers: {
      "Content-Type": "application/json",
      // Add CORS headers to the response
      "Access-Control-Allow-Origin": request.headers.get("origin") || "*",
      "Access-Control-Allow-Credentials": "true",
      "Access-Control-Allow-Headers": "Content-Type, Authorization",
    },
  });

  return nextResponse;
}

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> },
) {
  const { path } = await params;
  return proxyRequest(request, path);
}

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> },
) {
  const { path } = await params;
  return proxyRequest(request, path);
}

export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> },
) {
  const { path } = await params;
  return proxyRequest(request, path);
}

export async function PATCH(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> },
) {
  const { path } = await params;
  return proxyRequest(request, path);
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> },
) {
  const { path } = await params;
  return proxyRequest(request, path);
}

// Add OPTIONS method for CORS preflight
export async function OPTIONS(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> },
) {
  const response = new NextResponse(null, {
    status: 200,
    headers: {
      "Access-Control-Allow-Origin": request.headers.get("origin") || "*",
      "Access-Control-Allow-Methods": "GET, POST, PUT, PATCH, DELETE, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type, Authorization, Cookie",
      "Access-Control-Allow-Credentials": "true",
    },
  });
  return response;
}
