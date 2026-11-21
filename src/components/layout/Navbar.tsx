import Link from "next/link";

const links = [
  { label: "How I build", href: "/about" },
  { label: "Projects", href: "/projects" },
];

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b border-border bg-background print:hidden">
      <div className="mx-auto flex min-h-16 w-full max-w-6xl items-center justify-between gap-4 px-4 py-3 sm:px-6">
        <Link href="/" className="focus-ring flex min-w-0 shrink-0 items-center gap-3" aria-label="Hadi Budhy home">
          <span className="grid h-9 w-9 place-items-center rounded-md bg-primary text-xs font-semibold tracking-tight text-primary-foreground">HB</span>
          <span className="hidden text-sm font-medium tracking-tight text-foreground sm:inline">Hadi Budhy</span>
        </Link>
        <nav aria-label="Primary navigation" className="hidden min-w-0 items-center gap-7 text-sm font-medium sm:flex">
          {links.map((link) => <Link key={link.href} href={link.href} className="focus-ring text-muted-foreground transition-colors hover:text-primary">{link.label}</Link>)}
        </nav>
        <div className="flex items-center gap-2 sm:hidden">
          <details className="relative">
            <summary className="focus-ring flex min-h-10 cursor-pointer list-none items-center rounded-md border border-border bg-card px-3 text-[13px] font-semibold text-foreground [&::-webkit-details-marker]:hidden">Menu</summary>
            <div className="absolute right-0 top-12 z-50 w-52 rounded-lg border border-border bg-card p-2">
              {links.map((link) => <Link key={link.href} href={link.href} className="focus-ring flex min-h-11 items-center px-3 text-sm text-muted-foreground hover:bg-muted hover:text-foreground">{link.label}</Link>)}
            </div>
          </details>
          <a href="mailto:hadi.budhy@gmail.com" className="focus-ring inline-flex min-h-10 items-center rounded-md bg-primary px-3 text-[13px] font-semibold text-primary-foreground transition-colors hover:bg-brand-deep">Contact</a>
        </div>
        <a href="mailto:hadi.budhy@gmail.com" className="focus-ring hidden min-h-10 items-center rounded-md bg-primary px-4 text-sm font-semibold text-primary-foreground transition-colors hover:bg-brand-deep sm:inline-flex">Contact</a>
      </div>
    </header>
  );
}
