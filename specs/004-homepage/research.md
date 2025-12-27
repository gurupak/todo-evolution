# Research: Homepage Implementation Technologies

**Feature**: 004-homepage  
**Date**: 2025-12-27  
**Phase**: 0 - Research & Technology Selection

## Overview

This document consolidates research findings for implementing the professional Todo-Evolution homepage with parallax effects, dark/light theme support, contact form with email integration, and comprehensive theme application across all pages.

---

## Decision 1: Dark/Light Theme Management

### Decision
**next-themes** v0.4.x (latest)

### Rationale
- Zero-flash theme switching with system preference detection
- Seamless Next.js App Router integration (v13+)
- Built-in `suppressHydrationWarning` support for SSR
- Only 2 lines of code for basic setup
- 78 code snippets available, High reputation, 86.2 benchmark score
- Supports multiple themes beyond just light/dark
- Respects `prefers-color-scheme` media query
- Automatic localStorage persistence

### Implementation Pattern
```tsx
// app/layout.tsx
import { ThemeProvider } from 'next-themes'

export default function Layout({ children }) {
  return (
    <html suppressHydrationWarning>
      <body>
        <ThemeProvider attribute="class" defaultTheme="system">
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
```

### Alternatives Considered
1. **Manual CSS variables + context** - More complex, requires custom implementation
2. **Tailwind dark mode only** - Doesn't handle system preferences or persistence
3. **Custom theme provider** - Reinventing the wheel, higher maintenance

### Integration Points
- Works with existing Tailwind CSS setup (already in phase-3/frontend)
- Compatible with shadcn/ui components (already installed)
- Applies to all routes automatically via layout wrapper

---

## Decision 2: Parallax Scrolling Effects

### Decision
**CSS-based parallax** using `transform: translateZ()` + Intersection Observer API

### Rationale
- Native browser performance (hardware-accelerated)
- WCAG 2.1 Level AA compliant (can disable with `prefers-reduced-motion`)
- No external dependencies needed
- Smaller bundle size compared to JavaScript libraries
- Better mobile performance than JS-based solutions
- Fine-grained control over scroll speeds (30-50% as specified)

### Implementation Pattern
```tsx
// CSS approach
.parallax-layer {
  transform: translateZ(-1px) scale(2);
  will-change: transform;
}

@media (prefers-reduced-motion: reduce) {
  .parallax-layer {
    transform: none;
  }
}

// Intersection Observer for scroll detection
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      // Apply parallax transform
    }
  });
}, { rootMargin: '-20% 0px 0px 0px' });
```

### Alternatives Considered
1. **Framer Motion** (/grx7/framer-motion) - 327 snippets, 52.1 score
   - Rejected: Adds 47KB gzipped, overkill for simple parallax
   - Better suited for complex animations
2. **React Parallax Tilt** - Not found in Context7
   - Searched but no high-quality match for Next.js 15
3. **Rellax** (/dixonandmoe_rellax) - Vanilla JS library
   - Rejected: Old library, not React-native, 19 snippets only

### Performance Considerations
- Use `will-change: transform` sparingly (only on scrolling elements)
- Implement lazy loading for parallax sections below fold
- Debounce scroll events to 16ms (60fps)

---

## Decision 3: Navigation Active State Detection

### Decision
**React Intersection Observer** (/thebuilder/react-intersection-observer)

### Rationale
- 58 code snippets, High reputation, 89.9 benchmark score
- Perfect for detecting when sections enter viewport
- Supports `rootMargin: '-20% 0px 0px 0px'` for 80-100px offset (CL-005 requirement)
- SSR-safe, TypeScript support
- Performance: Uses native IntersectionObserver API
- Works seamlessly with Next.js App Router

### Implementation Pattern
```tsx
import { useInView } from 'react-intersection-observer'

function Section({ id, onInView }) {
  const { ref, inView } = useInView({
    threshold: 0,
    rootMargin: '-20% 0px 0px 0px', // CL-005: 20% offset
    onChange: (inView) => {
      if (inView) onInView(id);
    }
  });

  return <section ref={ref} id={id}>...</section>
}
```

