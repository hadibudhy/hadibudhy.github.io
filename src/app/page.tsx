import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { ProjectCard } from "@/components/ui/ProjectCard";
import { getAllProjects } from "@/lib/mdx";
import { careerArc, skills } from "@/lib/profile";

export default function Home() {
  const projects = getAllProjects();
  const featuredProjects = projects.filter((project) => project.meta.featured);
  const supportingProjects = projects.filter((project) => !project.meta.featured);

  return (
    <div>
      <section className="border-b border-border">
          <div className="mx-auto grid max-w-6xl gap-10 px-4 pb-16 pt-12 sm:gap-12 sm:px-8 sm:pb-24 sm:pt-20 lg:grid-cols-[1.15fr_0.85fr] lg:items-center lg:gap-16 md:pb-32">
          <div className="min-w-0">
            <div className="mb-7 flex flex-wrap items-center gap-3 text-xs font-bold uppercase tracking-[0.2em] text-primary">
              <span className="h-2 w-2 bg-primary" />
              Senior Data Analyst / Analytics Engineer <span className="text-muted-foreground">• Applied AI</span>
              <span className="text-muted-foreground">/ Jakarta, ID</span>
            </div>
            <h1 className="max-w-4xl break-words text-[2.7rem] font-black leading-[0.98] tracking-[-0.055em] text-foreground sm:text-6xl lg:text-7xl">
              Making unreliable data easier to use for <span className="text-primary">better decisions.</span>
            </h1>
            <p className="mt-7 max-w-2xl text-lg leading-8 text-muted-foreground md:text-xl">
              Hadi Budhy works across growth, operations, and risk, using messy data to clarify what is happening and what could happen next.
            </p>
            <div className="mt-9 flex flex-col gap-3 sm:flex-row">
              <Button size="lg" asChild className="w-full sm:w-auto">
                <Link href="#work">View the Work <span className="ml-3 text-lg" aria-hidden="true">→</span></Link>
              </Button>
              <Button size="lg" variant="outline" asChild className="w-full sm:w-auto">
                <a href="mailto:hadi.budhy@gmail.com">Contact</a>
              </Button>
            </div>
            <div className="mt-8 flex flex-wrap gap-x-6 gap-y-2 text-sm text-muted-foreground">
              <a href="https://github.com/hadibudhy" target="_blank" rel="noreferrer" className="transition-colors hover:text-foreground">GitHub ↗</a>
              <a href="https://linkedin.com/in/hadibudhy" target="_blank" rel="noreferrer" className="transition-colors hover:text-foreground">LinkedIn ↗</a>
              <span>5+ years across BI, analytics, and data engineering</span>
            </div>
          </div>

          <aside className="surface min-w-0 p-5 sm:p-7 lg:p-8">
            <div className="mb-10 flex items-center justify-between text-xs font-bold uppercase tracking-[0.18em] text-muted-foreground">
              <span>What the work brings</span>
              <span className="text-lg text-primary" aria-hidden="true">↓</span>
            </div>
            <div className="space-y-7">
              {["Reliable data foundations", "Models built for a clear question", "Decision-ready analytics"].map((item, index) => (
                <div key={item} className="flex gap-4 border-t border-border pt-5 first:border-t-0 first:pt-0">
                  <span className="font-mono text-sm text-primary">0{index + 1}</span>
                  <div>
                    <h2 className="text-lg font-bold text-foreground">{item}</h2>
                    <p className="mt-1 text-sm leading-6 text-muted-foreground">{["Clean, tested data that teams can use with confidence.", "Models that answer a clear question instead of adding complexity.", "Dashboards and analysis that make the next action easier to see."][index]}</p>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-10 border-t border-border pt-5 text-sm text-muted-foreground">
              <span className="text-primary">Available for practical data work.</span> Making the numbers useful starts with a clear question.
            </div>
          </aside>
        </div>
      </section>

      <section id="experience" className="scroll-mt-20 border-b border-border">
        <div className="mx-auto max-w-6xl px-4 py-16 sm:px-8 sm:py-20 md:py-28">
          <div className="grid gap-10 lg:grid-cols-[0.75fr_1.25fr] lg:gap-20">
            <div>
              <p className="section-kicker">Career arc</p>
              <h2 className="section-title mt-4">A career built across the data lifecycle.</h2>
              <p className="mt-5 leading-7 text-muted-foreground">From reporting foundations to data systems, the focus has stayed consistent: make complex information easier to trust and act on.</p>
            </div>
            <div className="space-y-0">
              {careerArc.map((item) => (
                <div key={item.index} className="group grid grid-cols-[2.5rem_1fr] gap-3 border-t border-border py-5 first:border-t-0 first:pt-0 sm:grid-cols-[3rem_1fr] sm:gap-5 sm:py-6">
                  <span className="font-mono text-sm text-primary">{item.index}</span>
                  <div>
                    <h3 className="text-xl font-bold text-foreground group-hover:text-primary">{item.title}</h3>
                    <p className="mt-2 max-w-xl leading-7 text-muted-foreground">{item.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section id="work" className="scroll-mt-20 border-b border-border">
        <div className="mx-auto max-w-6xl px-4 py-16 sm:px-8 sm:py-20 md:py-28">
          <div className="mb-12 flex flex-col justify-between gap-6 md:flex-row md:items-end">
            <div>
              <p className="section-kicker">Selected work</p>
              <h2 className="section-title mt-4">Selected case studies and analysis.</h2>
              <p className="mt-5 max-w-2xl leading-7 text-muted-foreground">Five featured case studies put the questions, evidence, and trade-offs first. The full library covers growth, operations, risk, finance, marketplaces, workforce, and applied AI.</p>
            </div>
            <Link href="/projects" className="focus-ring inline-flex items-center text-sm font-bold text-primary transition-colors hover:text-foreground">View all projects <span className="ml-2 text-lg" aria-hidden="true">→</span></Link>
          </div>
          <div className="grid gap-6 lg:grid-cols-2">
            {featuredProjects.map((project) => <ProjectCard key={project.slug} slug={project.slug} meta={project.meta} featured />)}
          </div>
          {supportingProjects.length > 0 && (
            <div className="mt-16">
              <p className="section-kicker mb-6">More analysis</p>
              <div className="grid gap-6 lg:grid-cols-2">
                {supportingProjects.map((project) => <ProjectCard key={project.slug} slug={project.slug} meta={project.meta} />)}
              </div>
            </div>
          )}
        </div>
      </section>

      <section id="skills" className="scroll-mt-20 border-b border-border bg-muted/40">
          <div className="mx-auto grid max-w-6xl gap-8 px-4 py-16 sm:px-8 sm:py-20 lg:grid-cols-[0.7fr_1.3fr] lg:gap-10 md:py-24">
          <div>
            <p className="section-kicker">Toolkit</p>
            <h2 className="section-title mt-4">Skills for useful analysis.</h2>
          </div>
          <div className="flex content-start flex-wrap gap-3">
            {skills.map((skill) => <span key={skill} className="border border-border bg-card px-4 py-2.5 text-sm font-medium text-foreground transition-colors hover:border-primary hover:text-primary">{skill}</span>)}
          </div>
        </div>
      </section>

      <section id="contact" className="scroll-mt-20">
        <div className="mx-auto max-w-6xl px-4 py-16 sm:px-8 sm:py-20 md:py-28">
          <div className="border border-primary/40 bg-primary/10 p-6 sm:p-8 md:p-14">
          <div className="relative grid gap-8 lg:grid-cols-[1fr_auto] lg:items-end">
              <div>
                <p className="section-kicker">Next conversation</p>
                <h2 className="mt-4 max-w-2xl text-3xl font-black tracking-tight text-foreground md:text-5xl">Have a messy data problem worth making clear?</h2>
                <p className="mt-5 max-w-xl leading-7 text-muted-foreground">Available for conversations about analytics, data work, and decisions that need clearer evidence.</p>
              </div>
              <Button size="lg" asChild className="w-full sm:w-auto"><a href="mailto:hadi.budhy@gmail.com">Let&apos;s talk <span className="ml-3 text-lg" aria-hidden="true">→</span></a></Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
