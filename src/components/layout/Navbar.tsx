import Link from 'next/link';
import { cn } from '@/lib/utils';

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/80 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-16 max-w-5xl items-center justify-between px-4 md:px-8">
        <Link href="/" className="flex items-center space-x-2 transition-opacity hover:opacity-80">
          <span className="font-bold tracking-tight text-foreground text-lg">Hadi Budhy</span>
        </Link>
        <nav className="flex items-center space-x-6 text-sm font-medium">
          <Link href="/projects" className="text-muted-foreground hover:text-primary transition-colors">
            Projects
          </Link>
          <Link href="/about" className="text-muted-foreground hover:text-primary transition-colors">
            About
          </Link>
          <Link 
            href="/resume.pdf" 
            className={cn(
              "hidden md:inline-flex items-center justify-center rounded-md text-sm font-medium",
              "bg-primary text-primary-foreground hover:bg-primary/90 h-9 px-4 py-2 transition-all",
              "shadow-sm hover:shadow-primary/25"
            )}
            target="_blank"
            rel="noopener noreferrer"
          >
            Resume
          </Link>
        </nav>
      </div>
    </header>
  );
}
