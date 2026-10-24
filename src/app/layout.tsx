import type { Metadata, Viewport } from "next";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { cn } from "@/lib/utils";

export const metadata: Metadata = {
  metadataBase: new URL("https://hadibudhy.github.io"),
    title: {
    default: "Hadi Budhy | Data Engineering, Analytics & Data Science",
    template: "%s | Hadi Budhy"
  },
  description: "Data professional working across data engineering, analytics, and applied data science to build reliable foundations and decision-ready evidence.",
  keywords: ["Data engineering", "Data analytics", "Data science", "Analytics engineering", "Product analytics", "SQL", "Python"],
  authors: [{ name: "Hadi Budhy" }],
  creator: "Hadi Budhy",
  alternates: {
    canonical: "/",
  },
  openGraph: {
    type: "website",
    url: "https://hadibudhy.github.io",
    title: "Hadi Budhy | Data Engineering, Analytics & Data Science",
    description: "Data professional working across data engineering, analytics, and applied data science to build reliable foundations and decision-ready evidence.",
    siteName: "Hadi Budhy",
    locale: "en_US",
    images: [{ url: "/images/profile-illustration.jpg", alt: "Illustrated profile portrait of Hadi Budhy" }],
  },
  twitter: {
    card: "summary",
    title: "Hadi Budhy | Data Engineering, Analytics & Data Science",
    description: "Data professional working across data engineering, analytics, and applied data science to build reliable foundations and decision-ready evidence.",
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
    <html lang="en" className={cn("h-full antialiased")}>
      <body className="min-h-full flex flex-col bg-background text-foreground">
        <Navbar />
        <main className="flex-1">
          {children}
        </main>
        <Footer />
        <script id="person-jsonld" type="application/ld+json">
          {JSON.stringify({
              "@context": "https://schema.org",
              "@type": "Person",
              name: "Hadi Budhy",
              url: "https://hadibudhy.github.io",
              jobTitle: "Data professional across engineering, analytics, and data science",
              knowsAbout: ["Data engineering", "Analytics engineering", "Product analytics", "Applied data science", "Experimentation", "Data reliability"],
              address: { "@type": "PostalAddress", addressLocality: "Jakarta", addressCountry: "ID" },
              sameAs: ["https://github.com/hadibudhy", "https://linkedin.com/in/hadibudhy"],
            })}
        </script>
      </body>
    </html>
  );
}
