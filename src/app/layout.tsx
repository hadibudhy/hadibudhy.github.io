import type { Metadata, Viewport } from "next";
import localFont from "next/font/local";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { cn } from "@/lib/utils";

const ibmPlexSans = localFont({
  src: "../../public/fonts/IBM-Plex-Sans-Latin.woff2",
  weight: "400 700",
  display: "swap",
  variable: "--font-ibm-plex-sans",
});

export const metadata: Metadata = {
  metadataBase: new URL("https://hadibudhy.github.io"),
    title: {
    default: "Hadi Budhy | End-to-End Data: Engineering, Analytics, Science and Automation",
    template: "%s | Hadi Budhy"
  },
  description: "I build the path from raw data to decisions with tested pipelines, useful analysis, evaluated models, and automated checks.",
  keywords: ["Data engineering", "Data analytics", "Data science", "Data automation", "Analytics engineering", "Product analytics", "SQL", "Python", "dbt", "DuckDB"],
  authors: [{ name: "Hadi Budhy" }],
  creator: "Hadi Budhy",
  alternates: {
    canonical: "/",
  },
  openGraph: {
    type: "website",
    url: "https://hadibudhy.github.io",
    title: "Hadi Budhy | End-to-End Data: Engineering, Analytics, Science and Automation",
    description: "I build the path from raw data to decisions with tested pipelines, useful analysis, evaluated models, and automated checks.",
    siteName: "Hadi Budhy",
    locale: "en_US",
    images: [{ url: "/images/profile-illustration.jpg", alt: "Illustrated profile portrait of Hadi Budhy" }],
  },
  twitter: {
    card: "summary",
    title: "Hadi Budhy | End-to-End Data: Engineering, Analytics, Science and Automation",
    description: "I build the path from raw data to decisions with tested pipelines, useful analysis, evaluated models, and automated checks.",
    images: ["/images/profile-illustration.jpg"],
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={cn("h-full antialiased", ibmPlexSans.variable)}>
      <body className="min-h-full flex flex-col bg-background text-foreground">
        <a href="#main-content" className="skip-link">Skip to content</a>
        <Navbar />
        <main id="main-content" tabIndex={-1} className="flex-1 scroll-mt-20">
          {children}
        </main>
        <Footer />
        <script id="person-jsonld" type="application/ld+json">
          {JSON.stringify({
              "@context": "https://schema.org",
              "@type": "Person",
              name: "Hadi Budhy",
              url: "https://hadibudhy.github.io",
              jobTitle: "End-to-end data professional across engineering, analytics, science, and automation",
              knowsAbout: ["Data engineering", "Analytics engineering", "Product analytics", "Applied data science", "Data automation", "Experimentation", "Data reliability"],
              sameAs: ["https://github.com/hadibudhy"],
            })}
        </script>
      </body>
    </html>
  );
}
