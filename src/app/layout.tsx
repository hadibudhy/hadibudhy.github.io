import type { Metadata, Viewport } from "next";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { cn } from "@/lib/utils";

export const metadata: Metadata = {
  metadataBase: new URL("https://hadibudhy.github.io"),
    title: {
    default: "Hadi Budhy | Analytics Engineer & Product Analyst",
    template: "%s | Hadi Budhy"
  },
  description: "Analytics Engineer and Product Analyst building trustworthy metrics and using product data to guide decisions.",
  keywords: ["Analytics Engineer", "Product Analyst", "Product analytics", "Analytics engineering", "dbt", "SQL", "Python"],
  authors: [{ name: "Hadi Budhy" }],
  creator: "Hadi Budhy",
  alternates: {
    canonical: "/",
  },
  openGraph: {
    type: "website",
    url: "https://hadibudhy.github.io",
    title: "Hadi Budhy | Analytics Engineer & Product Analyst",
    description: "Analytics Engineer and Product Analyst building trustworthy metrics and using product data to guide decisions.",
    siteName: "Hadi Budhy",
    locale: "en_US",
  },
  twitter: {
    card: "summary",
    title: "Hadi Budhy | Analytics Engineer & Product Analyst",
    description: "Analytics Engineer and Product Analyst building trustworthy metrics and using product data to guide decisions.",
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
              jobTitle: "Data Analyst",
              knowsAbout: ["Analytics engineering", "Product analytics", "Experimentation"],
              address: { "@type": "PostalAddress", addressLocality: "Jakarta", addressCountry: "ID" },
              sameAs: ["https://github.com/hadibudhy", "https://linkedin.com/in/hadibudhy"],
            })}
        </script>
      </body>
    </html>
  );
}
