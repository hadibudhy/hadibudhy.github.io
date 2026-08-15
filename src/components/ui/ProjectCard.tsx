import Image from "next/image";
import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import type { ProjectMeta } from "@/lib/mdx";

interface ProjectCardProps {
  slug: string;
  meta: ProjectMeta;
  featured?: boolean;
}

export function ProjectCard({ slug, meta, featured = false }: ProjectCardProps) {
  return (
    <Link href={`/projects/${slug}`} className={`group block h-full min-w-0 ${featured ? "lg:col-span-2" : ""}`}>
      <article className={`relative flex h-full min-w-0 overflow-hidden rounded-2xl border border-white/[0.1] bg-card/70 transition-all duration-300 hover:-translate-y-1 hover:border-primary/50 hover:bg-card hover:shadow-[0_18px_60px_rgba(2,6,23,0.45)] ${featured ? "lg:grid lg:grid-cols-[1.1fr_0.9fr]" : "flex-col"}`}>
        {meta.teaser && (
          <div className={`relative overflow-hidden bg-slate-950 ${featured ? "aspect-[16/10] lg:aspect-auto lg:min-h-full" : "aspect-[16/9]"}`}>
            <Image
              src={meta.teaser}
              alt=""
              fill
              sizes={featured ? "(max-width: 768px) 100vw, 55vw" : "(max-width: 768px) 100vw, 33vw"}
              className="object-cover transition-transform duration-500 group-hover:scale-105"
              unoptimized
            />
            <div className="absolute inset-0 bg-gradient-to-t from-slate-950/70 via-transparent to-transparent" />
          </div>
        )}
        <div className="flex min-w-0 flex-1 flex-col justify-between p-5 sm:p-6 lg:p-7">
          <div>
            <div className="mb-5 flex flex-wrap items-center gap-2">
              {meta.categories.slice(0, 1).map((category) => (
                <span key={category} className="text-[11px] font-bold uppercase tracking-[0.18em] text-primary">{category}</span>
              ))}
              {meta.tags.slice(0, featured ? 4 : 3).map((tag) => (
                <Badge key={tag} variant="secondary" className="text-[10px] uppercase tracking-wider">{tag}</Badge>
              ))}
            </div>
            <h3 className={`${featured ? "text-xl sm:text-2xl lg:text-3xl" : "text-lg sm:text-xl"} mb-3 break-words font-bold tracking-tight text-foreground transition-colors group-hover:text-primary`}>{meta.title}</h3>
            <p className="mb-5 text-sm leading-6 text-muted-foreground">{meta.excerpt}</p>
            {meta.result && (
              <div className="break-words border-l-2 border-primary/70 pl-4 text-sm leading-6 text-slate-200">
                <span className="mb-1 block text-[10px] font-bold uppercase tracking-[0.18em] text-primary">Result</span>
                {meta.result}
              </div>
            )}
          </div>
          <div className="mt-6 flex items-center justify-between gap-3 border-t border-white/[0.08] pt-5 text-sm font-semibold text-primary sm:mt-7">
            <span>{featured ? "Explore the case study" : "Read case study"}</span>
            <ArrowUpRight className="h-5 w-5 transition-transform duration-300 group-hover:-translate-y-1 group-hover:translate-x-1" aria-hidden="true" />
          </div>
        </div>
      </article>
    </Link>
  );
}
