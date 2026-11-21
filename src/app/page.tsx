import Image from "next/image";
import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { getAllProjects } from "@/lib/mdx";

const codeBase = "https://github.com/hadibudhy/hadibudhy.github.io";

const proofCards = [
  {
    area: "Engineering",
    title: "Product Event Model",
    result: "165 of 885,129 events lack session IDs; a staged dbt model keeps them visible alongside the composite-key funnel and quality marts.",
    caseHref: "/projects/2026-09-05-product-event-foundation",
    codeHref: `${codeBase}/tree/master/analytics/models`,
  },
  {
    area: "Analytics",
    title: "Campaign Incrementality",
    result: "Criteo benchmark ITT conversion lift: +0.115 percentage points (95% CI +0.108 to +0.122).",
    caseHref: "/projects/campaign-incrementality",
    codeHref: `${codeBase}/tree/master/projects/growth-analytics/01-campaign-incrementality`,
  },
  {
    area: "Science",
    title: "Fraud Screening",
    result: "72.8% recall at 96.9% precision on the untouched test set; threshold selected on validation data.",
    caseHref: "/projects/2026-05-10-fake-job-detection",
    codeHref: `${codeBase}/blob/master/projects/fake-job-detection/fake_job_ml_v2.py`,
  },
  {
    area: "Automation",
    title: "ComplaintFlow Triage",
    result: "On a 20-case synthetic fixture, the service reached 1.00 macro-F1, cited all 17 routed cases, and escalated all three unknown cases.",
    caseHref: "/projects/2026-08-23-complaintflow-ai-triage",
    codeHref: `${codeBase}/tree/master/ai_engineering/complaintflow`,
    evidenceHref: `${codeBase}/blob/master/public/data/evidence/complaintflow-ai-triage.json`,
  },
];

const skillGroups = [
  {
    area: "Engineering",
    links: [
      ["dbt", `${codeBase}/tree/master/analytics/models`],
      ["DuckDB", `${codeBase}/blob/master/analytics/load_rees46.py`],
      ["Data contracts", `${codeBase}/blob/master/analytics/models/schema.yml`],
    ],
  },
  {
    area: "Analytics",
    links: [
      ["Product funnels", "/projects/2026-09-05-product-event-foundation"],
      ["Metric definitions", `${codeBase}/blob/master/analytics/metrics.yml`],
      ["Incrementality and ITT", "/projects/campaign-incrementality"],
    ],
  },
  {
    area: "Science",
    links: [
      ["Text classification", `${codeBase}/blob/master/projects/fake-job-detection/fake_job_ml_v2.py`],
      ["Model evaluation", "/projects/2026-05-10-fake-job-detection"],
      ["Threshold selection", "/projects/2026-05-10-fake-job-detection"],
    ],
  },
  {
    area: "Automation",
    links: [
      ["GitHub Actions", `${codeBase}/blob/master/.github/workflows/nextjs.yml`],
      ["pytest contracts", `${codeBase}/blob/master/analytics/tests/test_contracts.py`],
      ["Evidence verification", `${codeBase}/blob/master/scripts/verify_published_evidence.py`],
    ],
  },
];

function EvidenceLink({ href, children }: { href: string; children: React.ReactNode }) {
  const isExternal = href.startsWith("https://");
  const className = "focus-ring text-primary underline underline-offset-4 hover:text-foreground";

  return isExternal ? (
    <a href={href} target="_blank" rel="noreferrer" className={className}>{children}</a>
  ) : (
    <Link href={href} className={className}>{children}</Link>
  );
}

