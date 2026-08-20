import Link from "next/link";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { careerArc, education, experience, skills } from "@/lib/profile";

export const metadata = {
  title: "About",
  description: "Hadi Budhy’s experience across business intelligence, analytics engineering, automation, and applied AI.",
  alternates: { canonical: "/about" },
};

export default function AboutPage() {
  return (
    <div>
      <section className="border-b border-border">
        <div className="mx-auto max-w-6xl px-4 py-16 sm:px-8 sm:py-20 md:py-28">
          <p className="section-kicker">About the work</p>
          <h1 className="mt-5 max-w-4xl break-words text-[2.7rem] font-bold tracking-[-0.05em] text-foreground sm:text-5xl md:text-7xl">Hadi Budhy works from messy data toward a clearer decision.</h1>
          <div className="mt-8 grid gap-8 lg:grid-cols-[1fr_0.8fr] lg:gap-20">
            <div className="space-y-5 text-lg leading-8 text-muted-foreground">
              <p>Hadi Budhy is a Data Analyst and Analytics Engineer with 5+ years of experience across business intelligence, customer analytics, data automation, and applied AI, based in Jakarta, Indonesia.</p>
              <p>His work began in Business Intelligence and grew into data analysis, data engineering, and applied AI workflows. The goal is simple: turn scattered information into evidence that supports a more informed decision.</p>
            </div>
            <div className="border-l border-primary/50 pl-6 text-sm leading-7 text-muted-foreground">His work spans reliable data pipelines, forecasting and classification models, and dashboards that help teams understand what is happening and what to do next. This public summary keeps employer, client, and operational details intentionally high level.<p className="mt-5 text-xs font-bold uppercase tracking-[0.16em] text-primary">{education}</p></div>
          </div>
          <div className="mt-10 flex flex-col gap-3 sm:flex-row">
            <Button size="lg" asChild><a href="mailto:hadi.budhy@gmail.com">Get in Touch</a></Button>
            <Button size="lg" variant="outline" asChild><Link href="/projects">Explore the Work <span className="ml-3 text-lg" aria-hidden="true">→</span></Link></Button>
          </div>
        </div>
      </section>

      <section className="border-b border-border">
        <div className="mx-auto grid max-w-6xl gap-10 px-4 py-16 sm:px-8 sm:py-20 lg:grid-cols-[0.75fr_1.25fr] lg:gap-12 md:py-28">
          <div><p className="section-kicker">How Hadi got here</p><h2 className="section-title mt-4">From reporting questions to data systems.</h2></div>
          <div>{careerArc.map((item) => <div key={item.index} className="grid grid-cols-[3rem_1fr] gap-5 border-t border-border py-6 first:border-t-0 first:pt-0"><span className="font-mono text-sm text-primary">{item.index}</span><div><h3 className="text-xl font-bold text-foreground">{item.title}</h3><p className="mt-2 leading-7 text-muted-foreground">{item.description}</p></div></div>)}</div>
        </div>
      </section>

      <section className="border-b border-border bg-muted/40">
        <div className="mx-auto max-w-6xl px-4 py-16 sm:px-8 sm:py-20 md:py-28">
          <div className="grid gap-10 lg:grid-cols-[0.75fr_1.25fr] lg:gap-12">
            <div><p className="section-kicker">Selected experience</p><h2 className="section-title mt-4">A progression from reporting to decision systems.</h2><p className="mt-5 leading-7 text-muted-foreground">The public version focuses on the type of work and decisions supported, while keeping company and client details private.</p></div>
            <div className="space-y-0">{experience.map((item) => <div key={`${item.period}-${item.role}`} className="border-t border-border py-6 first:border-t-0 first:pt-0"><div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-baseline"><h3 className="text-xl font-bold text-foreground">{item.role}</h3><span className="text-sm text-primary">{item.period}</span></div><p className="mt-1 text-sm font-semibold text-foreground/70">{item.setting}</p><p className="mt-3 max-w-2xl leading-7 text-muted-foreground">{item.description}</p></div>)}</div>
          </div>
        </div>
      </section>

      <section className="border-b border-border">
        <div className="mx-auto grid max-w-6xl gap-8 px-4 py-16 sm:px-8 sm:py-20 lg:grid-cols-[0.7fr_1.3fr] lg:gap-10 md:py-24">
          <div><p className="section-kicker">Skills</p><h2 className="section-title mt-4">A practical toolkit for careful analysis.</h2></div>
          <div className="flex flex-wrap content-start gap-3">{skills.map((skill) => <Badge key={skill} variant="secondary" className="px-3 py-1.5 text-sm font-normal">{skill}</Badge>)}</div>
        </div>
      </section>
    </div>
  );
}
