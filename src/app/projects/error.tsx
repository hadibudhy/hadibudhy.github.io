"use client";

export default function Error({ reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return <main className="mx-auto flex min-h-[60vh] max-w-3xl flex-col justify-center px-4 py-16 sm:px-8"><p className="section-kicker">Something went wrong</p><h1 className="mt-4 text-4xl font-bold tracking-tight">The case studies could not load.</h1><p className="mt-5 leading-7 text-muted-foreground">Please try again. If the problem continues, return to the homepage.</p><button type="button" onClick={() => reset()} className="focus-ring mt-8 w-fit border border-primary bg-primary px-5 py-3 text-sm font-bold text-primary-foreground hover:bg-foreground hover:text-background">Try again</button></main>;
}
