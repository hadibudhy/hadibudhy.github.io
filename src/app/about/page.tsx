import Link from "next/link";
import { ArrowRight, Mail } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { careerArc, impactStats, skills } from "@/lib/profile";

export const metadata = {
  title: "About",
  description: "About Hadi Budhy - Senior Data Analyst & Analytics Engineer",
  alternates: { canonical: "/about" },
  openGraph: {
    type: "website",
    url: "https://hadibudhy.github.io/about",
    title: "About | Hadi Budhy",
    description: "About Hadi Budhy - Senior Data Analyst & Analytics Engineer",
    siteName: "Hadi Budhy",
  },
  twitter: {
    card: "summary",
    title: "About | Hadi Budhy",
    description: "About Hadi Budhy - Senior Data Analyst & Analytics Engineer",
  },
};

export default function AboutPage() {
  return (
    <div>
      <section className="border-b border-white/[0.08]">
        <div className="mx-auto max-w-6xl px-5 py-20 sm:px-8 md:py-28">
          <p className="section-kicker">About the work</p>
          <h1 className="mt-5 max-w-4xl text-5xl font-black tracking-[-0.05em] text-foreground md:text-7xl">I make the path from messy data to a better decision shorter.</h1>
          <div className="mt-10 grid gap-10 md:grid-cols-[1fr_0.8fr] md:gap-20">
            <div className="space-y-5 text-lg leading-8 text-muted-foreground">
              <p>I am a Senior Data Analyst and Analytics Engineer with ~6 years of experience based in Jakarta, Indonesia.</p>
              <p>I started in Business Intelligence and grew into full-stack data work, driven by a desire to turn fragmented pipelines into cohesive business decisions at scale.</p>
            </div>
            <div className="border-l border-primary/50 pl-6 text-sm leading-7 text-slate-300">My work spans data engineering, dimensional modeling, predictive machine learning, and dashboards that help teams act with more confidence.</div>
          </div>
          <div className="mt-10 flex flex-col gap-3 sm:flex-row">
            <Button size="lg" asChild><a href="mailto:hadi.budhy@gmail.com"><Mail className="mr-2 h-4 w-4" aria-hidden="true" /> Get in Touch</a></Button>
            <Button size="lg" variant="outline" asChild><Link href="/projects">Explore the Work <ArrowRight className="ml-2 h-4 w-4" aria-hidden="true" /></Link></Button>
          </div>
        </div>
      </section>

      <section className="border-b border-white/[0.08] bg-slate-900/35">
        <div className="mx-auto grid max-w-6xl gap-px px-5 sm:grid-cols-3 sm:px-8">
          {impactStats.map((stat) => <div key={stat.label} className="py-8 sm:border-r sm:border-white/[0.08] sm:px-8 sm:first:border-l"><div className="text-3xl font-black text-foreground">{stat.value}</div><div className="mt-2 text-xs font-bold uppercase tracking-[0.16em] text-muted-foreground">{stat.label}</div></div>)}
        </div>
      </section>

      <section className="border-b border-white/[0.08]">
        <div className="mx-auto grid max-w-6xl gap-12 px-5 py-20 sm:px-8 md:grid-cols-[0.75fr_1.25fr] md:py-28">
          <div><p className="section-kicker">How I got here</p><h2 className="section-title mt-4">From reporting questions to data systems.</h2></div>
          <div>{careerArc.map((item) => <div key={item.index} className="grid grid-cols-[3rem_1fr] gap-5 border-t border-white/[0.1] py-6 first:border-t-0 first:pt-0"><span className="font-mono text-sm text-primary">{item.index}</span><div><h3 className="text-xl font-bold text-foreground">{item.title}</h3><p className="mt-2 leading-7 text-muted-foreground">{item.description}</p></div></div>)}</div>
        </div>
      </section>

      <section className="border-b border-white/[0.08]">
        <div className="mx-auto grid max-w-6xl gap-10 px-5 py-20 sm:px-8 md:grid-cols-[0.7fr_1.3fr] md:py-24">
          <div><p className="section-kicker">Skills</p><h2 className="section-title mt-4">A practical toolkit for the full lifecycle.</h2></div>
          <div className="flex flex-wrap content-start gap-3">{skills.map((skill) => <Badge key={skill} variant="secondary" className="px-3 py-1.5 text-sm font-normal text-slate-200">{skill}</Badge>)}</div>
        </div>
      </section>
    </div>
  );
}