export default function Home() {
  const projectCount = getAllProjects().length;

  return (
    <div>
      <section>
        <div className="mx-auto grid min-h-[calc(100svh-4rem)] w-full max-w-6xl gap-6 px-4 pb-8 pt-6 sm:px-6 sm:pb-12 sm:pt-8 md:grid-cols-12 md:items-center md:gap-10 md:py-14">
          <div className="min-w-0 md:col-span-7">
            <div className="flex items-center gap-4">
              <Image src="/images/profile-illustration.jpg" alt="Illustrated profile portrait of Hadi Budhy" width={160} height={160} className="h-14 w-14 shrink-0 rounded-lg border border-border object-cover object-top sm:h-20 sm:w-20" priority />
              <div>
                <p className="text-lg font-semibold tracking-tight text-foreground">Hadi Budhy</p>
                <p className="mt-1 text-sm text-muted-foreground">End-to-end data: engineering, analytics, science and automation</p>
              </div>
            </div>
            <div className="mt-6 space-y-4 sm:mt-8 sm:space-y-5">
              <p className="section-kicker">Data portfolio</p>
              <h1 className="max-w-3xl text-balance text-[2rem] font-medium leading-[1.08] tracking-[-0.04em] text-foreground sm:text-5xl md:text-[3.6rem]">From raw data to decisions you can inspect.</h1>
              <p className="max-w-2xl text-base leading-7 text-muted-foreground sm:text-lg sm:leading-8">I build and test pipelines, analysis and models, then automate the checks behind each result.</p>
              <div className="flex flex-wrap items-center gap-x-6 gap-y-3 pt-1">
                <Button size="lg" asChild><Link href="#proof">See the work <span className="ml-3" aria-hidden="true">→</span></Link></Button>
                <a href={codeBase} target="_blank" rel="noreferrer" className="focus-ring text-sm font-semibold text-primary underline underline-offset-4 decoration-primary/40 hover:decoration-primary">View the code</a>
              </div>
            </div>
          </div>
          <aside className="surface-card min-w-0 p-4 sm:p-6 md:col-span-5" aria-label="How portfolio work is tested and published">
            <p className="text-sm font-semibold text-foreground">From source to release</p>
            <div className="mt-4 grid gap-3 sm:mt-5 sm:gap-4">
              <div className="rounded-lg bg-brand-wash p-3 sm:p-4">
                <p className="text-sm font-semibold text-primary">Local source path</p>
                <p className="mt-1 text-sm leading-6 text-foreground">Public data <span aria-hidden="true">→</span> Python <span aria-hidden="true">→</span> DuckDB + dbt</p>
              </div>
              <div className="rounded-lg border border-border p-3 sm:p-4">
                <p className="text-sm font-semibold text-foreground">CI release checks</p>
                <p className="mt-1 text-sm leading-6 text-muted-foreground">pytest fixtures · dbt seeds · published evidence hashes</p>
              </div>
            </div>
            <Link href="/about" className="focus-ring mt-4 inline-flex text-sm font-semibold text-primary underline underline-offset-4 decoration-primary/40 hover:decoration-primary sm:mt-5">See how I build <span className="ml-2" aria-hidden="true">→</span></Link>
          </aside>
        </div>
      </section>

      <section id="proof" className="scroll-mt-20">
        <div className="mx-auto w-full max-w-6xl px-4 py-9 sm:px-6 sm:py-12">
          <h2 className="section-title">Four areas, one data path</h2>
          <div className="mt-7 grid gap-4 sm:grid-cols-2 sm:gap-5">
            {proofCards.map((card) => (
              <article key={card.area} className="surface-card lift-on-hover flex min-w-0 flex-col p-5 sm:p-6">
                <p className="text-sm font-medium text-primary">{card.area}</p>
                <h3 className="mt-2 text-xl font-semibold leading-tight tracking-[-0.02em] text-foreground sm:text-2xl">{card.title}</h3>
                <p className="mt-3 flex-1 text-base leading-6 text-muted-foreground">{card.result}</p>
                <div className="mt-5 flex flex-wrap gap-x-5 gap-y-2 text-sm font-semibold">
                  {card.caseHref && <EvidenceLink href={card.caseHref}>Read the case study</EvidenceLink>}
                  <EvidenceLink href={card.codeHref}>{card.area === "Automation" ? "View the workflow" : "View the code"}</EvidenceLink>
                  {card.evidenceHref && <EvidenceLink href={card.evidenceHref}>View evidence checks</EvidenceLink>}
                </div>
              </article>
            ))}
          </div>
          <p className="mt-6 text-sm text-muted-foreground">Browse <span className="font-semibold text-foreground">{projectCount} published case studies</span> on the <Link href="/projects" className="focus-ring font-semibold text-primary underline underline-offset-4 decoration-primary/40 hover:decoration-primary">full project list</Link>.</p>
        </div>
      </section>

      <section aria-labelledby="skills-heading">
        <div className="mx-auto w-full max-w-6xl px-4 pb-14 pt-6 sm:px-6 sm:pb-20">
          <h2 id="skills-heading" className="text-2xl font-semibold tracking-normal text-foreground">Skills with evidence</h2>
          <div className="mt-5 grid gap-x-8 gap-y-5 sm:grid-cols-2 lg:grid-cols-4">
            {skillGroups.map((group) => (
              <div key={group.area}>
                <h3 className="text-sm font-semibold text-foreground">{group.area}</h3>
                <p className="mt-2 flex flex-wrap gap-x-3 gap-y-2 text-sm leading-6">
                  {group.links.map(([label, href]) => <EvidenceLink key={label} href={href}>{label}</EvidenceLink>)}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
