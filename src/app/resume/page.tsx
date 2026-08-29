import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { education, experience, skills } from "@/lib/profile";
import { getAllProjects } from "@/lib/mdx";

export const metadata = {
  title: "Resume",
  description: "Public resume for Hadi Budhy, a data analyst focused on growth and decision analytics.",
  alternates: { canonical: "/resume" },
};

export default function ResumePage() {
  const selectedProjects = getAllProjects().filter((project) => ["campaign-incrementality", "mta-congestion-pricing-causal-audit", "marketplace-supply-demand"].includes(project.slug));

  return (
    <article className="mx-auto w-full max-w-3xl px-4 py-14 print:max-w-none print:px-0 print:py-0 sm:px-6 sm:py-20">
      <header className="border-b border-border pb-10">
        <p className="section-kicker">Public resume</p>
        <h1 className="mt-4 text-4xl font-bold tracking-tight text-foreground sm:text-6xl">Hadi Budhy</h1>
        <p className="mt-3 text-lg text-primary">Data Analyst · Growth &amp; Decision Analytics</p>
        <p className="mt-4 max-w-2xl leading-7 text-muted-foreground">Jakarta, Indonesia · 5+ years across business intelligence, customer analytics, and data automation; applied AI demonstrated through public portfolio work.</p>
        <div className="mt-6 flex flex-wrap gap-x-5 gap-y-2 text-sm font-semibold">
          <a className="focus-ring text-primary hover:text-foreground" href="mailto:hadi.budhy@gmail.com">hadi.budhy@gmail.com</a>
          <a className="focus-ring text-primary hover:text-foreground" href="https://linkedin.com/in/hadibudhy" target="_blank" rel="noreferrer">LinkedIn</a>
          <a className="focus-ring text-primary hover:text-foreground" href="https://github.com/hadibudhy" target="_blank" rel="noreferrer">GitHub</a>
        </div>
      </header>

      <section className="border-b border-border py-10">
        <p className="section-kicker">Profile</p>
        <p className="mt-4 leading-7 text-muted-foreground">Turns messy business data into decision-ready analysis, reliable reporting, and practical tests. Public work demonstrates experimental design, causal restraint, and marketplace measurement.</p>
      </section>

      <section className="border-b border-border py-10">
        <p className="section-kicker">Experience</p>
        <div className="mt-6">
          {experience.map((item) => (
            <div key={`${item.period}-${item.role}`} className="border-t border-border py-6 first:border-t-0 first:pt-0">
              <div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-baseline">
                <h2 className="text-xl font-bold text-foreground">{item.role}</h2>
                <span className="text-sm text-primary">{item.period}</span>
              </div>
              <p className="mt-1 text-sm font-semibold text-foreground/70">{item.setting}</p>
              <p className="mt-3 leading-7 text-muted-foreground">{item.description}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="border-b border-border py-10">
        <p className="section-kicker">Selected evidence</p>
        <div className="mt-6 grid gap-5 sm:grid-cols-2">
          {selectedProjects.map((project) => (
            <Link key={project.slug} href={`/projects/${project.slug}`} className="focus-ring border-t border-border pt-4 hover:border-primary">
              <h2 className="font-bold text-foreground">{project.meta.title}</h2>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">{project.meta.excerpt}</p>
            </Link>
          ))}
        </div>
      </section>

      <section className="border-b border-border py-10">
        <div>
          <p className="section-kicker">Skills &amp; education</p>
          <p className="mt-5 text-sm leading-7 text-muted-foreground">{skills.join(" · ")}</p>
          <p className="mt-6 text-sm font-semibold leading-6 text-foreground">{education}</p>
        </div>
      </section>

      <footer className="pt-10">
        <p className="text-sm leading-6 text-muted-foreground">Professional employer names, scale, adoption, and outcome metrics are omitted when they cannot be verified in this public repository. Role-specific context can be discussed in an interview subject to confidentiality.</p>
        <div className="mt-6 flex flex-wrap gap-3 print:hidden">
          <Button asChild><a href="mailto:hadi.budhy@gmail.com">Contact Hadi</a></Button>
          <Button variant="outline" asChild><Link href="/projects">Review case studies</Link></Button>
        </div>
      </footer>
    </article>
  );
}
