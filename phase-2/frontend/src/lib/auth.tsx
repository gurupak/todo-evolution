import { betterAuth } from "better-auth";
import { Pool } from "pg";

/**
 * Better Auth server instance
 * This handles authentication, session management, and JWT token generation
 * Used in API routes (app/api/auth/[...all]/route.ts)
 */
export const auth = betterAuth({
  baseURL: process.env.NEXT_PUBLIC_FRONTEND_URL || "http://localhost:3000",
  database: new Pool({
    connectionString: process.env.DATABASE_URL,
  }),
  secret: process.env.BETTER_AUTH_SECRET!,
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Simplified for Phase II
    sendResetPassword: async ({user, url, token}, request) => {
      // This function is required for password reset to work
      console.log(`Password reset email would be sent to ${user.email}`);
      console.log(`Reset URL: ${url}`);
      // In production, you would send an actual email here using your email provider
    },
  },
  passwordReset: {
    enabled: true,
  },
  email: {
    enabled: true,
    provider: {
      type: "smtp",
      host: process.env.SMTP_HOST || "smtp.gmail.com", // Can use Gmail or other SMTP provider
      port: parseInt(process.env.SMTP_PORT || "587"),
      auth: {
        user: process.env.SMTP_USER || "", // Your email
        pass: process.env.SMTP_PASSWORD || "", // Your email password or app password
      },
      from: process.env.SMTP_FROM || "noreply@yourdomain.com", // From email address
    },
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
  // Disable CSRF check for development
  csrf: {
    enabled: false
  }
});
