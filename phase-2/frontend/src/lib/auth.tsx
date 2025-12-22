import { betterAuth } from "better-auth";
import { Pool } from "pg";

/**
 * Better Auth server instance
 * This handles authentication, session management, and JWT token generation
 * Used in API routes (app/api/auth/[...all]/route.ts)
 */
export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.DATABASE_URL,
  }),
  secret: process.env.BETTER_AUTH_SECRET!,
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Simplified for Phase II
  },
  session: {
    expiresIn: 60 * 60 * 24, // 24 hours
    updateAge: 60 * 60, // Update session every hour
    cookieCache: {
      enabled: true,
      maxAge: 60 * 60 * 24, // 24 hours
    },
  },
  advanced: {
    // Configure cookies for cross-browser support
    defaultCookieAttributes: {
      sameSite: process.env.NODE_ENV === "production" ? "none" : "lax", // Use 'none' for cross-site in production
      secure: process.env.NODE_ENV === "production", // Secure in production only
      httpOnly: true,
      path: "/",
    },
  },
});
