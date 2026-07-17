import { Button } from "@/components/ui/Button";
import { ProjectCard } from "@/components/ui/ProjectCard";
import { getAllProjects } from "@/lib/mdx";
import { ArrowRight, Database, LineChart, BrainCircuit } from "lucide-react";
import Link from "next/link";

export default function Home() {
  const projects = getAllProjects();
  // For featured projects, we just take the first 3
  const featuredProjects = projects.slice(0, 3);

  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-24 pb-32 md:pt-36 md:pb-40">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#1e293b_1px,transparent_1px),linear-gradient(to_bottom,#1e293b_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] opacity-20" />
        <div className="container relative mx-auto max-w-5xl px-4 md:px-8 text-center">
          <div className="inline-flex items-center rounded-full border border-primary/30 bg-primary/10 px-3 py-1 text-sm font-medium text-primary mb-8 backdrop-blur-sm">
            <span className="flex h-2 w-2 rounded-full bg-primary mr-2 animate-pulse" />
            Senior Data Analyst & Analytics Engineer
          </div>
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight mb-6 bg-clip-text text-transparent bg-gradient-to-r from-slate-100 to-slate-500">
            Turning messy data pipelines into <br className="hidden md:block" />
            <span className="text-primary">business decisions at scale.</span>
          </h1>
          <p className="mx-auto max-w-2xl text-lg md:text-xl text-muted-foreground mb-10 leading-relaxed">
            I specialize in full-stack data engineering and predictive modeling. 
            I build the infrastructure that makes data reliable and the models that make it actionable.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button size="lg" asChild className="w-full sm:w-auto font-semibold">
              <Link href="/projects">
                View Case Studies <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
            <Button size="lg" variant="outline" asChild className="w-full sm:w-auto">
              <Link href="/about">About Me</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Quantified Impact / Value Prop */}
      <section className="py-24 bg-slate-900/50 border-y border-border/50">
        <div className="container mx-auto max-w-5xl px-4 md:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tight mb-4">Core Competencies</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Delivering measurable impact across the entire data lifecycle, from extraction to executive dashboards.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="p-6 rounded-2xl bg-card border border-border/50 shadow-sm">
              <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center mb-6 text-primary">
                <Database className="h-6 w-6" />
              </div>
              <h3 className="text-xl font-bold mb-3">Data Engineering</h3>
              <p className="text-muted-foreground leading-relaxed mb-6">
                Orchestrating robust ELT pipelines with Airflow, dbt, and BigQuery to eliminate manual overhead and ensure data integrity.
              </p>
              <div className="text-sm font-semibold text-slate-300 border-t border-border pt-4">
                <span className="text-primary mr-2">&lt;10 min</span> Incident Response Time
              </div>
            </div>

            <div className="p-6 rounded-2xl bg-card border border-border/50 shadow-sm">
              <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center mb-6 text-primary">
                <BrainCircuit className="h-6 w-6" />
              </div>
              <h3 className="text-xl font-bold mb-3">Machine Learning</h3>
              <p className="text-muted-foreground leading-relaxed mb-6">
                Deploying churn models, K-Means segmentation, and advanced NLP classifiers into production to drive revenue and mitigate fraud.
              </p>
              <div className="text-sm font-semibold text-slate-300 border-t border-border pt-4">
                <span className="text-primary mr-2">10M+</span> Rows Clustered
              </div>
            </div>

            <div className="p-6 rounded-2xl bg-card border border-border/50 shadow-sm">
              <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center mb-6 text-primary">
                <LineChart className="h-6 w-6" />
              </div>
              <h3 className="text-xl font-bold mb-3">Actionable Analytics</h3>
              <p className="text-muted-foreground leading-relaxed mb-6">
                Building self-service dashboards and conducting A/B tests that translate complex datasets into proactive business decisions.
              </p>
              <div className="text-sm font-semibold text-slate-300 border-t border-border pt-4">
                <span className="text-primary mr-2">12-18%</span> Marketing Engagement Increase
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Projects */}
      <section className="py-24 relative">
        <div className="container mx-auto max-w-5xl px-4 md:px-8">
          <div className="flex flex-col md:flex-row md:items-end justify-between mb-12 gap-6">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold tracking-tight mb-4">Featured Work</h2>
              <p className="text-muted-foreground max-w-2xl">
                Deep dives into real-world problems I've solved using data science and engineering.
              </p>
            </div>
            <Button variant="outline" asChild className="shrink-0">
              <Link href="/projects">View All Projects</Link>
            </Button>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {featuredProjects.map((project, idx) => (
              <ProjectCard 
                key={project.slug} 
                slug={project.slug} 
                meta={project.meta as any} 
                index={idx} 
              />
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
