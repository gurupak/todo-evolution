# Data Model: Homepage & Theme System

**Feature**: 004-homepage  
**Date**: 2025-12-27  
**Phase**: 1 - Data Model Design

## Overview

This document defines the data structures for the homepage feature, contact form submissions, and theme preferences. The homepage is primarily a static marketing page with minimal server-side data requirements.

---

## Entity 1: Contact Form Submission

### Purpose
Captures user inquiries from the contact form for email delivery and optional persistence.

### Schema

```typescript
interface ContactSubmission {
  // Metadata
  id: string;                    // UUID v4
  submittedAt: Date;             // ISO 8601 timestamp
  ipAddress?: string;            // For spam prevention (optional)
  userAgent?: string;            // Browser info (optional)
  
  // User Input
  name: string;                  // 2-100 characters
  email: string;                 // Valid email format
  message: string;               // 10-1000 characters
  subject?: string;              // Optional, defaults to "New Contact Form"
  
  // Status
  status: 'pending' | 'sent' | 'failed' | 'spam';
  emailId?: string;              // Resend email ID (from API response)
  error?: string;                // Error message if failed
  retryCount: number;            // Number of send attempts
  sentAt?: Date;                 // When email was successfully sent
}
```

### Validation Rules

```typescript
import { z } from 'zod';

export const contactSubmissionSchema = z.object({
  name: z.string()
    .min(2, 'Name must be at least 2 characters')
    .max(100, 'Name must not exceed 100 characters')
    .regex(/^[a-zA-Z\s'-]+$/, 'Name contains invalid characters'),
  
  email: z.string()
    .email('Invalid email address')
    .max(255, 'Email must not exceed 255 characters')
    .toLowerCase(),
  
  message: z.string()
    .min(10, 'Message must be at least 10 characters')
    .max(1000, 'Message must not exceed 1000 characters')
    .trim(),
  
  subject: z.string()
    .max(200, 'Subject must not exceed 200 characters')
    .optional(),
});

export type ContactSubmissionInput = z.infer<typeof contactSubmissionSchema>;
```

### State Transitions

```
pending → sent (success)
pending → failed (retry < 3)
failed → sent (retry successful)
failed → failed (retry >= 3, permanent failure)
pending → spam (spam detection triggered)
```

### Storage Strategy

**Option 1: No Persistence (Recommended for MVP)**
- Contact submissions are sent via email immediately
- No database storage required
- Simpler implementation, fewer dependencies

**Option 2: Database Persistence (Future Enhancement)**
- Store in PostgreSQL (Neon DB already configured)
- Useful for admin dashboard, analytics
- Requires new table migration

```sql
-- Optional: Future enhancement
CREATE TABLE contact_submissions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  submitted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  ip_address INET,
  user_agent TEXT,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL,
  message TEXT NOT NULL,
  subject VARCHAR(200),
  status VARCHAR(20) NOT NULL DEFAULT 'pending',
  email_id VARCHAR(255),
  error TEXT,
  retry_count INTEGER NOT NULL DEFAULT 0,
  sent_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_contact_submissions_status ON contact_submissions(status);
CREATE INDEX idx_contact_submissions_submitted_at ON contact_submissions(submitted_at DESC);
```

---

## Entity 2: Theme Preference

### Purpose
Stores user's theme preference (light/dark/system) using next-themes automatic persistence.

### Schema

```typescript
interface ThemePreference {
  theme: 'light' | 'dark' | 'system';
  resolvedTheme: 'light' | 'dark';  // Actual applied theme
  systemTheme: 'light' | 'dark';    // OS preference
}
```

### Storage Strategy

**Client-Side Only (localStorage)**
- Managed automatically by next-themes
- Key: `theme` (configurable via `storageKey` prop)
- No server-side persistence needed
- Syncs across tabs automatically

```typescript
// Automatically stored by next-themes
localStorage.setItem('theme', 'dark');  // or 'light' or 'system'
```

### Implementation

```typescript
'use client';

import { useTheme } from 'next-themes';

function ThemeToggle() {
  const { theme, setTheme, resolvedTheme, systemTheme } = useTheme();
  
  return (
    <select value={theme} onChange={(e) => setTheme(e.target.value)}>
      <option value="light">Light</option>
      <option value="dark">Dark</option>
      <option value="system">System</option>
    </select>
  );
}
```

---

## Entity 3: Navigation Section

### Purpose
Defines sections of the homepage for scroll-based navigation highlighting.

### Schema

```typescript
interface NavigationSection {
  id: string;                    // HTML element ID (e.g., 'hero', 'features')
  label: string;                 // Display name in nav (e.g., 'Home', 'Features')
  href: string;                  // Scroll anchor (e.g., '#hero', '#features')
  order: number;                 // Display order in navigation
  isActive: boolean;             // Currently visible in viewport
}
```

