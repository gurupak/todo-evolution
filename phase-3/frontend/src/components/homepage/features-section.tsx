"use client";

import { useEffect, useRef, useState } from "react";
import { FEATURE_CARDS } from "@/lib/constants/features";

/**
 * Features Section Component
 * Displays 9 feature cards in responsive grid with fade-in animations
 * Per FR-019 to FR-022
 */
export function FeaturesSection() {
  const [visibleCards, setVisibleCards] = useState<Set<string>>(new Set());
  const cardRefs = useRef<Map<string, HTMLDivElement>>(new Map());

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const cardId = entry.target.getAttribute("data-card-id");
            if (cardId) {
              setVisibleCards((prev) => new Set(prev).add(cardId));
            }
          }
        });
      },
      {
        threshold: 0.1,
        rootMargin: "0px 0px -100px 0px",
      },
    );

    cardRefs.current.forEach((element) => {
      if (element) observer.observe(element);
    });

    return () => observer.disconnect();
  }, []);

  return (
    <section
      id="features"
      className="relative py-24 bg-gray-50 dark:bg-gray-800"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
            Powerful Features for Modern Teams
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Everything you need to manage tasks efficiently, powered by AI and
            built for collaboration.
          </p>
        </div>

        {/* Feature Cards Grid - FR-019 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {FEATURE_CARDS.map((feature, index) => (
            <div
              key={feature.id}
              ref={(el) => {
                if (el) cardRefs.current.set(feature.id, el);
              }}
              data-card-id={feature.id}
              className={`bg-white dark:bg-gray-900 rounded-xl p-6 shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all duration-500 border border-gray-200 dark:border-gray-700 ${
                visibleCards.has(feature.id)
                  ? "opacity-100 translate-y-0"
                  : "opacity-0 translate-y-8"
              }`}
              style={{
                transitionDelay: visibleCards.has(feature.id)
                  ? `${(index % 3) * 100}ms`
                  : "0ms",
              }}
            >
              {/* Icon */}
              <div className="text-5xl mb-4">{feature.icon}</div>

              {/* Title - FR-020 */}
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">
                {feature.title}
              </h3>

              {/* Description - FR-020 */}
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                {feature.description}
              </p>

              {/* Optional Learn More Link - FR-020 */}
              {feature.learnMoreLink && (
                <a
                  href={feature.learnMoreLink}
                  className="text-blue-600 dark:text-blue-400 hover:underline font-medium inline-flex items-center"
                >
                  Learn More
                  <svg
                    className="w-4 h-4 ml-1"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 5l7 7-7 7"
                    />
                  </svg>
                </a>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
