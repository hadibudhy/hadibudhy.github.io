import { ProjectCard } from "@/components/ui/ProjectCard";
import { getAllProjects } from "@/lib/mdx";

export const metadata = {
  title: "Case Studies & Projects",
  description: "Analytics engineering and product analytics case studies showing how reliable data supports better product decisions.",
  alternates: { canonical: "/projects" },
  openGraph: {
    type: "website",
    url: "https://hadibudhy.github.io/projects",
    title: "Case Studies & Projects | Hadi Budhy",
    description: "Analytics engineering and product analytics case studies showing how reliable data supports better product decisions.",
    siteName: "Hadi Budhy",
  },
  twitter: {
    card: "summary",
    title: "Case Studies & Projects | Hadi Budhy",
    description: "Analytics engineering and product analytics case studies showing how reliable data supports better product decisions.",
  },
};

export default function ProjectsPage() {
  const projects = getAllProjects();
  const featuredProjects = projects.filter((project) => project.meta.kind === "flagship");
  const completedProjects = projects.filter((project) => project.meta.kind === "completed");
  const trackLabels = [
    ["analytics-engineering", "Analytics Engineering"],
    ["product-analytics", "Product Analytics"],
    ["experimentation-growth", "Experimentation & Growth"],
  ] as const;

  return (
    <div>
      <section className="border-b border-border">
        <div className="mx-auto w-full max-w-3xl px-4 py-12 sm:px-6 sm:py-14 md:py-16">
          <p className="section-kicker">Case studies</p>
          <h1 className="mt-5 max-w-4xl break-words text-[2.7rem] font-black tracking-[-0.05em] text-foreground sm:text-5xl md:text-7xl">Case studies built around real business questions.</h1>
          <p className="mt-7 max-w-2xl text-lg leading-8 text-muted-foreground">A focused library showing how reliable data models, product analysis, and experimentation support clear decisions.</p>
        </div>
      </section>
      <section className="bg-muted/25">
        <div className="mx-auto w-full max-w-3xl px-4 py-12 sm:px-6 sm:py-16 md:py-20">
          <div className="mb-8">
            <p className="section-kicker">Flagship work</p>
            <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground">{featuredProjects.length} selected studies connect data foundations to product and growth decisions.</p>
          </div>
          {projects.length === 0 ? <div className="surface p-8"><p className="text-lg font-semibold text-foreground">No case studies are available yet.</p><p className="mt-2 text-muted-foreground">Please return shortly or use the contact link to request the current portfolio.</p></div> : trackLabels.map(([track, label]) => { const items = featuredProjects.filter((project) => project.meta.primaryTrack === track); return items.length ? <div key={track} className="mb-10 last:mb-0"><p className="section-kicker mb-4">{label}</p><div className="grid gap-5 sm:grid-cols-2">{items.map((project) => <ProjectCard key={project.slug} slug={project.slug} meta={project.meta} featured />)}</div></div> : null })}
          {completedProjects.length > 0 && <div className="mt-14"><p className="section-kicker mb-2">Completed analyses</p><p className="mb-6 max-w-2xl text-sm leading-6 text-muted-foreground">Completed public analyses with computed findings, explicit denominators, and decision boundaries.</p><div className="grid gap-5 sm:grid-cols-2">{completedProjects.map((project) => <ProjectCard key={project.slug} slug={project.slug} meta={project.meta} />)}</div></div>}
        </div>
      </section>
    </div>
  );
}