### Static Configuration

```typescript
export const NAVIGATION_SECTIONS: NavigationSection[] = [
  { id: 'hero', label: 'Home', href: '#hero', order: 1, isActive: false },
  { id: 'features', label: 'Features', href: '#features', order: 2, isActive: false },
  { id: 'video-demo', label: 'Demo', href: '#video-demo', order: 3, isActive: false },
  { id: 'developers', label: 'Developers', href: '#developers', order: 4, isActive: false },
  { id: 'contact', label: 'Contact', href: '#contact', order: 5, isActive: false },
];
```

---

## Entity 4: Feature Card

### Purpose
Represents individual feature highlights displayed on the homepage.

### Schema

```typescript
interface FeatureCard {
  id: string;                    // Unique identifier
  icon: string;                  // Lucide icon name (e.g., 'MessageSquare')
  title: string;                 // Feature name (e.g., 'AI-Powered Chat')
  description: string;           // 2-3 sentence description
  learnMoreUrl?: string;         // Optional link to detailed docs
  order: number;                 // Display order
}
```

### Static Configuration (8-9 cards per CL-004)

```typescript
import { 
  MessageSquare, 
  Sparkles, 
  History, 
  Users, 
  Zap, 
  Target,
  Smartphone,
  Workflow,
  BarChart3 
} from 'lucide-react';

export const FEATURE_CARDS: FeatureCard[] = [
  {
    id: 'ai-chat',
    icon: 'MessageSquare',
    title: 'AI-Powered Chat',
    description: 'Manage tasks through natural conversation with our intelligent AI assistant.',
    order: 1,
  },
  {
    id: 'natural-language',
    icon: 'Sparkles',
    title: 'Natural Language Input',
    description: 'Add, update, and complete tasks using plain English—no complex syntax required.',
    order: 2,
  },
  {
    id: 'conversation-history',
    icon: 'History',
    title: 'Conversation History',
    description: 'Access your complete chat history with rename and delete capabilities.',
    order: 3,
  },
  {
    id: 'multi-user',
    icon: 'Users',
    title: 'Multi-User Support',
    description: 'Collaborate with your team using isolated, secure user workspaces.',
    order: 4,
  },
  {
    id: 'real-time',
    icon: 'Zap',
    title: 'Real-Time Updates',
    description: 'See changes instantly across all your devices with live synchronization.',
    order: 5,
  },
  {
    id: 'task-prioritization',
    icon: 'Target',
    title: 'Smart Prioritization',
    description: 'Automatically prioritize tasks based on deadlines, importance, and context.',
    order: 6,
  },
  {
    id: 'mobile-apps',
    icon: 'Smartphone',
    title: 'Mobile Ready',
    description: 'Access your tasks anywhere with our fully responsive web interface.',
    order: 7,
  },
  {
    id: 'api-integration',
    icon: 'Workflow',
    title: 'Developer API',
    description: 'Integrate Todo-Evolution into your workflow with our comprehensive REST API and MCP server.',
    order: 8,
  },
  {
    id: 'analytics',
    icon: 'BarChart3',
    title: 'Task Analytics',
    description: 'Track productivity trends and task completion rates with built-in analytics.',
    order: 9,
  },
];
```

---

## Entity 5: Email Template Data

### Purpose
Props passed to React Email components for rendering contact form emails.

### Schema

```typescript
interface ContactEmailProps {
  name: string;                  // Sender's name
  email: string;                 // Sender's email (for reply-to)
  message: string;               // User's message
  subject?: string;              // Optional subject override
  submittedAt: Date;             // When form was submitted
  ipAddress?: string;            // For spam detection
}
```

### React Email Component

```typescript
// components/emails/contact-email.tsx
import {
  Html,
  Head,
  Body,
  Container,
  Section,
  Text,
  Link,
  Hr,
} from '@react-email/components';

export function ContactEmail({ 
  name, 
  email, 
  message, 
  subject,
  submittedAt 
}: ContactEmailProps) {
  return (
    <Html>
      <Head />
      <Body style={{ fontFamily: 'sans-serif', backgroundColor: '#f6f9fc' }}>
        <Container style={{ padding: '20px' }}>
          <Section style={{ backgroundColor: '#ffffff', padding: '20px', borderRadius: '5px' }}>
            <Text style={{ fontSize: '18px', fontWeight: 'bold' }}>
              New Contact Form Submission
            </Text>
            <Hr />
            <Text><strong>From:</strong> {name}</Text>
            <Text><strong>Email:</strong> <Link href={`mailto:${email}`}>{email}</Link></Text>
            <Text><strong>Submitted:</strong> {submittedAt.toLocaleString()}</Text>
            {subject && <Text><strong>Subject:</strong> {subject}</Text>}
            <Hr />
            <Text style={{ whiteSpace: 'pre-wrap' }}>{message}</Text>
          </Section>
        </Container>
      </Body>
    </Html>
  );
}
```

