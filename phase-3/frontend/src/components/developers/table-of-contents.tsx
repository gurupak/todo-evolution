"use client";

interface Section {
  id: string;
  label: string;
  subsections?: { id: string; label: string }[];
}

const sections: Section[] = [
  { id: "quick-start", label: "Quick Start" },
  { id: "authentication", label: "Authentication" },
  {
    id: "tasks-api",
    label: "Tasks API",
    subsections: [
      { id: "list-tasks", label: "List Tasks" },
      { id: "create-task", label: "Create Task" },
      { id: "get-task", label: "Get Task" },
      { id: "update-task", label: "Update Task" },
      { id: "toggle-complete", label: "Toggle Complete" },
      { id: "delete-task", label: "Delete Task" },
    ],
  },
  {
    id: "chat-api",
    label: "Chat API",
    subsections: [
      { id: "send-message", label: "Send Message" },
      { id: "list-conversations", label: "List Conversations" },
      { id: "get-conversation", label: "Get Conversation" },
      { id: "update-conversation", label: "Update Conversation" },
      { id: "delete-conversation", label: "Delete Conversation" },
    ],
  },
  {
    id: "mcp-server",
    label: "MCP Server",
    subsections: [
      { id: "mcp-overview", label: "Overview" },
      { id: "mcp-setup", label: "Setup" },
      { id: "mcp-tools", label: "Available Tools" },
    ],
  },
  { id: "error-handling", label: "Error Handling" },
];

interface TableOfContentsProps {
  activeSection: string;
}

export function TableOfContents({ activeSection }: TableOfContentsProps) {
  const scrollToSection = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      const offset = 100;
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - offset;

      window.scrollTo({
        top: offsetPosition,
        behavior: "smooth",
      });
    }
  };

  return (
    <nav className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 border border-gray-200 dark:border-gray-800">
      <h2 className="text-sm font-semibold text-gray-900 dark:text-white mb-4 uppercase tracking-wide">
        On This Page
      </h2>
      <ul className="space-y-2">
        {sections.map((section) => (
          <li key={section.id}>
            <button
              onClick={() => scrollToSection(section.id)}
              className={`text-left w-full text-sm py-1.5 px-3 rounded transition-colors ${
                activeSection === section.id
                  ? "bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 font-medium"
                  : "text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800"
              }`}
            >
              {section.label}
            </button>
            {section.subsections && (
              <ul className="ml-4 mt-1 space-y-1">
                {section.subsections.map((subsection) => (
                  <li key={subsection.id}>
                    <button
                      onClick={() => scrollToSection(subsection.id)}
                      className={`text-left w-full text-xs py-1 px-3 rounded transition-colors ${
                        activeSection === subsection.id
                          ? "bg-blue-50 dark:bg-blue-950 text-blue-600 dark:text-blue-400"
                          : "text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800"
                      }`}
                    >
                      {subsection.label}
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </li>
        ))}
      </ul>
    </nav>
  );
}
