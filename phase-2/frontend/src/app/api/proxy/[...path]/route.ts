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

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

async function proxyRequest(request: NextRequest, path: string[]) {
  const pathname = path.join("/");
  const searchParams = request.nextUrl.searchParams.toString();
  const url = `${BACKEND_URL}/api/${pathname}${searchParams ? `?${searchParams}` : ""}`;

  // Get all cookies from Next.js request
  const cookieStore = await cookies();
  const sessionToken = cookieStore.get("better-auth.session_token");

  console.log("Proxy: Forwarding to FastAPI:", url);
  console.log(
    "Proxy: Session token:",
    sessionToken?.value ? "PRESENT" : "MISSING",
  );

  // Build Cookie header from Better Auth session
  const cookieHeader = sessionToken
    ? `better-auth.session_token=${sessionToken.value}`
    : "";

  // Forward the request to FastAPI with cookies
  const response = await fetch(url, {
    method: request.method,
    headers: {
      "Content-Type": "application/json",
      // Forward Better Auth session cookie to FastAPI
      ...(cookieHeader ? { Cookie: cookieHeader } : {}),
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
  return new NextResponse(data, {
    status: response.status,
    headers: {
      "Content-Type": "application/json",
    },
  });
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
