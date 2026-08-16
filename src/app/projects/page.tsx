import { ProjectCard } from "@/components/ui/ProjectCard";
import { getAllProjects } from "@/lib/mdx";

export const metadata = {
  title: "Case Studies & Projects",
  description: "Business-focused case studies across growth, operations, risk, finance, marketplaces, workforce analytics, and applied AI.",
  alternates: { canonical: "/projects" },
  openGraph: {
    type: "website",
    url: "https://hadibudhy.github.io/projects",
    title: "Case Studies & Projects | Hadi Budhy",
    description: "Business-focused case studies across growth, operations, risk, finance, marketplaces, workforce analytics, and applied AI.",
    siteName: "Hadi Budhy",
  },
  twitter: {
    card: "summary",
    title: "Case Studies & Projects | Hadi Budhy",
    description: "Business-focused case studies across growth, operations, risk, finance, marketplaces, workforce analytics, and applied AI.",
  },
};

export default function ProjectsPage() {
  const projects = getAllProjects();
  const featuredProjects = projects.filter((project) => project.meta.featured);
  const supportingProjects = projects.filter((project) => !project.meta.featured);

  return (
    <div>
      <section className="border-b border-white/[0.08]">
        <div className="mx-auto max-w-6xl px-4 py-16 sm:px-8 sm:py-20 md:py-28">
          <p className="section-kicker">Case studies</p>
          <h1 className="mt-5 max-w-4xl break-words text-[2.7rem] font-black tracking-[-0.05em] text-foreground sm:text-5xl md:text-7xl">The evidence behind better business decisions.</h1>
          <p className="mt-7 max-w-2xl text-lg leading-8 text-muted-foreground">A focused library of business case studies. Start with the featured work, then explore the deeper analyses across growth, operations, risk, finance, marketplaces, workforce analytics, and applied AI.</p>
        </div>
      </section>
      <section>
        <div className="mx-auto max-w-6xl px-4 py-14 sm:px-8 sm:py-20 md:py-24">
          <div className="grid gap-6 lg:grid-cols-2">
            {featuredProjects.map((project) => <ProjectCard key={project.slug} slug={project.slug} meta={project.meta} featured />)}
          </div>
          {supportingProjects.length > 0 && <div className="mt-16"><p className="section-kicker mb-6">More work</p><div className="grid gap-6 lg:grid-cols-2">{supportingProjects.map((project) => <ProjectCard key={project.slug} slug={project.slug} meta={project.meta} />)}</div></div>}
        </div>
      </section>
    </div>
  );
}
