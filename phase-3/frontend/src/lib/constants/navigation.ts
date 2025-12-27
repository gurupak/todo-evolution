import { NavigationSection } from '@/types/homepage';

/**
 * Navigation Sections
 * In-page scroll anchor links per FR-001
 */

export const NAVIGATION_SECTIONS: NavigationSection[] = [
  {
    id: 'home',
    label: 'Home',
    href: '#home',
  },
  {
    id: 'features',
    label: 'Features',
    href: '#features',
  },
  {
    id: 'demo',
    label: 'Demo',
    href: '#demo',
  },
  {
    id: 'developers',
    label: 'Developers',
    href: '#developers',
  },
  {
    id: 'contact',
    label: 'Contact',
    href: '#contact',
  },
];

/**
 * Footer Navigation Columns
 * Per FR-031 (updated - no unimplemented pages)
 */

export const FOOTER_SECTIONS = {
  product: {
    title: 'Product',
    links: [
      { label: 'Features', href: '#features' },
    ],
  },
  developers: {
    title: 'Developers',
    links: [
      { label: 'API Docs', href: '/developers' },
      { label: 'MCP Integration', href: '/developers#mcp' },
    ],
  },
  company: {
    title: 'Company',
    links: [
      { label: 'Contact', href: '#contact' },
    ],
  },
  legal: {
    title: 'Legal',
    links: [
      { label: 'Privacy Policy', href: '/privacy' },
      { label: 'Terms of Service', href: '/terms' },
    ],
  },
};

export const SOCIAL_LINKS = [
  { name: 'GitHub', href: 'https://github.com', icon: 'github' },
  { name: 'Twitter', href: 'https://twitter.com', icon: 'twitter' },
  { name: 'LinkedIn', href: 'https://linkedin.com', icon: 'linkedin' },
];
