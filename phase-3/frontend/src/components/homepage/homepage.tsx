import { Navigation } from "./navigation";
import { HeroSection } from "./hero-section";
import { VideoSection } from "./video-section";
import { FeaturesSection } from "./features-section";
import { DeveloperSection } from "./developer-section";
import { ContactSection } from "./contact-section";
import { Footer } from "./footer";

/**
 * HomePage Composition Component
 * Complete professional homepage with all sections
 * Phase 3: Navigation, Hero, Video
 * Phase 4: Features
 * Phase 5: Developer/API
 * Phase 7: Contact Form
 * Phase 8: Footer
 */
export function HomePage() {
  return (
    <div className="min-h-screen">
      <Navigation />
      <main>
        <HeroSection />
        <VideoSection />
        <FeaturesSection />
        <DeveloperSection />
        <ContactSection />
      </main>
      <Footer />
    </div>
  );
}
