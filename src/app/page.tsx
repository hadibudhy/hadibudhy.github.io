import Link from "next/link";
import Image from "next/image";
import { Button } from "@/components/ui/Button";
import { ProjectCard } from "@/components/ui/ProjectCard";
import { getAllProjects } from "@/lib/mdx";

export default function Home() {
  const projects = getAllProjects();
  const featuredProjects = projects.filter((project) => project.meta.featured);
  const trackLabels = [
    ["analytics-engineering", "Analytics Engineering"],
    ["product-analytics", "Product Analytics"],
    ["experimentation-growth", "Experimentation & Growth"],
  ] as const;

  return (
    <div>
      <section>
        <div className="mx-auto flex w-full max-w-3xl flex-col gap-8 px-4 pb-8 pt-8 sm:gap-10 sm:px-6 sm:pb-12 sm:pt-14">
          <div className="flex items-center gap-4 sm:gap-6">
            <Image src="/images/profile-illustration.jpg" alt="Illustrated profile portrait of Hadi Budhy" width={160} height={160} className="h-24 w-24 shrink-0 rounded-full border border-border object-cover object-top sm:h-32 sm:w-32" priority />
            <div className="flex flex-col gap-2">
              <p className="text-xl font-semibold tracking-tight text-foreground sm:text-2xl">Hadi Budhy</p>
              <p className="text-sm text-muted-foreground">Data professional across engineering, analytics &amp; data science</p>
              <div className="flex gap-4 text-sm text-muted-foreground">
                <a href="https://github.com/hadibudhy" target="_blank" rel="noreferrer" className="hover:text-foreground">GitHub</a>
                <a href="https://linkedin.com/in/hadibudhy" target="_blank" rel="noreferrer" className="hover:text-foreground">LinkedIn</a>
              </div>
            </div>
          </div>
          <div className="space-y-5 sm:space-y-6">
            <h1 className="max-w-full text-[1.8rem] font-normal leading-tight tracking-normal text-foreground sm:text-[2.3rem]">From reliable data foundations to analysis and applied data science</h1>
            <p className="text-base leading-7 text-muted-foreground sm:text-lg sm:leading-8">I build pipelines and models, answer product and business questions, and make the limits of evidence clear.</p>
            <div className="flex flex-wrap gap-3 pt-2">
              <Button size="lg" asChild><Link href="#work">View the work <span className="ml-3" aria-hidden="true">→</span></Link></Button>
              <Button size="lg" variant="outline" asChild><a href="mailto:hadi.budhy@gmail.com">Get in touch</a></Button>
            </div>
          </div>
        </div>
      </section>

      <section id="work" className="scroll-mt-20">
        <div className="mx-auto w-full max-w-3xl px-4 py-10 sm:px-6 sm:py-12 md:py-16">
          <div className="mb-10 flex flex-col justify-between gap-5 md:flex-row md:items-end">
            <div>
              <h2 className="section-title">Selected projects</h2>
              <p className="mt-4 max-w-2xl leading-7 text-muted-foreground">{featuredProjects.length} case studies across data engineering, product analytics, and applied data science.</p>
            </div>
            <Link href="/projects" className="focus-ring inline-flex items-center text-sm font-semibold text-primary underline underline-offset-4 transition-colors hover:text-foreground">All projects <span className="ml-2 text-lg" aria-hidden="true">→</span></Link>
          </div>
          {trackLabels.map(([track, label]) => {
            const trackProjects = featuredProjects.filter((project) => project.meta.primaryTrack === track);
            if (!trackProjects.length) return null;
            return <div key={track} className="mb-10 last:mb-0"><p className="mb-2 text-sm font-semibold text-muted-foreground">{label}</p><div className="grid gap-x-8 gap-y-8 sm:grid-cols-2">{trackProjects.map((project) => <ProjectCard key={project.slug} slug={project.slug} meta={project.meta} featured />)}</div></div>;
          })}
        </div>
      </section>

      <section id="contact" className="scroll-mt-20">
        <div className="mx-auto w-full max-w-3xl px-4 py-14 sm:px-6 sm:py-16 md:py-20">
          <div className="grid gap-6 border-t border-border pt-8 sm:gap-8 lg:grid-cols-[1fr_auto] lg:items-end">
              <div>
                <h2 className="max-w-2xl text-3xl font-semibold tracking-normal text-foreground md:text-4xl">Need reliable data for a decision?</h2>
                <p className="mt-4 max-w-xl leading-7 text-muted-foreground">Email me about a role, collaboration, or analytics problem.</p>
              </div>
              <Button size="lg" asChild className="w-full sm:w-auto"><a href="mailto:hadi.budhy@gmail.com">Get in touch <span className="ml-3 text-lg" aria-hidden="true">→</span></a></Button>
          </div>
        </div>
      </section>
    </div>
  );
}
