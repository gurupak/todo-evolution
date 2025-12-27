"use client";

import { useState } from "react";

interface CodeBlockProps {
  code: string;
  language: string;
}

export function CodeBlock({ code, language }: CodeBlockProps) {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="relative group mb-6">
      <div className="absolute top-3 right-3 z-10">
        <button
          onClick={copyToClipboard}
          className="px-3 py-1.5 text-xs bg-gray-700 hover:bg-gray-600 text-white rounded transition-colors"
        >
          {copied ? "Copied!" : "Copy"}
        </button>
      </div>
      <div className="absolute top-3 left-3 text-xs text-gray-400 font-mono uppercase">
        {language}
      </div>
      <pre className="bg-gray-900 text-gray-100 rounded-lg p-6 pt-12 overflow-x-auto">
        <code className="text-sm font-mono">{code}</code>
      </pre>
    </div>
  );
}
