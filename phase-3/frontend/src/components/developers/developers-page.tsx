"use client";

import { useState, useEffect } from "react";
import { TableOfContents } from "./table-of-contents";
import { AuthenticationSection } from "./sections/authentication";
import { TasksApiSection } from "./sections/tasks-api";
import { ChatApiSection } from "./sections/chat-api";
import { McpServerSection } from "./sections/mcp-server";
import { QuickStartSection } from "./sections/quick-start";
import { ErrorHandlingSection } from "./sections/error-handling";

export function DevelopersPage() {
  const [activeSection, setActiveSection] = useState("quick-start");

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActiveSection(entry.target.id);
          }
        });
      },
      {
        rootMargin: "-20% 0px -80% 0px",
        threshold: 0,
      }
    );

    const sections = document.querySelectorAll("[data-section]");
    sections.forEach((section) => observer.observe(section));

    return () => observer.disconnect();
  }, []);

  return (
    <div className="min-h-screen bg-white dark:bg-gray-950">
      {/* Header */}
      <header className="sticky top-0 z-40 border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-950">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                API Documentation
              </h1>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                Complete guide to integrating with Todo Evolution
              </p>
            </div>
            <a
              href="/"
              className="text-sm text-blue-600 dark:text-blue-400 hover:underline"
            >
              ← Back to Home
            </a>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Table of Contents - Sticky on Desktop */}
          <aside className="lg:w-64 lg:sticky lg:top-24 lg:self-start">
            <TableOfContents activeSection={activeSection} />
          </aside>

          {/* Documentation Content */}
          <main className="flex-1 max-w-4xl">
            <QuickStartSection />
            <AuthenticationSection />
            <TasksApiSection />
            <ChatApiSection />
            <McpServerSection />
            <ErrorHandlingSection />
          </main>
        </div>
      </div>
    </div>
  );
}
