# Quickstart Guide: Homepage Implementation

**Feature**: 004-homepage  
**Estimated Time**: 4-6 hours for MVP  
**Prerequisites**: Phase III frontend (Next.js 15 + React 19) already running

---

## 🚀 Quick Start (5 minutes)

### 1. Install Dependencies

```bash
cd phase-3/frontend

# Install required packages
npm install next-themes react-intersection-observer resend react-email

# Install React Email components (for email templates)
npm install @react-email/components @react-email/render
```

### 2. Set Up Environment Variables

Create or update `.env.local`:

```env
# Resend API Key (get from https://resend.com/api-keys)
RESEND_API_KEY=re_xxxxxxxxxxxx

# Email configuration
CONTACT_EMAIL_TO=team@todo-evolution.com
CONTACT_EMAIL_FROM=contact@todo-evolution.com
```

### 3. Add ThemeProvider to Root Layout

Update `phase-3/frontend/src/app/layout.tsx`:

```tsx
import { ThemeProvider } from 'next-themes'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
```

### 4. Update Tailwind Config

Ensure `tailwind.config.ts` has dark mode enabled:

```typescript
import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: 'class', // ← Add this line
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  // ... rest of config
};
```

### 5. Create Homepage Route

Create `phase-3/frontend/src/app/page.tsx` (replace existing):

```tsx
import { HomePage } from '@/components/homepage/homepage';

export default function Page() {
  return <HomePage />;
}
```

### 6. Run Development Server

```bash
npm run dev
```

Visit http://localhost:3000 to see the homepage.

---

## 📁 File Structure

After implementation, your structure will look like this:

```
phase-3/frontend/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   └── contact/
│   │   │       └── route.ts              # NEW: Contact form API
│   │   ├── layout.tsx                     # MODIFIED: Add ThemeProvider
│   │   ├── page.tsx                       # MODIFIED: Homepage route
│   │   └── globals.css                    # MODIFIED: Dark mode styles
│   │
│   ├── components/
│   │   ├── homepage/                      # NEW: Homepage components
│   │   │   ├── homepage.tsx               # Main homepage component
│   │   │   ├── hero-section.tsx           # Hero with CTA
│   │   │   ├── features-section.tsx       # 9 feature cards
│   │   │   ├── video-section.tsx          # YouTube embed
│   │   │   ├── developer-section.tsx      # API info
│   │   │   ├── contact-section.tsx        # Contact form
│   │   │   ├── footer.tsx                 # Footer with links
│   │   │   └── navigation.tsx             # Header navigation
│   │   │
│   │   ├── emails/                        # NEW: Email templates
│   │   │   └── contact-email.tsx          # React Email template
│   │   │
│   │   ├── theme/                         # NEW: Theme components
│   │   │   └── theme-toggle.tsx           # Dark/light mode toggle
│   │   │
│   │   ├── auth/
│   │   │   └── auth-layout.tsx            # MODIFIED: Add dark mode styles
│   │   │
│   │   ├── layout/
│   │   │   └── header.tsx                 # MODIFIED: Add theme toggle
│   │   │
│   │   └── ui/                            # EXISTING: shadcn components
│   │       ├── button.tsx
│   │       ├── input.tsx
│   │       ├── card.tsx
│   │       └── ...
│   │
│   ├── lib/
│   │   ├── constants/
│   │   │   ├── features.ts                # NEW: Feature cards data
│   │   │   └── navigation.ts              # NEW: Nav sections data
│   │   │
│   │   └── validations/
│   │       └── contact.ts                 # NEW: Zod schemas
│   │
│   └── types/
│       └── homepage.ts                    # NEW: TypeScript types
│
├── .env.local                             # NEW: Environment variables
├── tailwind.config.ts                     # MODIFIED: Enable dark mode
└── package.json                           # MODIFIED: New dependencies
```

---

## 🎨 Component Implementation Order

### Phase 1: Core Infrastructure (30 min)
1. ✅ Install dependencies
2. ✅ Configure ThemeProvider
3. ✅ Create types and constants
4. ✅ Set up validation schemas

### Phase 2: Theme System (30 min)
5. Create `ThemeToggle` component
6. Update existing `Header` component to include toggle
7. Test dark mode across auth, dashboard, chat pages
8. Add dark mode variants to `globals.css`

### Phase 3: Homepage Sections (2 hours)
9. Create `Navigation` component (sticky header)
10. Create `HeroSection` component (parallax background)
11. Create `FeaturesSection` component (9 cards, 3×3 grid)
12. Create `VideoSection` component (YouTube embed)
13. Create `DeveloperSection` component (API docs link)
14. Create `ContactSection` component (form with validation)
15. Create `Footer` component (links, social, copyright)

### Phase 4: Email & API (1 hour)
16. Create `ContactEmail` React Email template
17. Implement `/api/contact` route handler
18. Test email sending with Resend
19. Add rate limiting middleware

### Phase 5: Polish & Accessibility (1 hour)
20. Add parallax scroll effects
21. Implement smooth scrolling
22. Add Intersection Observer for nav highlighting
23. Test keyboard navigation
24. Run Lighthouse accessibility audit
25. Fix any WCAG 2.1 Level AA violations

