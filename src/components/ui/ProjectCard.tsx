import Image from "next/image";
import Link from "next/link";
import type { ProjectMeta } from "@/lib/mdx";

interface ProjectCardProps { slug: string; meta: ProjectMeta; featured?: boolean; }

export function ProjectCard({ slug, meta, featured = false }: ProjectCardProps) {
  const trackLabel = {
    "analytics-engineering": "Analytics engineering",
    "product-analytics": "Product analytics",
    "experimentation-growth": "Experimentation & growth",
  }[meta.primaryTrack];
  const kindLabel = meta.artifactLabel ?? trackLabel;
  const summary = meta.problem || meta.excerpt;

  return (
    <Link href={`/projects/${slug}`} className="group block h-full min-w-0 focus-ring">
      <article className={`flex h-full min-w-0 flex-col overflow-hidden border border-border bg-card transition-colors hover:border-primary ${featured ? "sm:flex-row" : ""}`}>
        {meta.teaser && <div className={`relative aspect-[16/9] w-full shrink-0 overflow-hidden bg-white ${featured ? "sm:aspect-[16/10] sm:w-[190px] sm:self-start lg:w-[250px]" : ""}`}><Image src={meta.teaser} alt="" fill sizes="(max-width: 1024px) 100vw, 50vw" className={featured ? "object-contain" : "object-cover object-top"} unoptimized /></div>}
        <div className="flex min-w-0 w-full flex-1 flex-col p-5 sm:p-6">
          <p className="mb-2 text-sm font-medium text-muted-foreground">{kindLabel}</p>
          <h3 className={`${featured ? "text-xl" : "text-lg sm:text-xl"} mb-3 break-words font-semibold tracking-normal text-foreground group-hover:text-primary`}>{meta.title}</h3>
          <p className="text-sm leading-6 text-muted-foreground">{summary}</p>
          {meta.result && <div className="mt-4 break-words text-sm leading-6 text-foreground"><p className="mb-1 font-semibold">{meta.kind === "methods" ? "Evidence boundary" : "Finding"}</p><p>{meta.result}</p></div>}
          <span className="mt-auto pt-5 inline-flex w-fit items-center gap-2 text-sm font-semibold text-primary underline underline-offset-4 group-hover:text-foreground">Read case study <span aria-hidden="true" className="text-lg transition-transform group-hover:translate-x-1">→</span></span>
        </div>
      </article>
    </Link>
  );
}
