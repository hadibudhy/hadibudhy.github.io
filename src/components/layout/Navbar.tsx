import Link from "next/link";

const links = [
  { label: "About", href: "/about" },
  { label: "Experience", href: "/#experience" },
  { label: "Work", href: "/#work" },
  { label: "Projects", href: "/projects" },
];

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b-2 border-foreground bg-background print:hidden">
      <div className="mx-auto flex min-h-14 w-full max-w-[1060px] items-center justify-between gap-4 px-4 py-3 sm:px-6 sm:py-4">
        <Link href="/" className="focus-ring flex min-w-0 shrink-0 items-center gap-3" aria-label="Hadi Budhy home">
          <span className="flex h-8 w-8 items-center justify-center rounded-[3px] bg-primary font-mono text-xs font-medium tracking-tight text-primary-foreground">HB</span>
          <span className="hidden text-sm font-bold tracking-tight text-foreground sm:inline">Hadi Budhy</span>
        </Link>
        <nav aria-label="Primary navigation" className="hidden min-w-0 items-center gap-5 text-sm font-semibold sm:flex md:gap-7">
          {links.map((link) => <Link key={link.href} href={link.href} className="focus-ring text-muted-foreground transition-colors hover:text-foreground">{link.label}</Link>)}
        </nav>
        <div className="flex items-center gap-2 sm:hidden">
          <details className="relative">
            <summary className="focus-ring flex min-h-10 cursor-pointer list-none items-center rounded-[3px] border border-border px-3 text-xs font-bold text-foreground [&::-webkit-details-marker]:hidden">Menu</summary>
            <div className="absolute right-0 top-12 z-50 w-52 rounded-[3px] border border-border bg-card p-2">
              {links.map((link) => <Link key={link.href} href={link.href} className="focus-ring flex min-h-11 items-center px-3 text-sm text-muted-foreground hover:bg-muted hover:text-foreground">{link.label}</Link>)}
            </div>
          </details>
          <a href="mailto:hadi.budhy@gmail.com" className="focus-ring inline-flex min-h-10 items-center rounded-[3px] border border-primary bg-primary px-3 text-xs font-bold text-primary-foreground transition-colors hover:bg-foreground hover:text-background">Contact</a>
        </div>
        <a href="mailto:hadi.budhy@gmail.com" className="focus-ring hidden min-h-10 items-center rounded-[3px] border border-primary bg-primary px-4 text-sm font-bold text-primary-foreground transition-colors hover:bg-foreground hover:text-background sm:inline-flex">Contact</a>
      </div>
    </header>
  );
}