---

## Data Flow Diagrams

### Contact Form Submission Flow

```
User fills form
    ↓
Client-side validation (Zod + React Hook Form)
    ↓
POST /api/contact
    ↓
Server-side validation (Zod)
    ↓
Create ContactSubmission object
    ↓
Call Resend API with React Email template
    ↓
Success: Return { success: true, id: string }
Failure: Return { error: string } (500 status)
    ↓
Client shows success/error message
```

### Theme Preference Flow

```
User selects theme (light/dark/system)
    ↓
setTheme() from next-themes
    ↓
localStorage.setItem('theme', value)
    ↓
Update CSS class on <html> element
    ↓
Tailwind applies dark: prefixed styles
    ↓
Re-render all components with new theme
```

### Navigation Active State Flow

```
Page loads
    ↓
IntersectionObserver watches all sections
    ↓
User scrolls
    ↓
Section enters viewport (rootMargin: -20%)
    ↓
Callback updates active section state
    ↓
Navigation highlights active link
```

---

## API Endpoints

### POST /api/contact

**Purpose**: Handle contact form submissions and send email

**Request**:
```typescript
POST /api/contact
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "message": "I'm interested in Todo-Evolution for my team.",
  "subject": "Enterprise Inquiry" // optional
}
```

**Response** (Success):
```typescript
200 OK
Content-Type: application/json

{
  "success": true,
  "id": "4ef2ae98-7ab1-4edd-9cb1-3e8f3e3e3e3e"
}
```

**Response** (Validation Error):
```typescript
400 Bad Request
Content-Type: application/json

{
  "error": "Validation failed",
  "issues": [
    {
      "field": "email",
      "message": "Invalid email address"
    }
  ]
}
```

**Response** (Server Error):
```typescript
500 Internal Server Error
Content-Type: application/json

{
  "error": "Failed to send email. Please try again later."
}
```

---

## Type Exports

### Central Types File

```typescript
// types/homepage.ts

export interface ContactSubmission {
  id: string;
  submittedAt: Date;
  ipAddress?: string;
  userAgent?: string;
  name: string;
  email: string;
  message: string;
  subject?: string;
  status: 'pending' | 'sent' | 'failed' | 'spam';
  emailId?: string;
  error?: string;
  retryCount: number;
  sentAt?: Date;
}

export interface ThemePreference {
  theme: 'light' | 'dark' | 'system';
  resolvedTheme: 'light' | 'dark';
  systemTheme: 'light' | 'dark';
}

export interface NavigationSection {
  id: string;
  label: string;
  href: string;
  order: number;
  isActive: boolean;
}

export interface FeatureCard {
  id: string;
  icon: string;
  title: string;
  description: string;
  learnMoreUrl?: string;
  order: number;
}

export interface ContactEmailProps {
  name: string;
  email: string;
  message: string;
  subject?: string;
  submittedAt: Date;
  ipAddress?: string;
}
```

---

## Constraints & Validation Summary

| Field | Min | Max | Pattern | Required |
|-------|-----|-----|---------|----------|
| Contact Name | 2 chars | 100 chars | `^[a-zA-Z\s'-]+$` | ✓ |
| Contact Email | - | 255 chars | Valid email | ✓ |
| Contact Message | 10 chars | 1000 chars | - | ✓ |
| Contact Subject | - | 200 chars | - | ✗ |
| Theme Value | - | - | `'light' \| 'dark' \| 'system'` | ✓ |
| Feature Title | 3 chars | 50 chars | - | ✓ |
| Feature Description | 20 chars | 200 chars | - | ✓ |

---

## Security Considerations

### Contact Form
- Rate limiting: 5 submissions per IP per hour
- Spam detection: honeypot field + reCAPTCHA (future)
- Email validation: Strict regex + DNS MX record check (future)
- XSS prevention: Sanitize message before email rendering
- CSRF protection: Next.js built-in middleware

### Theme Preference
- Client-side only, no security concerns
- No PII stored

---

## Testing Checklist

- [ ] Contact form validation accepts valid inputs
- [ ] Contact form validation rejects invalid inputs
- [ ] Email successfully sends to configured address
- [ ] Email template renders correctly
- [ ] Theme switcher persists selection
- [ ] Theme applies across all pages (home, auth, dashboard, chat)
- [ ] Parallax respects prefers-reduced-motion
- [ ] Navigation highlights correct section on scroll
- [ ] Rate limiting prevents spam
