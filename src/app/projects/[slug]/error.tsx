"use client";

import Link from "next/link";

export default function Error({ reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return <main className="mx-auto flex min-h-[60vh] max-w-3xl flex-col justify-center px-4 py-16 sm:px-8"><p className="section-kicker">Case study unavailable</p><h1 className="mt-4 text-4xl font-bold tracking-tight">This analysis could not load.</h1><p className="mt-5 leading-7 text-muted-foreground">Try again or return to the case-study library.</p><div className="mt-8 flex flex-wrap gap-3"><button type="button" onClick={() => reset()} className="focus-ring border border-primary bg-primary px-5 py-3 text-sm font-bold text-primary-foreground hover:bg-foreground hover:text-background">Try again</button><Link href="/projects" className="focus-ring border border-border px-5 py-3 text-sm font-bold hover:bg-muted">View all projects</Link></div></main>;
}
