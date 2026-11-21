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
    <Link href={`/projects/${slug}`} className="group block h-full min-w-0 rounded-xl focus-ring">
      <article className="surface-card lift-on-hover flex h-full min-w-0 flex-col overflow-hidden">
        {meta.teaser && <div className="relative aspect-[16/9] w-full overflow-hidden bg-muted"><Image src={meta.teaser} alt="" fill sizes="(max-width: 1024px) 100vw, 50vw" className="object-contain transition-transform duration-300 group-hover:scale-[1.02] motion-reduce:transition-none motion-reduce:group-hover:scale-100" unoptimized /></div>}
        <div className="flex min-w-0 w-full flex-1 flex-col p-5 sm:p-6">
          <div>
            <p className="mb-2 text-sm font-medium text-primary">{kindLabel}</p>
            <h3 className={`${featured ? "text-xl sm:text-2xl" : "text-lg sm:text-xl"} mb-3 break-words font-semibold leading-tight tracking-[-0.02em] text-foreground group-hover:text-primary`}>{meta.title}</h3>
            <p className="text-base leading-6 text-muted-foreground">{summary}</p>
            {meta.result && <div className="mt-4 break-words border-l-2 border-primary/30 pl-3 text-sm leading-6 text-foreground"><p className="mb-1 font-semibold">{meta.kind === "methods" ? "Evidence boundary" : "Finding"}</p><p>{meta.result}</p></div>}
          </div>
          <span className="mt-5 inline-flex w-fit items-center gap-2 text-sm font-semibold text-primary underline underline-offset-4 decoration-primary/40 group-hover:decoration-primary">Read case study <span aria-hidden="true" className="text-lg transition-transform group-hover:translate-x-1 motion-reduce:transition-none">→</span></span>
        </div>
      </article>
    </Link>
  );
}