### Alternatives Considered
1. **Manual scroll listeners** - Lower performance, needs cleanup
2. **react-intersection-observer-hook** (/onderonur/react-intersection-observer-hook) - 33 snippets
   - Rejected: Less adoption, fewer examples
3. **Vanilla IntersectionObserver** - Works but less React-idiomatic

---

## Decision 4: Email Sending (Contact Form)

### Decision
**Resend** (/resend/resend-node) with React Email templates

### Rationale
- Official email API for Next.js ecosystem
- 98 code snippets, High reputation, 82.8 benchmark score
- React Email component support (400 snippets, 75.9 score)
- Free tier: 100 emails/day, 3,000/month
- Simple API route integration
- No SMTP configuration needed
- Excellent deliverability rates

### Implementation Pattern
```tsx
// app/api/contact/route.ts
import { Resend } from 'resend';
import { ContactEmail } from '@/components/emails/contact-email';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST(request: Request) {
  const { name, email, message } = await request.json();
  
  const { data, error } = await resend.emails.send({
    from: 'contact@todo-evolution.com',
    to: 'team@todo-evolution.com',
    replyTo: email,
    subject: `New Contact Form: ${name}`,
    react: <ContactEmail name={name} email={email} message={message} />,
  });

  if (error) {
    return Response.json({ error }, { status: 500 });
  }

  return Response.json({ success: true, id: data.id });
}
```

### Alternatives Considered
1. **Nodemailer** - Requires SMTP setup, more complex
2. **SendGrid** - Requires account setup, less developer-friendly API
3. **Mailgun** - Similar to SendGrid, more enterprise-focused
4. **React Email + custom SMTP** - More configuration, harder to maintain

