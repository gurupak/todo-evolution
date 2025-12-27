/**
 * API Configuration
 * Uses Next.js API proxy (/api/proxy/*) to avoid cross-origin cookie issues
 * The proxy forwards requests to the FastAPI backend at localhost:8000
 */
export const API_URL = process.env.NEXT_PUBLIC_API_URL || "/api/proxy";
export const APP_URL =
  process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000";
