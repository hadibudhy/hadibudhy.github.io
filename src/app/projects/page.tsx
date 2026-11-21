import { ProjectCard } from "@/components/ui/ProjectCard";
import { getAllProjects } from "@/lib/mdx";

export const metadata = {
  title: "Data Projects & Case Studies",
  description: "Published case studies across data engineering, analytics, and applied data science, with methods, findings, and evidence limits.",
  alternates: { canonical: "/projects" },
  openGraph: {
    type: "website",
    url: "https://hadibudhy.github.io/projects",
    title: "Data Projects & Case Studies | Hadi Budhy",
    description: "Published case studies across data engineering, analytics, and applied data science, with methods, findings, and evidence limits.",
    siteName: "Hadi Budhy",
    images: [{ url: "/images/profile-illustration.jpg", alt: "Illustrated profile portrait of Hadi Budhy" }],
  },
  twitter: {
    card: "summary",
    title: "Data Projects & Case Studies | Hadi Budhy",
    description: "Published case studies across data engineering, analytics, and applied data science, with methods, findings, and evidence limits.",
    images: ["/images/profile-illustration.jpg"],
  },
};

export default function ProjectsPage() {
  const projects = getAllProjects();
  const flagshipSlugs = [
    "2026-09-05-product-event-foundation",
    "campaign-incrementality",
    "2026-05-10-fake-job-detection",
    "2026-08-23-complaintflow-ai-triage",
  ];
  const supportingSlugs = new Set([
    "2026-09-05-financial-metrics",
    "2026-08-15-online-retail-customer-growth",
    "mta-congestion-pricing-causal-audit",
    "2026-10-12-business-network-hazard-screen",
    "2026-10-12-college-program-outcome-coverage",
    "marketplace-supply-demand",
  ]);
  const featuredProjects = flagshipSlugs.map((slug) => projects.find((project) => project.slug === slug)).filter((project) => project !== undefined);
  const supportingProjects = projects.filter((project) => supportingSlugs.has(project.slug));

  return (
    <div>
      <section>
        <div className="mx-auto w-full max-w-6xl px-4 pt-8 pb-6 sm:px-6 sm:py-12 md:py-14">
          <p className="section-kicker">Data portfolio</p>
          <h1 className="mt-3 max-w-4xl break-words text-balance text-4xl font-medium leading-tight tracking-[-0.035em] text-foreground md:text-5xl">Case studies from data to decisions</h1>
          <p className="mt-5 max-w-2xl text-lg leading-8 text-muted-foreground">{projects.length} published studies across engineering, analytics and data science. The homepage links each area to its code and evidence.</p>
        </div>
      </section>
      <section>
        <div className="mx-auto w-full max-w-6xl px-4 pt-6 pb-12 sm:px-6 sm:pb-16 md:pb-20">
          {projects.length === 0 ? <div className="py-8"><p className="text-lg font-semibold text-foreground">No case studies are available yet.</p><p className="mt-2 text-muted-foreground">Please return shortly or use the contact link to request the current portfolio.</p></div> : <>
            <div>
              <h2 className="mb-2 text-2xl font-semibold tracking-[-0.025em] text-foreground">Flagship case studies</h2>
              <p className="mb-6 max-w-2xl text-base leading-6 text-muted-foreground">One case study for engineering, analytics, data science and automation.</p>
              <div className="grid gap-5 sm:grid-cols-2 lg:gap-6">
                {featuredProjects.map((project) => <ProjectCard key={project.slug} slug={project.slug} meta={project.meta} featured />)}
              </div>
            </div>
            <div className="mt-16">
              <h2 className="mb-2 text-2xl font-semibold tracking-[-0.025em] text-foreground">Supporting studies</h2>
              <p className="mb-6 max-w-2xl text-base leading-6 text-muted-foreground">Six more studies, labeled by their main area of work.</p>
              <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3 lg:gap-6">{supportingProjects.map((project) => <ProjectCard key={project.slug} slug={project.slug} meta={project.meta} />)}</div>
            </div>
          </>}
        </div>
      </section>
    </div>
  );
}
