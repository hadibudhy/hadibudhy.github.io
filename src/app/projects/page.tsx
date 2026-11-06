import { ProjectCard } from "@/components/ui/ProjectCard";
import { getAllProjects } from "@/lib/mdx";

export const metadata = {
  title: "Data Projects & Case Studies",
  description: "Case studies across data engineering, analytics, and applied data science, with methods, findings, and evidence limits.",
  alternates: { canonical: "/projects" },
  openGraph: {
    type: "website",
    url: "https://hadibudhy.github.io/projects",
    title: "Data Projects & Case Studies | Hadi Budhy",
    description: "Case studies across data engineering, analytics, and applied data science, with methods, findings, and evidence limits.",
    siteName: "Hadi Budhy",
    images: [{ url: "/images/profile-illustration.jpg", alt: "Illustrated profile portrait of Hadi Budhy" }],
  },
  twitter: {
    card: "summary",
    title: "Data Projects & Case Studies | Hadi Budhy",
    description: "Case studies across data engineering, analytics, and applied data science, with methods, findings, and evidence limits.",
    images: ["/images/profile-illustration.jpg"],
  },
};

export default function ProjectsPage() {
  const projects = getAllProjects();
  const featuredProjects = projects.filter((project) => project.meta.kind === "flagship");
  const completedProjects = projects.filter((project) => project.meta.kind === "completed");
  const trackLabels = [
    ["analytics-engineering", "Analytics engineering"],
    ["product-analytics", "Product analytics"],
    ["experimentation-growth", "Experimentation & growth"],
  ] as const;

  return (
    <div>
      <section>
        <div className="mx-auto w-full max-w-[1060px] px-4 pt-8 pb-6 sm:px-6 sm:py-12 md:py-14">
          <h1 className="max-w-4xl break-words text-4xl font-bold leading-tight tracking-normal text-foreground md:text-6xl">Case studies built around real business questions</h1>
          <p className="mt-5 max-w-2xl text-lg leading-8 text-muted-foreground">Data engineering, analytics, and applied data science with methods, findings, and limits made clear.</p>
        </div>
      </section>
      <section>
        <div className="mx-auto w-full max-w-[1060px] px-4 pt-6 pb-12 sm:px-6 sm:pb-16 md:pb-20">
          <div className="mb-8">
            <h2 className="text-2xl font-semibold tracking-normal text-foreground">Flagship projects</h2>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-muted-foreground">{featuredProjects.length} case studies across three areas of work.</p>
          </div>
          {projects.length === 0 ? <div className="py-8"><p className="text-lg font-semibold text-foreground">No case studies are available yet.</p><p className="mt-2 text-muted-foreground">Please return shortly or use the contact link to request the current portfolio.</p></div> : trackLabels.map(([track, label]) => { const items = featuredProjects.filter((project) => project.meta.primaryTrack === track); return items.length ? <div key={track} className="mb-10 last:mb-0"><p className="mb-3 text-sm font-semibold text-muted-foreground">{label}</p><div className="grid gap-8 md:grid-cols-2">{items.map((project) => <ProjectCard key={project.slug} slug={project.slug} meta={project.meta} featured />)}</div></div> : null })}
          {completedProjects.length > 0 && <div className="mt-14"><h2 className="text-2xl font-semibold tracking-normal text-foreground">Completed analyses</h2><p className="mt-2 mb-6 max-w-2xl text-sm leading-6 text-muted-foreground">Public analyses with computed findings, denominators, and decision boundaries.</p><div className="grid gap-8 md:grid-cols-2">{completedProjects.map((project) => <ProjectCard key={project.slug} slug={project.slug} meta={project.meta} />)}</div></div>}
        </div>
      </section>
    </div>
  );
}
