"use client";

import { useEffect, useRef, useState } from "react";
import { useInView } from "react-intersection-observer";

/**
 * Video Section Component
 * YouTube video demonstration with lazy loading and auto-play on scroll
 * Per FR-013 to FR-017
 */
export function VideoSection() {
  const [isPlaying, setIsPlaying] = useState(false);
  const { ref, inView } = useInView({
    threshold: 0.5,
    triggerOnce: false,
  });

  // Todo-Evolution demo video
  const VIDEO_ID = "ibGnjSKLqTc";

  useEffect(() => {
    // Check for prefers-reduced-motion
    const prefersReducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;

    if (inView && !prefersReducedMotion && !isPlaying) {
      setIsPlaying(true);
    }
  }, [inView, isPlaying]);

  return (
    <section
      id="demo"
      ref={ref}
      className="relative py-24 bg-white dark:bg-gray-900"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-12">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
            See Todo-Evolution in Action
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Watch how AI-powered task management transforms your workflow.
            Natural conversations, instant results.
          </p>
        </div>

        {/* Video Player - FR-013, FR-014, FR-015 */}
        <div className="relative max-w-5xl mx-auto">
          <div className="relative pb-[56.25%] rounded-xl overflow-hidden shadow-2xl bg-gray-100 dark:bg-gray-800">
            {!isPlaying ? (
              /* Loading/Preview State - FR-017 */
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center">
                  <div className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg
                      className="w-10 h-10 text-white"
                      fill="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path d="M8 5v14l11-7z" />
                    </svg>
                  </div>
                  <p className="text-gray-600 dark:text-gray-400">
                    Scroll to play demo
                  </p>
                </div>
              </div>
            ) : (
              /* YouTube Iframe - FR-013, FR-015 (privacy mode) */
              <iframe
                className="absolute inset-0 w-full h-full"
                src={`https://www.youtube-nocookie.com/embed/${VIDEO_ID}?autoplay=1&mute=1&controls=1&rel=0&modestbranding=1`}
                title="Todo-Evolution Demo Video"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            )}
          </div>

          {/* Video Caption - FR-016 */}
          <div className="mt-6 text-center">
            <p className="text-gray-600 dark:text-gray-400">
              Learn how to create, manage, and complete tasks using natural
              language. No training required.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
