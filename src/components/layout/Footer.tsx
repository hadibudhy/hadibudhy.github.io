export function Footer() {
  return (
    <footer className="mt-auto border-t border-border bg-muted/40">
      <div className="mx-auto flex w-full max-w-3xl flex-col gap-6 px-4 py-8 sm:px-6 md:flex-row md:items-end md:justify-between">
        <div>
          <p className="text-sm font-semibold text-foreground">Hadi Budhy</p>
          <p className="mt-2 text-sm leading-6 text-muted-foreground">Data analysis, dependable systems, and practical next steps.</p>
          <p className="mt-3 text-xs text-muted-foreground/70">© {new Date().getFullYear()} Hadi Budhy. All rights reserved.</p>
        </div>
        <div className="flex flex-wrap gap-x-5 gap-y-2 text-sm font-semibold">
          <a href="https://github.com/hadibudhy" target="_blank" rel="noreferrer" className="focus-ring text-muted-foreground hover:text-primary">GitHub</a>
          <a href="https://linkedin.com/in/hadibudhy" target="_blank" rel="noreferrer" className="focus-ring text-muted-foreground hover:text-primary">LinkedIn</a>
          <a href="mailto:hadi.budhy@gmail.com" className="focus-ring text-muted-foreground hover:text-primary">Email</a>
          <a href="/privacy" className="focus-ring text-muted-foreground hover:text-primary">Privacy</a>
          <a href="/terms" className="focus-ring text-muted-foreground hover:text-primary">Terms</a>
        </div>
      </div>
    </footer>
  );
}
