export function Footer() {
  return (
    <footer className="mt-auto border-t border-border bg-muted/50 print:hidden">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-6 px-4 py-8 sm:px-6 md:flex-row md:items-end md:justify-between">
        <div>
          <p className="text-sm font-semibold tracking-tight text-foreground">Hadi Budhy</p>
          <p className="mt-2 text-sm leading-6 text-muted-foreground">Reliable metrics, product insight, and practical next steps.</p>
          <p className="mt-3 text-[13px] text-muted-foreground">© {new Date().getFullYear()} Hadi Budhy. All rights reserved.</p>
        </div>
        <div className="flex flex-wrap gap-x-5 gap-y-2 text-sm font-semibold">
          <a href="https://github.com/hadibudhy" target="_blank" rel="noreferrer" className="focus-ring text-muted-foreground underline decoration-transparent underline-offset-4 transition-colors hover:text-primary hover:decoration-current">GitHub</a>
          <a href="mailto:hadi.budhy@gmail.com" className="focus-ring text-muted-foreground underline decoration-transparent underline-offset-4 transition-colors hover:text-primary hover:decoration-current">Email</a>
          <a href="/privacy" className="focus-ring text-muted-foreground underline decoration-transparent underline-offset-4 transition-colors hover:text-primary hover:decoration-current">Privacy</a>
          <a href="/terms" className="focus-ring text-muted-foreground underline decoration-transparent underline-offset-4 transition-colors hover:text-primary hover:decoration-current">Terms</a>
        </div>
      </div>
    </footer>
  );
}
