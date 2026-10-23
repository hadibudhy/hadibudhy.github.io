import Link from "next/link";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { capabilities, careerArc, education, experience, skills } from "@/lib/profile";

export const metadata = {
  title: "About | Data Engineering, Analytics & Data Science",
  description: "Data professional in Jakarta with BI and data analyst experience, plus public work in analytics engineering, product analytics, experimentation, and applied data science.",
  alternates: { canonical: "/about" },
};

export default function AboutPage() {
  return (
    <div>
      <section className="border-b border-border">
        <div className="mx-auto max-w-6xl px-4 py-16 sm:px-8 sm:py-20 md:py-28">
          <p className="section-kicker">About the work</p>
          <h1 className="mt-5 max-w-4xl break-words text-[2.7rem] font-bold tracking-[-0.05em] text-foreground sm:text-5xl md:text-7xl">End-to-end data work, from reliable foundations to evidence-based decisions.</h1>
          <div className="mt-8 grid gap-8 lg:grid-cols-[1fr_0.8fr] lg:gap-20">
            <div className="space-y-5 text-lg leading-8 text-muted-foreground">
              <p>Data professional based in Jakarta, Indonesia. Professional experience is grounded in BI and data analysis; public case studies demonstrate work across data engineering, product analytics, experimentation, and applied data science.</p>
              <p>I build pipelines and models, analyze product and business questions, and communicate what the evidence can and cannot support.</p>
            </div>
            <div className="border-l border-primary/50 pl-6 text-sm leading-7 text-muted-foreground">Work spans source validation, data pipelines, SQL modeling, metric governance, product funnels, retention, experimentation, and applied modeling.<p className="mt-5 text-xs font-bold uppercase tracking-[0.16em] text-primary">{education}</p></div>
          </div>
          <div className="mt-10 flex flex-col gap-3 sm:flex-row">
            <Button size="lg" asChild><a href="mailto:hadi.budhy@gmail.com">Get in Touch</a></Button>
            <Button size="lg" variant="outline" asChild><Link href="/projects">Explore the Work <span className="ml-3 text-lg" aria-hidden="true">→</span></Link></Button>
          </div>
          <div className="mt-10 border-l-2 border-primary/50 pl-5 text-sm leading-7 text-muted-foreground"><p className="font-bold uppercase tracking-[0.16em] text-primary">Real-world evidence boundary</p><p className="mt-2">Professional experience covers alerting, warehouse pipelines, live dashboards, campaign and survey models, and KPI work. Employer names, scale, adoption, and outcome metrics are kept private or are not verifiable in this public repository. The public case studies separately demonstrate independent engineering, analytical, and data science work; they are not employer results.</p></div>
        </div>
      </section>

      <section className="border-b border-border">
        <div className="mx-auto grid max-w-6xl gap-10 px-4 py-16 sm:px-8 sm:py-20 lg:grid-cols-[0.75fr_1.25fr] lg:gap-12 md:py-28">
          <div><p className="section-kicker">Career arc</p><h2 className="section-title mt-4">From reporting questions to product and data systems.</h2></div>
          <div>{careerArc.map((item) => <div key={item.index} className="grid grid-cols-[3rem_1fr] gap-5 border-t border-border py-6 first:border-t-0 first:pt-0"><span className="font-mono text-sm text-primary">{item.index}</span><div><h3 className="text-xl font-bold text-foreground">{item.title}</h3><p className="mt-2 leading-7 text-muted-foreground">{item.description}</p></div></div>)}</div>
        </div>
      </section>

      <section className="border-b border-border bg-muted/40">
        <div className="mx-auto max-w-6xl px-4 py-16 sm:px-8 sm:py-20 md:py-28">
          <div className="grid gap-10 lg:grid-cols-[0.75fr_1.25fr] lg:gap-12">
            <div><p className="section-kicker">Selected experience</p><h2 className="section-title mt-4">A progression from reporting to reliable decision systems.</h2><p className="mt-5 leading-7 text-muted-foreground">A concise view of work across four analytics roles, the data foundations built, and the decisions made clearer.</p></div>
            <div className="space-y-0">{experience.map((item) => <div key={`${item.period}-${item.role}`} className="border-t border-border py-6 first:border-t-0 first:pt-0"><div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-baseline"><h3 className="text-xl font-bold text-foreground">{item.role}</h3><span className="text-sm text-primary">{item.period}</span></div><p className="mt-1 text-sm font-semibold text-foreground/70">{item.setting}</p><p className="mt-3 max-w-2xl leading-7 text-muted-foreground">{item.description}</p></div>)}</div>
          </div>
        </div>
      </section>

      <section className="border-b border-border">
        <div className="mx-auto grid max-w-6xl gap-8 px-4 py-16 sm:px-8 sm:py-20 lg:grid-cols-[0.7fr_1.3fr] lg:gap-10 md:py-24">
            <div><p className="section-kicker">Capabilities</p><h2 className="section-title mt-4">A practical toolkit for careful analysis.</h2></div>
          <div className="space-y-5">{capabilities.map((capability) => <div key={capability.title} className="border-t border-border pt-4 first:border-t-0 first:pt-0"><h3 className="font-semibold text-foreground">{capability.title}</h3><p className="mt-1 text-sm leading-6 text-muted-foreground">{capability.evidence}</p></div>)}<div className="flex flex-wrap gap-2 pt-2">{skills.map((skill) => <Badge key={skill} variant="secondary" className="px-3 py-1.5 text-sm font-normal">{skill}</Badge>)}</div></div>
        </div>
      </section>
    </div>
  );
}
