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
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-5 lg:px-8">
        <Link href="/" className="group flex items-center gap-3" aria-label="Hadi Budhy home">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-sm font-black text-primary-foreground transition-transform group-hover:rotate-6">HB</span>
          <span className="hidden text-sm font-bold tracking-[0.18em] text-foreground sm:inline">HADI BUDHY</span>
        </Link>
        <nav aria-label="Primary navigation" className="flex items-center gap-4 text-sm font-medium sm:gap-6">
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="hidden text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 sm:inline"
            >
              {link.label}
            </Link>
          ))}
          <Link
            href="/projects"
            className="text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
          >
            Projects
          </Link>
          <a
            href="mailto:hadi.budhy@gmail.com"
            className="inline-flex items-center gap-2 rounded-full bg-primary px-3.5 py-2 text-sm font-semibold text-primary-foreground shadow-[0_0_24px_rgba(59,130,246,0.2)] transition-all hover:-translate-y-0.5 hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 sm:px-4"
          >
            <Mail className="h-4 w-4 sm:hidden" aria-hidden="true" />
            <span>Contact<span className="hidden sm:inline"> Me</span></span>
          </a>
        </nav>
      </div>
    </header>
  );
}
