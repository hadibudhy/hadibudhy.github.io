import Link from "next/link";
import Image from "next/image";
import { Button } from "@/components/ui/Button";
import { ProjectCard } from "@/components/ui/ProjectCard";
import { getAllProjects } from "@/lib/mdx";
import { capabilities, careerArc } from "@/lib/profile";

export default function Home() {
  const projects = getAllProjects();
  const featuredProjects = projects.filter((project) => project.meta.featured);

  return (
    <div>
      <section className="border-b border-border">
        <div className="mx-auto flex w-full max-w-3xl flex-col gap-8 px-4 pb-12 pt-8 sm:gap-10 sm:px-6 sm:pb-16 sm:pt-14">
          <div className="flex items-center gap-4 sm:gap-6">
            <Image src="/images/profile-illustration.jpg" alt="Illustrated profile portrait of Hadi Budhy" width={160} height={160} className="h-24 w-24 shrink-0 rounded-full border border-border object-cover object-top sm:h-32 sm:w-32" priority />
            <div className="flex flex-col gap-2">
              <p className="text-xl font-semibold tracking-tight text-foreground sm:text-2xl">Hadi Budhy</p>
              <p className="text-sm text-muted-foreground">Data Analyst · Growth &amp; Decision Analytics</p>
              <div className="flex gap-4 text-sm text-muted-foreground">
                <a href="https://github.com/hadibudhy" target="_blank" rel="noreferrer" className="hover:text-foreground">GitHub</a>
                <a href="https://linkedin.com/in/hadibudhy" target="_blank" rel="noreferrer" className="hover:text-foreground">LinkedIn</a>
              </div>
            </div>
          </div>
          <div className="space-y-5 sm:space-y-6">
            <h1 className="max-w-full text-[1.8rem] font-normal leading-tight tracking-tight text-foreground sm:text-[2.3rem]">Decision-ready analysis for growth, product, and operations teams.</h1>
            <p className="text-base font-light leading-7 text-muted-foreground sm:text-lg sm:leading-8">I turn messy data into evidence for what to invest in, what to test, and what to stop—while keeping uncertainty visible.</p>
            <p className="text-sm font-medium leading-6 text-primary">Primary target: Senior Data Analyst · Growth &amp; Decision Analytics. Secondary strengths: experimentation, product analytics, marketplace operations, and analytics engineering.</p>
            <p className="max-w-2xl text-base leading-7 text-foreground"><span className="font-semibold">Why hire me:</span> In professional work, I own alerting, warehouse pipelines, and live dashboards; in portfolio work, I show how to turn a growth question into a holdout, reject a weak causal comparison, separate marketplace proxies from demand, and build an auditable AI workflow with safe fallback.</p>
            <div className="flex flex-wrap gap-3 pt-2">
              <Button size="lg" asChild><Link href="#work">View the work <span className="ml-3" aria-hidden="true">→</span></Link></Button>
              <Button size="lg" variant="outline" asChild><a href="mailto:hadi.budhy@gmail.com">Get in touch</a></Button>
            </div>
          </div>
        </div>
      </section>

      <section id="experience" className="scroll-mt-20 border-b border-border">
        <div className="mx-auto w-full max-w-3xl px-4 py-14 sm:px-6 sm:py-16 md:py-20">
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
        <div className="mx-auto w-full max-w-3xl px-4 py-14 sm:px-6 sm:py-16 md:py-20">
          <div className="mb-12 flex flex-col justify-between gap-6 md:flex-row md:items-end">
            <div>
              <p className="section-kicker">Selected work</p>
              <h2 className="section-title mt-4">Selected case studies and analysis.</h2>
              <p className="mt-5 max-w-2xl leading-7 text-muted-foreground">{featuredProjects.length} featured case studies put the questions, evidence, and trade-offs first. The full library covers growth, product, operations, marketplace quality, and applied AI.</p>
            </div>
            <Link href="/projects" className="focus-ring inline-flex items-center text-sm font-bold text-primary transition-colors hover:text-foreground">View all projects <span className="ml-2 text-lg" aria-hidden="true">→</span></Link>
          </div>
          <div className="grid gap-5 sm:grid-cols-2">
            {featuredProjects.map((project) => <ProjectCard key={project.slug} slug={project.slug} meta={project.meta} featured />)}
          </div>
        </div>
      </section>

      <section id="skills" className="scroll-mt-20 border-b border-border bg-muted/40">
          <div className="mx-auto grid w-full max-w-3xl gap-8 px-4 py-14 sm:px-6 sm:py-16 lg:grid-cols-[0.7fr_1.3fr] lg:gap-10 md:py-20">
          <div>
            <p className="section-kicker">Toolkit</p>
            <h2 className="section-title mt-4">Capabilities demonstrated across work and case studies.</h2>
          </div>
          <div className="space-y-5">
            {capabilities.map((capability) => <div key={capability.title} className="border-t border-border pt-4 first:border-t-0 first:pt-0"><h3 className="font-semibold text-foreground">{capability.title}</h3><p className="mt-1 text-sm leading-6 text-muted-foreground">{capability.evidence}</p></div>)}
          </div>
        </div>
      </section>

      <section id="contact" className="scroll-mt-20">
        <div className="mx-auto w-full max-w-3xl px-4 py-14 sm:px-6 sm:py-16 md:py-20">
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
