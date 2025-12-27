import { z } from 'zod';

/**
 * Contact Form Validation Schema
 * Validates contact form inputs per FR-052, FR-053
 */

export const contactFormSchema = z.object({
  name: z
    .string()
    .min(2, 'Name must be at least 2 characters')
    .max(100, 'Name must not exceed 100 characters')
    .trim(),

  email: z
    .string()
    .email('Please enter a valid email address')
    .trim(),

  subject: z
    .string()
    .max(200, 'Subject must not exceed 200 characters')
    .trim()
    .optional(),

  message: z
    .string()
    .min(10, 'Message must be at least 10 characters')
    .max(1000, 'Message must not exceed 1000 characters')
    .trim(),
});

export type ContactFormData = z.infer<typeof contactFormSchema>;
