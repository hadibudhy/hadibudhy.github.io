import Link from "next/link";

const links = [
  { label: "About", href: "/about" },
  { label: "Experience", href: "/#experience" },
  { label: "Work", href: "/#work" },
  { label: "Skills", href: "/#skills" },
  { label: "Projects", href: "/projects" },
];

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b border-border bg-background/95 backdrop-blur-sm">
      <div className="mx-auto flex min-h-16 max-w-6xl items-center justify-between gap-4 px-4 sm:px-8">
        <Link href="/" className="focus-ring flex min-w-0 shrink-0 items-center gap-3" aria-label="Hadi Budhy home">
          <span className="flex h-9 w-9 items-center justify-center border border-foreground bg-foreground text-xs font-bold text-background">HB</span>
          <span className="hidden text-sm font-bold tracking-[0.14em] text-foreground sm:inline">HADI BUDHY</span>
        </Link>
        <nav aria-label="Primary navigation" className="hidden min-w-0 items-center gap-5 text-sm font-semibold sm:flex md:gap-7">
          {links.map((link) => <Link key={link.href} href={link.href} className="focus-ring text-muted-foreground transition-colors hover:text-foreground">{link.label}</Link>)}
        </nav>
        <div className="flex items-center gap-2 sm:hidden">
          <details className="relative">
            <summary className="focus-ring flex min-h-10 cursor-pointer list-none items-center border border-border px-3 text-xs font-bold text-foreground [&::-webkit-details-marker]:hidden">Menu</summary>
            <div className="absolute right-0 top-12 z-50 w-52 border border-border bg-card p-2">
              {links.map((link) => <Link key={link.href} href={link.href} className="focus-ring flex min-h-11 items-center px-3 text-sm text-muted-foreground hover:bg-muted hover:text-foreground">{link.label}</Link>)}
            </div>
          </details>
          <a href="mailto:hadi.budhy@gmail.com" className="focus-ring inline-flex min-h-10 items-center border border-primary bg-primary px-3 text-xs font-bold text-primary-foreground transition-colors hover:bg-foreground hover:text-background">Contact</a>
        </div>
        <a href="mailto:hadi.budhy@gmail.com" className="focus-ring hidden min-h-10 items-center border border-primary bg-primary px-4 text-sm font-bold text-primary-foreground transition-colors hover:bg-foreground hover:text-background sm:inline-flex">Contact</a>
      </div>
    </header>
  );
}
