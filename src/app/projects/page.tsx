import { ProjectCard } from "@/components/ui/ProjectCard";
import { getAllProjects } from "@/lib/mdx";

export const metadata = {
  title: "Case Studies & Projects",
  description: "Deep dives into my data science and engineering projects.",
  alternates: { canonical: "/projects" },
  openGraph: {
    type: "website",
    url: "https://hadibudhy.github.io/projects",
    title: "Case Studies & Projects | Hadi Budhy",
    description: "Deep dives into my data science and engineering projects.",
    siteName: "Hadi Budhy",
  },
  twitter: {
    card: "summary",
    title: "Case Studies & Projects | Hadi Budhy",
    description: "Deep dives into my data science and engineering projects.",
  },
};

export default function ProjectsPage() {
  const projects = getAllProjects();

  return (
    <div className="py-24 md:py-32">
      <div className="container mx-auto max-w-5xl px-4 md:px-8">
        <div className="max-w-2xl mb-16">
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-6">
            Case Studies
          </h1>
          <p className="text-lg text-muted-foreground leading-relaxed">
            A selection of my work across data engineering, predictive modeling, and analytics. 
            Each project focuses on solving a specific business problem and driving measurable impact.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <ProjectCard 
              key={project.slug} 
              slug={project.slug} 
              meta={project.meta}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
