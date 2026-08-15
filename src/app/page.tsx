import Link from "next/link";
import { ArrowDownRight, ArrowRight, Mail } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { ProjectCard } from "@/components/ui/ProjectCard";
import { getAllProjects } from "@/lib/mdx";
import { careerArc, impactStats, skills } from "@/lib/profile";

export default function Home() {
  const projects = getAllProjects();
  const featuredProjects = projects.filter((project) => project.meta.featured);
  const supportingProjects = projects.filter((project) => !project.meta.featured);

  return (
    <div className="overflow-hidden">
      <section className="relative border-b border-white/[0.08]">
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_75%_20%,rgba(59,130,246,0.16),transparent_32%),radial-gradient(circle_at_15%_55%,rgba(14,165,233,0.08),transparent_28%)]" />
        <div className="pointer-events-none absolute inset-0 opacity-30 [background-image:linear-gradient(rgba(148,163,184,0.08)_1px,transparent_1px),linear-gradient(90deg,rgba(148,163,184,0.08)_1px,transparent_1px)] [background-size:4rem_4rem] [mask-image:linear-gradient(to_bottom,black,transparent_82%)]" />
          <div className="relative mx-auto grid max-w-6xl gap-10 px-4 pb-16 pt-12 sm:gap-12 sm:px-5 sm:pb-24 sm:pt-16 lg:grid-cols-[1.15fr_0.85fr] lg:items-center lg:gap-16 md:px-8 md:pb-32 md:pt-24">
          <div className="min-w-0">
            <div className="mb-7 flex flex-wrap items-center gap-3 text-xs font-bold uppercase tracking-[0.2em] text-primary">
              <span className="h-2 w-2 rounded-full bg-primary shadow-[0_0_16px_rgba(59,130,246,0.9)]" />
              Senior Data Analyst / Analytics Engineer
              <span className="text-muted-foreground">/ Jakarta, ID</span>
            </div>
            <h1 className="max-w-4xl break-words text-[2.7rem] font-black leading-[0.98] tracking-[-0.055em] text-foreground sm:text-6xl lg:text-7xl">
              I turn unreliable data into <span className="text-primary">decisions people can act on.</span>
            </h1>
            <p className="mt-7 max-w-2xl text-lg leading-8 text-muted-foreground md:text-xl">
              I turn messy business data into clear evidence, useful recommendations, and better decisions.
            </p>
            <div className="mt-9 flex flex-col gap-3 sm:flex-row">
              <Button size="lg" asChild className="w-full sm:w-auto">
                <Link href="#work">View My Work <ArrowRight className="ml-2 h-4 w-4" aria-hidden="true" /></Link>
              </Button>
              <Button size="lg" variant="outline" asChild className="w-full sm:w-auto">
                <a href="mailto:hadi.budhy@gmail.com"><Mail className="mr-2 h-4 w-4" aria-hidden="true" /> Contact Me</a>
              </Button>
            </div>
            <div className="mt-8 flex flex-wrap gap-x-6 gap-y-2 text-sm text-muted-foreground">
              <a href="https://github.com/hadibudhy" target="_blank" rel="noreferrer" className="transition-colors hover:text-foreground">GitHub ↗</a>
              <a href="https://linkedin.com/in/hadibudhy" target="_blank" rel="noreferrer" className="transition-colors hover:text-foreground">LinkedIn ↗</a>
              <span>~6 years turning data into decisions</span>
            </div>
          </div>

          <aside className="relative min-w-0 rounded-3xl border border-white/[0.12] bg-slate-950/65 p-5 shadow-2xl shadow-blue-950/20 backdrop-blur-sm sm:p-6 lg:p-8">
            <div className="mb-10 flex items-center justify-between text-xs font-bold uppercase tracking-[0.18em] text-muted-foreground">
              <span>What I bring</span>
              <ArrowDownRight className="h-5 w-5 text-primary" aria-hidden="true" />
            </div>
            <div className="space-y-7">
              {["Reliable data foundations", "Models built for a clear question", "Decision-ready analytics"].map((item, index) => (
                <div key={item} className="flex gap-4">
                  <span className="font-mono text-sm text-primary">0{index + 1}</span>
                  <div>
                    <h2 className="text-lg font-bold text-foreground">{item}</h2>
                    <p className="mt-1 text-sm leading-6 text-muted-foreground">{["Clean, tested data that teams can use with confidence.", "Models that answer a clear question instead of adding complexity.", "Dashboards and analysis that make the next action easier to see."][index]}</p>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-10 border-t border-white/[0.1] pt-5 text-sm text-muted-foreground">
              <span className="text-primary">Available for practical data work.</span> Let&apos;s make the numbers useful.
            </div>
          </aside>
        </div>
      </section>

      <section aria-label="Selected impact" className="border-b border-white/[0.08] bg-slate-900/35">
        <div className="mx-auto grid max-w-6xl gap-px px-4 sm:grid-cols-3 sm:px-8">
          {impactStats.map((stat) => (
            <div key={stat.label} className="border-white/[0.08] py-8 sm:border-r sm:px-8 sm:first:border-l">
              <div className="text-3xl font-black tracking-tight text-foreground md:text-4xl">{stat.value}</div>
              <div className="mt-2 text-xs font-bold uppercase tracking-[0.16em] text-muted-foreground">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      <section id="experience" className="scroll-mt-20 border-b border-white/[0.08]">
        <div className="mx-auto max-w-6xl px-4 py-16 sm:px-8 sm:py-20 md:py-28">
          <div className="grid gap-10 lg:grid-cols-[0.75fr_1.25fr] lg:gap-20">
            <div>
              <p className="section-kicker">Career arc</p>
              <h2 className="section-title mt-4">A career built across the data lifecycle.</h2>
              <p className="mt-5 leading-7 text-muted-foreground">From reporting foundations to data systems, my focus has stayed consistent: make complex information easier to trust and act on.</p>
            </div>
            <div className="space-y-0">
              {careerArc.map((item) => (
                <div key={item.index} className="group grid grid-cols-[2.5rem_1fr] gap-3 border-t border-white/[0.1] py-5 first:border-t-0 first:pt-0 sm:grid-cols-[3rem_1fr] sm:gap-5 sm:py-6">
                  <span className="font-mono text-sm text-primary">{item.index}</span>
                  <div>
                    <h3 className="text-xl font-bold text-foreground transition-colors group-hover:text-primary">{item.title}</h3>
                    <p className="mt-2 max-w-xl leading-7 text-muted-foreground">{item.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section id="work" className="scroll-mt-20 border-b border-white/[0.08]">
        <div className="mx-auto max-w-6xl px-4 py-16 sm:px-8 sm:py-20 md:py-28">
          <div className="mb-12 flex flex-col justify-between gap-6 md:flex-row md:items-end">
            <div>
              <p className="section-kicker">Selected work</p>
              <h2 className="section-title mt-4">Proof, not just promises.</h2>
              <p className="mt-5 max-w-2xl leading-7 text-muted-foreground">Case studies that explain the problem, the evidence, the business meaning, and what to consider next.</p>
            </div>
            <Link href="/projects" className="inline-flex items-center text-sm font-bold text-primary transition-colors hover:text-foreground">View all projects <ArrowRight className="ml-2 h-4 w-4" aria-hidden="true" /></Link>
          </div>
          <div className="grid gap-6 lg:grid-cols-2">
            {featuredProjects.map((project) => <ProjectCard key={project.slug} slug={project.slug} meta={project.meta} featured />)}
          </div>
          {supportingProjects.length > 0 && (
            <div className="mt-6 grid gap-6 lg:grid-cols-2">
              {supportingProjects.map((project) => <ProjectCard key={project.slug} slug={project.slug} meta={project.meta} />)}
            </div>
          )}
        </div>
      </section>

      <section id="skills" className="scroll-mt-20 border-b border-white/[0.08] bg-slate-900/35">
          <div className="mx-auto grid max-w-6xl gap-8 px-4 py-16 sm:px-8 sm:py-20 lg:grid-cols-[0.7fr_1.3fr] lg:gap-10 md:py-24">
          <div>
            <p className="section-kicker">Toolkit</p>
            <h2 className="section-title mt-4">Skills that support better decisions.</h2>
          </div>
          <div className="flex content-start flex-wrap gap-3">
            {skills.map((skill) => <span key={skill} className="rounded-full border border-white/[0.12] bg-card px-4 py-2.5 text-sm font-medium text-slate-200 transition-colors hover:border-primary/60 hover:text-primary">{skill}</span>)}
          </div>
        </div>
      </section>

      <section id="contact" className="scroll-mt-20">
        <div className="mx-auto max-w-6xl px-4 py-16 sm:px-8 sm:py-20 md:py-28">
          <div className="relative overflow-hidden rounded-3xl border border-primary/30 bg-primary/[0.08] p-6 sm:p-8 md:p-14">
            <div className="pointer-events-none absolute -right-16 -top-24 h-64 w-64 rounded-full bg-primary/20 blur-3xl" />
          <div className="relative grid gap-8 lg:grid-cols-[1fr_auto] lg:items-end">
              <div>
                <p className="section-kicker">Next conversation</p>
                <h2 className="mt-4 max-w-2xl text-3xl font-black tracking-tight text-foreground md:text-5xl">Have a messy data problem worth making clear?</h2>
                <p className="mt-5 max-w-xl leading-7 text-muted-foreground">I&apos;m open to conversations about analytics, data work, and decisions that need clearer evidence.</p>
              </div>
              <Button size="lg" asChild className="w-full sm:w-auto"><a href="mailto:hadi.budhy@gmail.com">Let&apos;s talk <ArrowRight className="ml-2 h-4 w-4" aria-hidden="true" /></a></Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
