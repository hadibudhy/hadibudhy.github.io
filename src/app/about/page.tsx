import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { capabilities, education, experience, skills } from "@/lib/profile";

export const metadata = {
  title: "About | Data Engineering, Analytics & Data Science",
  description: "Data professional in Jakarta with BI and data analyst experience, plus public work in analytics engineering, product analytics, experimentation, and applied data science.",
  alternates: { canonical: "/about" },
};

export default function AboutPage() {
  return (
    <div>
      <section>
        <div className="mx-auto max-w-3xl px-4 py-14 sm:px-6 md:py-20">
          <h1 className="max-w-3xl break-words text-4xl font-bold leading-tight tracking-normal text-foreground md:text-5xl">Data engineering, analytics, and applied data science</h1>
          <div className="mt-8 grid gap-8 lg:grid-cols-[1fr_0.8fr] lg:gap-20">
            <div className="space-y-5 text-lg leading-8 text-muted-foreground">
              <p>Based in Jakarta, Indonesia. My professional experience is in BI and data analysis; the public case studies show separate work in engineering, analytics, and data science.</p>
              <p>I build data pipelines and models, then explain what an analysis can and cannot support.</p>
            </div>
            <div className="text-sm leading-7 text-muted-foreground"><p className="font-semibold text-foreground">Education</p><p className="mt-1">{education}</p></div>
          </div>
          <div className="mt-10 flex flex-col gap-3 sm:flex-row">
            <Button size="lg" asChild><a href="mailto:hadi.budhy@gmail.com">Get in touch</a></Button>
            <Button size="lg" variant="outline" asChild><Link href="/projects">View projects <span className="ml-3 text-lg" aria-hidden="true">→</span></Link></Button>
          </div>
          <p className="mt-8 max-w-3xl text-sm leading-7 text-muted-foreground">Employer names, scale, adoption, and outcome metrics are private or not verifiable here. These case studies are independent projects, not employer results.</p>
        </div>
      </section>

      <section id="experience" className="scroll-mt-20">
        <div className="mx-auto max-w-3xl px-4 py-14 sm:px-6 md:py-16">
          <h2 className="section-title">Experience</h2>
          <div className="mt-8 space-y-9">{experience.map((item) => <article key={`${item.period}-${item.role}`}><div className="flex flex-col justify-between gap-1 sm:flex-row sm:items-baseline"><h3 className="text-xl font-semibold text-foreground">{item.role}</h3><span className="text-sm text-muted-foreground">{item.period}</span></div><p className="mt-1 text-sm font-medium text-foreground">{item.setting}</p><p className="mt-2 max-w-2xl leading-7 text-muted-foreground">{item.description}</p></article>)}</div>
        </div>
      </section>

      <section>
        <div className="mx-auto max-w-3xl px-4 py-14 sm:px-6 md:py-16">
          <h2 className="section-title">Capabilities</h2>
          <div className="mt-8 grid gap-x-10 gap-y-8 sm:grid-cols-2">{capabilities.map((capability) => <div key={capability.title}><h3 className="font-semibold text-foreground">{capability.title}</h3><p className="mt-2 text-sm leading-6 text-muted-foreground">{capability.evidence}</p></div>)}</div>
          <p className="mt-8 max-w-2xl text-sm leading-7 text-muted-foreground"><span className="font-semibold text-foreground">Tools and methods: </span>{skills.join(", ")}</p>
        </div>
      </section>
    </div>
  );
}
