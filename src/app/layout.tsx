import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { cn } from "@/lib/utils";

const inter = Inter({
  variable: "--font-sans",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  metadataBase: new URL("https://hadibudhy.github.io"),
  title: {
    default: "Hadi Budhy | Data Analyst & Analytics Engineer",
    template: "%s | Hadi Budhy"
  },
  description: "Data analyst and engineer who turns messy pipelines into business decisions — at scale",
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
    description: "Data analyst and engineer who turns messy pipelines into business decisions at scale.",
    siteName: "Hadi Budhy",
    locale: "en_US",
  },
  twitter: {
    card: "summary",
    title: "Hadi Budhy | Data Analyst & Analytics Engineer",
    description: "Data analyst and engineer who turns messy pipelines into business decisions at scale.",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={cn("dark h-full antialiased", inter.variable)}
      style={{ colorScheme: 'dark' }}
    >
      <body className="min-h-full flex flex-col font-sans bg-background text-foreground">
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
