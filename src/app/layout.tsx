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
  title: {
    default: "Hadi Budhy | Data Analyst & Analytics Engineer",
    template: "%s | Hadi Budhy"
  },
  description: "Data analyst and engineer who turns messy pipelines into business decisions — at scale",
  keywords: ["Data Analyst", "Data Engineer", "Analytics Engineer", "Machine Learning", "Python", "SQL"],
  authors: [{ name: "Hadi Budhy" }],
  creator: "Hadi Budhy",
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
      </body>
    </html>
  );
}
