import { betterAuth } from "better-auth";
import { Pool } from "pg";

/**
 * Better Auth configuration for CLI migrations
 * This file is used by @better-auth/cli migrate command
 */
export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.DATABASE_URL,
  }),
  secret: process.env.BETTER_AUTH_SECRET!,
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
  },
  session: {
    expiresIn: 60 * 60 * 24, // 24 hours
    updateAge: 60 * 60, // Update session every hour
  },
});
