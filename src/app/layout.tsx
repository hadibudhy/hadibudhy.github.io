import type { Metadata, Viewport } from "next";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { cn } from "@/lib/utils";

export const metadata: Metadata = {
  metadataBase: new URL("https://hadibudhy.github.io"),
  title: {
    default: "Hadi Budhy | Data Analyst & Analytics Engineer",
    template: "%s | Hadi Budhy"
  },
  description: "Data analyst and analytics engineer who works with messy business data to clarify decisions.",
  keywords: ["Data Analyst", "Data Engineer", "Analytics Engineer", "Machine Learning", "Python", "SQL"],
  authors: [{ name: "Hadi Budhy" }],
  creator: "Hadi Budhy",
  alternates: {
    canonical: "/",
  },
  openGraph: {
    type: "website",
    url: "https://hadibudhy.github.io",
    title: "Hadi Budhy | Data Analyst & Analytics Engineer",
    description: "Data analyst and analytics engineer who works with messy business data to clarify decisions.",
    siteName: "Hadi Budhy",
    locale: "en_US",
  },
  twitter: {
    card: "summary",
    title: "Hadi Budhy | Data Analyst & Analytics Engineer",
    description: "Data analyst and analytics engineer who works with messy business data to clarify decisions.",
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
              jobTitle: "Data Analyst & Analytics Engineer",
              address: { "@type": "PostalAddress", addressLocality: "Jakarta", addressCountry: "ID" },
              sameAs: ["https://github.com/hadibudhy", "https://linkedin.com/in/hadibudhy"],
            })}
        </script>
      </body>
    </html>
  );
}
