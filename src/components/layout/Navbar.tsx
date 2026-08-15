import Link from 'next/link';

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/80 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-16 max-w-5xl items-center justify-between px-4 md:px-8">
        <Link href="/" className="flex items-center space-x-2 transition-opacity hover:opacity-80">
          <span className="font-bold tracking-tight text-foreground text-lg">Hadi Budhy</span>
        </Link>
        <nav aria-label="Primary navigation" className="flex items-center space-x-6 text-sm font-medium">
          <Link href="/projects" className="text-muted-foreground hover:text-primary transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2">
            Projects
          </Link>
          <Link href="/about" className="text-muted-foreground hover:text-primary transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2">
            About
          </Link>
          <a
            href="mailto:hadi.budhy@gmail.com"
            className="hidden md:inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow-sm transition-all hover:bg-primary/90 hover:shadow-primary/25 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
          >
            Contact
          </a>
        </nav>
      </div>
    </header>
  );
}
