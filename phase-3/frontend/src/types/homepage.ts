/**
 * Homepage Types
 * Type definitions for homepage components and features
 */

export type ThemePreference = 'light' | 'dark' | 'system';

export interface ContactSubmission {
  name: string;
  email: string;
  subject?: string;
  message: string;
  submittedAt: Date;
}

export interface NavigationSection {
  id: string;
  label: string;
  href: string;
}

export interface FeatureCard {
  id: string;
  icon: string;
  title: string;
  description: string;
  learnMoreLink?: string;
}

export interface ContactEmailProps {
  name: string;
  email: string;
  subject?: string;
  message: string;
}