### Setup Requirements
- Resend API key (free tier sufficient for MVP)
- Verified domain (or use Resend's test domain)
- Environment variable: `RESEND_API_KEY`

---

## Decision 5: Video Player (YouTube Integration)

### Decision
**YouTube iframe API** with privacy-enhanced mode (`youtube-nocookie.com`)

### Rationale
- CL-002 clarification: YouTube with privacy mode selected
- No additional package needed (native iframe)
- Free CDN hosting for video
- Lazy loading support (FR-048)
- Auto-play with muted sound (CL-001)
- GDPR-friendly with privacy mode

### Implementation Pattern
```tsx
'use client';

function VideoSection() {
  const videoRef = useRef<HTMLIFrameElement>(null);
  const { ref, inView } = useInView({ triggerOnce: true });

  useEffect(() => {
    if (inView && videoRef.current) {
      // Auto-play when scrolled into view (CL-001)
      videoRef.current.src = videoRef.current.dataset.src!;
    }
  }, [inView]);

  return (
    <div ref={ref}>
      <iframe
        ref={videoRef}
        data-src="https://www.youtube-nocookie.com/embed/VIDEO_ID?autoplay=1&mute=1"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
      />
    </div>
  );
}
```

### Requirements
- Video must be uploaded to YouTube
- Video ID to be provided during implementation
- Fallback thumbnail image for loading state

---

## Decision 6: Smooth Scrolling (Watch Demo Button)

### Decision
**Native CSS `scroll-behavior: smooth`** + `Element.scrollIntoView()`

### Rationale
- CL-001: Auto-scroll to video section with 500-800ms duration
- Zero dependencies
- Native browser support (97%+ coverage)
- Respects `prefers-reduced-motion`

### Implementation Pattern
```tsx
function HeroSection() {
  const handleWatchDemo = () => {
    const videoSection = document.getElementById('video-demo');
    videoSection?.scrollIntoView({ 
      behavior: 'smooth',
      block: 'start'
    });
  };

  return (
    <button onClick={handleWatchDemo}>Watch Demo</button>
  );
}

// globals.css
html {
  scroll-behavior: smooth;
}

@media (prefers-reduced-motion: reduce) {
  html {
    scroll-behavior: auto;
  }
}
```

### Alternatives Considered
- **Framer Motion scroll animations** - Overkill for simple scroll
- **React Scroll** library - Unnecessary dependency

---

## Decision 7: Form Validation

### Decision
**React Hook Form** (already installed) + **Zod** (already installed)

### Rationale
- Already in package.json from Phase III
- Zero additional dependencies
- Type-safe validation with Zod schemas
- Excellent performance (uncontrolled components)
- Built-in error handling

### Implementation Pattern
```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const contactSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  message: z.string().min(10, 'Message must be at least 10 characters'),
});

function ContactForm() {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(contactSchema),
  });

  const onSubmit = async (data) => {
    const response = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
  };

  return <form onSubmit={handleSubmit(onSubmit)}>...</form>
}
```

---

## Decision 8: Component Library

### Decision
**shadcn/ui** (already installed via @radix-ui/*)

### Rationale
- Already integrated in Phase III frontend
- Matches existing design system
- All required components available:
  - Button (@radix-ui/react-slot)
  - Dialog (@radix-ui/react-dialog)
  - Dropdown Menu (@radix-ui/react-dropdown-menu)
  - Form inputs (custom + @radix-ui primitives)
- Tailwind CSS based (already configured)
- Accessible by default (WCAG 2.1 Level AA)

### Existing Components to Reuse
From `phase-3/frontend/src/components/ui/`:
- button.tsx
- card.tsx
- input.tsx
- label.tsx
- badge.tsx
- dialog.tsx
- dropdown-menu.tsx
- scroll-area.tsx

---

## Technology Stack Summary

| Technology | Version | Purpose | Status |
|------------|---------|---------|--------|
| Next.js | 15.1.0 | Framework | ✅ Installed |
| React | 19.0.0 | UI Library | ✅ Installed |
| TypeScript | 5.x | Type Safety | ✅ Installed |
| Tailwind CSS | 3.4.0 | Styling | ✅ Installed |
| next-themes | latest | Dark/Light Mode | 🔲 To Install |
| react-intersection-observer | latest | Scroll Detection | 🔲 To Install |
| resend | latest | Email API | 🔲 To Install |
| react-email | latest | Email Templates | 🔲 To Install |
| React Hook Form | 7.54.0 | Form Management | ✅ Installed |
| Zod | 3.24.0 | Validation | ✅ Installed |
| shadcn/ui (Radix) | Various | Components | ✅ Installed |
| Lucide React | 0.469.0 | Icons | ✅ Installed |

---

## Installation Commands

```bash
# Navigate to frontend
cd phase-3/frontend

# Install new dependencies
npm install next-themes react-intersection-observer resend react-email

# Install React Email CLI (dev dependency)
npm install -D @react-email/components
```

---

## Environment Variables Required

```env
# .env.local
RESEND_API_KEY=re_xxxxxxxxxxxx
CONTACT_EMAIL_TO=team@todo-evolution.com
CONTACT_EMAIL_FROM=contact@todo-evolution.com
```

---

## Performance Budget

| Metric | Target | Strategy |
|--------|--------|----------|
| First Contentful Paint | < 1.5s | Inline critical CSS, preload fonts |
| Largest Contentful Paint | < 2.0s | Lazy load video, optimize images |
| Total Bundle Size | < 300KB | Code splitting, tree shaking |
| Lighthouse Performance | 90+ | Follow all Core Web Vitals |
| Lighthouse Accessibility | 90+ | WCAG 2.1 Level AA compliance |

---

## Accessibility Compliance (WCAG 2.1 Level AA)

### Requirements Met
1. **Color Contrast**: 4.5:1 for normal text, 3:1 for large text
2. **Keyboard Navigation**: All interactive elements accessible via keyboard
3. **Screen Reader Support**: Semantic HTML, ARIA labels where needed
4. **Reduced Motion**: Respect `prefers-reduced-motion` for parallax
5. **Focus Indicators**: Visible focus states on all interactive elements

### Testing Tools
- Lighthouse accessibility audit
- axe DevTools
- NVDA/JAWS screen reader testing

---

## Next Steps

1. Install required npm packages
2. Create email templates using React Email
3. Implement ThemeProvider in root layout
4. Build homepage component structure
5. Apply theme to existing pages (auth, dashboard, chat)
6. Test dark/light mode across all routes
7. Implement contact form with Resend integration
8. Add parallax effects with accessibility fallbacks
9. Configure YouTube video embed
10. Run accessibility audit
