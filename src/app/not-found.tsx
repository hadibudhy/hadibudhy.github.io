import Link from "next/link";

export default function NotFound() {
  return <main className="mx-auto flex min-h-[60vh] max-w-3xl flex-col justify-center px-4 py-16 sm:px-8"><p className="section-kicker">404</p><h1 className="mt-4 text-4xl font-bold tracking-tight sm:text-6xl">That page is not here.</h1><p className="mt-5 max-w-xl leading-7 text-muted-foreground">The link may be outdated, or the case study may have moved.</p><Link href="/projects" className="focus-ring mt-8 inline-flex w-fit border border-primary bg-primary px-5 py-3 text-sm font-bold text-primary-foreground hover:bg-foreground hover:text-background">Browse case studies</Link></main>;
}
