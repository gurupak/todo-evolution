import { NextRequest } from "next/server";
import { auth } from "@/lib/auth";

/**
 * Custom signout API route
 * Handles signout for both frontend and backend sessions
 */
export async function POST(request: NextRequest) {
  try {
    // Handle the signout via Better Auth
    // We need to properly format the request to match Better Auth's expectations
    const url = new URL(request.url);
    const signOutRequest = new Request(`${url.origin}/api/auth/sign-out`, {
      method: 'POST',
      headers: {
        ...Object.fromEntries(request.headers.entries()),
        'Content-Type': 'application/json',
      },
      body: await request.text(),
    });

    const response = await auth.handler(signOutRequest);
    return response;
  } catch (error) {
    console.error("Signout error:", error);
    return new Response(
      JSON.stringify({ error: "Signout failed" }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
}