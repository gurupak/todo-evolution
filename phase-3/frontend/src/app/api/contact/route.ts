import { NextRequest, NextResponse } from "next/server";
import { Resend } from "resend";
import { ContactEmail } from "@/components/emails/contact-email";
import { contactFormSchema } from "@/lib/validations/contact";

const resend = new Resend(process.env.RESEND_API_KEY);

/**
 * Contact Form API Route
 * Handles contact form submissions and sends email via Resend
 * Per FR-054, FR-055
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Validate input - FR-053
    const validationResult = contactFormSchema.safeParse(body);

    if (!validationResult.success) {
      return NextResponse.json(
        { error: "Invalid form data", details: validationResult.error.errors },
        { status: 400 }
      );
    }

    const { name, email, subject, message } = validationResult.data;

    // Send email via Resend - FR-054
    const emailResponse = await resend.emails.send({
      from: process.env.CONTACT_EMAIL_FROM || "contact@todo-evolution.com",
      to: process.env.CONTACT_EMAIL_TO || "team@todo-evolution.com",
      replyTo: email, // FR-054: User's email as reply-to
      subject: subject || `Contact Form: Message from ${name}`,
      react: ContactEmail({ name, email, subject, message }),
    });

    if (emailResponse.error) {
      console.error("Resend error:", emailResponse.error);
      return NextResponse.json(
        { error: "Failed to send email. Please try again later." },
        { status: 500 }
      );
    }

    return NextResponse.json(
      {
        success: true,
        message: "Thank you for contacting us! We'll get back to you soon.",
        id: emailResponse.data?.id
      },
      { status: 200 }
    );
  } catch (error) {
    console.error("Contact form error:", error);
    return NextResponse.json(
      { error: "An unexpected error occurred. Please try again later." },
      { status: 500 }
    );
  }
}
