import Link from "next/link";
import { Mail } from "lucide-react";

const links = [
  { label: "About", href: "/about" },
  { label: "Experience", href: "/#experience" },
  { label: "Work", href: "/#work" },
  { label: "Skills", href: "/#skills" },
];

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b border-white/[0.08] bg-background/85 backdrop-blur-xl">
      <div className="mx-auto flex h-14 min-w-0 max-w-6xl items-center justify-between gap-3 px-4 sm:h-16 sm:px-5 lg:px-8">
        <Link href="/" className="group flex min-w-0 shrink-0 items-center gap-2 sm:gap-3" aria-label="Hadi Budhy home">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-sm font-black text-primary-foreground transition-transform group-hover:rotate-6">HB</span>
          <span className="hidden text-sm font-bold tracking-[0.18em] text-foreground sm:inline">HADI BUDHY</span>
        </Link>
        <nav aria-label="Primary navigation" className="hidden min-w-0 items-center gap-2 text-xs font-medium sm:flex sm:gap-4 sm:text-sm md:gap-6">
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="hidden text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 sm:inline"
            >
              {link.label}
            </Link>
          ))}
          <Link href="/projects" className="whitespace-nowrap text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2">
            Projects
          </Link>
        </nav>
        <div className="flex min-w-0 items-center gap-2 sm:hidden">
          <details className="relative">
            <summary className="flex min-h-11 cursor-pointer list-none items-center rounded-full border border-white/[0.12] px-3 text-xs font-semibold text-foreground [&::-webkit-details-marker]:hidden">
              Menu
            </summary>
            <div className="absolute right-0 top-14 z-50 w-52 rounded-2xl border border-white/[0.12] bg-slate-950 p-2 shadow-2xl">
              {[...links, { label: "Projects", href: "/projects" }].map((link) => (
                <Link key={link.href} href={link.href} className="flex min-h-11 items-center rounded-xl px-3 text-sm text-muted-foreground hover:bg-white/[0.06] hover:text-foreground">
                  {link.label}
                </Link>
              ))}
            </div>
          </details>
          <a href="mailto:hadi.budhy@gmail.com" className="inline-flex min-h-11 shrink-0 items-center gap-2 whitespace-nowrap rounded-full bg-primary px-3 text-xs font-semibold text-primary-foreground shadow-[0_0_24px_rgba(59,130,246,0.2)] transition-all hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2">
            <Mail className="h-4 w-4" aria-hidden="true" />
            <span>Contact</span>
          </a>
        </div>
        <a href="mailto:hadi.budhy@gmail.com" className="hidden min-h-11 shrink-0 items-center gap-2 whitespace-nowrap rounded-full bg-primary px-3 text-xs font-semibold text-primary-foreground shadow-[0_0_24px_rgba(59,130,246,0.2)] transition-all hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 sm:inline-flex sm:px-4 sm:text-sm">
          <Mail className="h-4 w-4" aria-hidden="true" />
          <span>Contact Me</span>
        </a>
      </div>
    </header>
  );
}