---

## 🧪 Testing Checklist

### Manual Testing
- [ ] Homepage loads without errors
- [ ] Theme toggle switches between light/dark/system
- [ ] Theme persists on page reload
- [ ] All pages (home, auth, dashboard, chat) respect theme
- [ ] Contact form validates inputs correctly
- [ ] Contact form submits and shows success message
- [ ] Email arrives with correct formatting
- [ ] Video auto-plays when scrolled to
- [ ] Navigation highlights active section
- [ ] Smooth scroll works on "Watch Demo" button
- [ ] Parallax effects work (and disable with prefers-reduced-motion)
- [ ] Mobile responsive (test 375px, 768px, 1024px, 1920px)

### Automated Testing
```bash
# Lighthouse audit
npm run build
npm run start
# Open Chrome DevTools > Lighthouse > Run audit

# Check for accessibility violations
npm install -D @axe-core/playwright
# Run accessibility tests
```

---

## 🔧 Configuration Reference

### Resend Setup

1. Sign up at https://resend.com
2. Verify your domain (or use `onboarding@resend.dev` for testing)
3. Create API key with "Sending access" permission
4. Add to `.env.local` as `RESEND_API_KEY`

### YouTube Video Setup

1. Upload demo video to YouTube
2. Go to video settings > Advanced > Allow embedding
3. Copy video ID from URL: `https://youtube.com/watch?v=VIDEO_ID`
4. Use in `VideoSection` component:
   ```tsx
   const VIDEO_ID = 'your-video-id-here';
   const embedUrl = `https://www.youtube-nocookie.com/embed/${VIDEO_ID}?autoplay=1&mute=1`;
   ```

### Theme Colors

Add to `tailwind.config.ts`:

```typescript
theme: {
  extend: {
    colors: {
      background: 'hsl(var(--background))',
      foreground: 'hsl(var(--foreground))',
      // ... existing colors
    },
  },
}
```

Add to `globals.css`:

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    /* ... other light mode colors */
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    /* ... other dark mode colors */
  }
}
```

---

## 🐛 Common Issues & Solutions

### Issue: "Module not found: Can't resolve 'next-themes'"
**Solution**: Run `npm install next-themes` again, restart dev server

### Issue: Email not sending
**Solution**: 
- Check `.env.local` has valid `RESEND_API_KEY`
- Verify email domain is verified in Resend dashboard
- Check server logs for error details
- Use `onboarding@resend.dev` for testing

### Issue: Dark mode not working
**Solution**:
- Ensure `darkMode: 'class'` in `tailwind.config.ts`
- Check `suppressHydrationWarning` on `<html>` tag
- Verify `ThemeProvider` wraps all content in `layout.tsx`
- Use `dark:` prefix for dark mode styles (e.g., `dark:bg-gray-900`)

### Issue: Parallax not working on mobile
**Solution**: This is expected for performance. Parallax is disabled on mobile devices and when `prefers-reduced-motion` is enabled.

### Issue: Navigation not highlighting active section
**Solution**:
- Check `rootMargin: '-20% 0px 0px 0px'` in Intersection Observer
- Verify section IDs match navigation hrefs
- Ensure sections have sufficient height to trigger observer

---

## 📊 Performance Targets

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| First Contentful Paint | < 1.5s | TBD | ⏳ |
| Largest Contentful Paint | < 2.0s | TBD | ⏳ |
| Total Blocking Time | < 200ms | TBD | ⏳ |
| Cumulative Layout Shift | < 0.1 | TBD | ⏳ |
| Lighthouse Performance | 90+ | TBD | ⏳ |
| Lighthouse Accessibility | 90+ | TBD | ⏳ |

Run after implementation:
```bash
npm run build
npm run start
# Open http://localhost:3000
# Chrome DevTools > Lighthouse > Generate report
```

---

## 🚀 Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Import project to Vercel
3. Add environment variables:
   - `RESEND_API_KEY`
   - `CONTACT_EMAIL_TO`
   - `CONTACT_EMAIL_FROM`
4. Deploy

### Environment Variables in Production

```env
RESEND_API_KEY=re_live_xxxxxxxxxxxx
CONTACT_EMAIL_TO=team@todo-evolution.com
CONTACT_EMAIL_FROM=contact@todo-evolution.com
NODE_ENV=production
```

---

## 📚 Additional Resources

- **next-themes docs**: https://github.com/pacocoursey/next-themes
- **Resend docs**: https://resend.com/docs
- **React Email docs**: https://react.email/docs
- **Intersection Observer API**: https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API
- **WCAG 2.1 Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/
- **Tailwind Dark Mode**: https://tailwindcss.com/docs/dark-mode

---

## 🆘 Getting Help

If you encounter issues:

1. Check this quickstart guide
2. Review `research.md` for technology decisions
3. Check `data-model.md` for type definitions
4. Review `contracts/contact-api.yaml` for API specs
5. Search GitHub issues for similar problems
6. Ask for help in team chat

---

**Next Step**: Proceed to implementation by following the component order above. Start with Phase 1 (Core Infrastructure) and work through each phase sequentially.
