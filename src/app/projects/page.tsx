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
      <section className="border-b border-border">
        <div className="mx-auto w-full max-w-3xl px-4 py-12 sm:px-6 sm:py-14 md:py-16">
          <p className="section-kicker">Case studies</p>
          <h1 className="mt-5 max-w-4xl break-words text-[2.7rem] font-black tracking-[-0.05em] text-foreground sm:text-5xl md:text-7xl">Case studies built around real business questions.</h1>
          <p className="mt-7 max-w-2xl text-lg leading-8 text-muted-foreground">A focused library of business case studies. Start with the featured work, then explore the deeper analyses across growth, operations, risk, finance, marketplaces, workforce analytics, and applied AI.</p>
        </div>
      </section>
      <section className="bg-muted/25">
        <div className="mx-auto w-full max-w-3xl px-4 py-12 sm:px-6 sm:py-16 md:py-20">
          <div className="mb-8">
            <p className="section-kicker">Flagship work</p>
            <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground">Four studies put the business question, the available evidence, and the limits of each analysis in view.</p>
          </div>
          {projects.length === 0 ? <div className="surface p-8"><p className="text-lg font-semibold text-foreground">No case studies are available yet.</p><p className="mt-2 text-muted-foreground">Please return shortly or use the contact link to request the current portfolio.</p></div> : <div className="grid gap-5 sm:grid-cols-2">{featuredProjects.map((project) => <ProjectCard key={project.slug} slug={project.slug} meta={project.meta} featured />)}</div>}
          {supportingProjects.length > 0 && <div className="mt-14"><p className="section-kicker mb-2">Supporting library</p><p className="mb-6 max-w-2xl text-sm leading-6 text-muted-foreground">Additional analyses demonstrate breadth across product, marketing, finance, marketplaces, workforce, and risk.</p><div className="grid gap-5 sm:grid-cols-2">{supportingProjects.map((project) => <ProjectCard key={project.slug} slug={project.slug} meta={project.meta} />)}</div></div>}
        </div>
      </section>
    </div>
  );
}
