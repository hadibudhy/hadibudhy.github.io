import Image from "next/image";
import Link from "next/link";
import { Badge } from "@/components/ui/Badge";
import type { ProjectMeta } from "@/lib/mdx";

interface ProjectCardProps { slug: string; meta: ProjectMeta; featured?: boolean; }

export function ProjectCard({ slug, meta, featured = false }: ProjectCardProps) {
  const trackLabel = {
    "analytics-engineering": "Analytics engineering",
    "product-analytics": "Product analytics",
    "experimentation-growth": "Experimentation & growth",
  }[meta.primaryTrack];
  const kindLabel = meta.artifactLabel ?? trackLabel;
  const signalLabel = meta.kind === "methods" ? "Evidence boundary" : "Decision signal";

  return (
    <Link href={`/projects/${slug}`} className="group block h-full min-w-0 focus-ring">
      <article className="surface flex h-full min-w-0 flex-col overflow-hidden transition-colors hover:border-primary">
        {meta.teaser && <div className="relative aspect-[16/9] w-full overflow-hidden bg-muted"><Image src={meta.teaser} alt="" fill sizes="(max-width: 1024px) 100vw, 50vw" className="object-contain" unoptimized /></div>}
        <div className="flex min-w-0 w-full flex-1 flex-col justify-between p-5 sm:p-7">
          <div>
            <div className="mb-5 flex flex-wrap items-center gap-2"><span className="text-[0.68rem] font-bold uppercase tracking-[0.16em] text-primary">{kindLabel}</span>{meta.categories.slice(0, 1).map((category) => <span key={category} className="text-[0.68rem] font-bold uppercase tracking-[0.16em] text-foreground/70">{category}</span>)}{meta.tags.slice(0, featured ? 4 : 3).map((tag) => <Badge key={tag} variant="secondary">{tag}</Badge>)}</div>
            <h3 className={`${featured ? "text-xl sm:text-2xl" : "text-lg sm:text-xl"} mb-3 break-words font-bold tracking-tight text-foreground group-hover:text-primary`}>{meta.title}</h3>
            <p className="mb-5 text-sm leading-6 text-muted-foreground">{meta.excerpt}</p>
            {meta.problem && <div className="mb-4 break-words border-t border-border pt-4 text-sm leading-6 text-muted-foreground"><span className="mb-1 block text-[0.65rem] font-bold uppercase tracking-[0.16em] text-foreground">Business question</span>{meta.problem}</div>}
            {meta.result && <div className="break-words border-t border-primary/40 pt-4 text-sm leading-6 text-foreground"><span className="mb-1 block text-[0.65rem] font-bold uppercase tracking-[0.16em] text-primary">{signalLabel}</span>{meta.result}</div>}
          </div>
          <div className="mt-7 flex items-center justify-between gap-3 border-t border-border pt-5 text-sm font-bold text-primary"><span>{featured ? "Open case study" : "Read case study"}</span><span aria-hidden="true" className="text-lg transition-transform group-hover:translate-x-1">→</span></div>
        </div>
      </article>
    </Link>
  );
}
