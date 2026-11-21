import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { howIveWorked } from "@/lib/profile";

const codeBase = "https://github.com/hadibudhy/hadibudhy.github.io";

const toolGroups = [
  {
    area: "Data engineering",
    links: [
      ["Python loaders", `${codeBase}/blob/master/analytics/load_rees46.py`],
      ["SQL and dbt models", `${codeBase}/tree/master/analytics/models`],
      ["DuckDB profile", `${codeBase}/blob/master/analytics/profiles.yml`],
      ["Product Event case study", "/projects/2026-09-05-product-event-foundation"],
    ],
  },
  {
    area: "Analytics",
    links: [
      ["Metric definitions", `${codeBase}/blob/master/analytics/metrics.yml`],
      ["Criteo ITT analysis", "/projects/campaign-incrementality"],
      ["Financial Metrics case study", "/projects/2026-09-05-financial-metrics"],
    ],
  },
  {
    area: "Data science",
    links: [
      ["TF-IDF/SVD and LightGBM", `${codeBase}/blob/master/projects/fake-job-detection/fake_job_ml_v2.py`],
      ["Threshold and test results", "/projects/2026-05-10-fake-job-detection"],
    ],
  },
  {
    area: "Automation",
    links: [
      ["GitHub Actions workflow", `${codeBase}/blob/master/.github/workflows/nextjs.yml`],
      ["pytest contract tests", `${codeBase}/blob/master/analytics/tests/test_contracts.py`],
      ["Published-evidence verifier", `${codeBase}/blob/master/scripts/verify_published_evidence.py`],
    ],
  },
];

function EvidenceLink({ href, label }: { href: string; label: string }) {
  const className = "focus-ring text-primary underline underline-offset-4 hover:text-foreground";

  return href.startsWith("https://") ? (
    <a href={href} target="_blank" rel="noreferrer" className={className}>{label}</a>
  ) : (
    <Link href={href} className={className}>{label}</Link>
  );
}

function PipelineDiagram() {
  return (
    <svg
      className="mx-auto block h-auto w-full max-w-[30rem]"
      viewBox="0 0 480 860"
      role="img"
      aria-labelledby="pipeline-title pipeline-description"
      xmlns="http://www.w3.org/2000/svg"
    >
      <title id="pipeline-title">Portfolio data and deployment pipeline</title>
      <desc id="pipeline-description">Public sources feed local Python loaders, DuckDB, and dbt models with local schema and SQL tests; a separate path uses Python analysis and chart scripts. Checked-in evidence manifests record source metadata and hashes. In GitHub Actions, pytest uses temporary fixtures and dbt uses committed seed data; the workflow also verifies manifests and chart hashes, builds the static site, and deploys the export to GitHub Pages.</desc>
      <defs>
        <marker id="pipeline-arrow" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
          <path d="M0,0 L8,4 L0,8 Z" fill="var(--color-primary)" />
        </marker>
      </defs>

      <g fill="var(--color-card)" stroke="var(--color-border)" strokeWidth="1.5">
        <rect x="24" y="20" width="432" height="86" rx="8" />
        <rect x="24" y="142" width="432" height="100" rx="8" />
        <rect x="24" y="282" width="432" height="100" rx="8" />
        <rect x="24" y="422" width="432" height="110" rx="8" />
        <rect x="24" y="572" width="432" height="132" rx="8" />
        <rect x="24" y="744" width="432" height="92" rx="8" />
      </g>

      <g fill="var(--color-foreground)" fontFamily="var(--font-ibm-plex-sans), sans-serif">
        <text x="44" y="52" fontSize="18" fontWeight="700">Public source snapshots</text>
        <text x="44" y="78" fontSize="14" fill="var(--color-muted-foreground)">REES46 events, SEC facts, and other cited datasets</text>

        <text x="44" y="176" fontSize="18" fontWeight="700">Local model path</text>
        <text x="44" y="201" fontSize="14" fill="var(--color-muted-foreground)">Python loaders → DuckDB raw tables</text>
        <text x="44" y="223" fontSize="14" fill="var(--color-muted-foreground)">dbt staging → intermediate → marts</text>

        <text x="44" y="316" fontSize="18" fontWeight="700">Separate chart path</text>
        <text x="44" y="342" fontSize="14" fill="var(--color-muted-foreground)">Analysis scripts write charts to public/images</text>
        <text x="44" y="364" fontSize="14" fill="var(--color-muted-foreground)">This work is separate from the CI dbt build</text>

        <text x="44" y="456" fontSize="18" fontWeight="700">Checked-in evidence</text>
        <text x="44" y="482" fontSize="14" fill="var(--color-muted-foreground)">Manifests record source metadata and source hashes</text>
        <text x="44" y="506" fontSize="14" fill="var(--color-muted-foreground)">Artifact hashes cover the published chart files</text>

        <text x="44" y="606" fontSize="18" fontWeight="700">GitHub Actions</text>
        <text x="44" y="632" fontSize="14" fill="var(--color-muted-foreground)">pytest uses temporary fixtures; dbt uses CI seeds</text>
        <text x="44" y="656" fontSize="14" fill="var(--color-muted-foreground)">dbt tests + verifier check models and evidence hashes</text>
        <text x="44" y="680" fontSize="14" fill="var(--color-muted-foreground)">Next.js lint/build creates the static export in out/</text>

        <text x="44" y="780" fontSize="18" fontWeight="700">GitHub Pages</text>
        <text x="44" y="806" fontSize="14" fill="var(--color-muted-foreground)">Deploys the static export from out/</text>
      </g>

      <g fill="none" stroke="var(--color-primary)" strokeWidth="2" markerEnd="url(#pipeline-arrow)">
        <path d="M240 106 V140" />
        <path d="M456 62 H470 V332 H458" />
        <path d="M24 192 H10 V477 H22" />
        <path d="M240 382 V420" />
        <path d="M240 532 V570" />
        <path d="M240 704 V742" />
      </g>
    </svg>
  );
}

export const metadata = {
  title: "How I Build | Engineering, Analytics, Science and Automation",
  description: "How I take public data from source to decision with tested models, clear evidence, and automated checks.",
  alternates: { canonical: "/about" },
};

export default function AboutPage() {
  return (
    <div>
      <section className="bg-brand-wash/40">
        <div className="mx-auto max-w-6xl px-4 py-12 sm:px-6 md:py-16">
          <p className="section-kicker">How I build</p>
          <h1 className="mt-3 max-w-4xl break-words text-balance text-4xl font-medium leading-tight tracking-[-0.035em] text-foreground md:text-5xl">From public source data to a decision people can inspect</h1>
          <p className="mt-6 max-w-3xl text-lg leading-8 text-muted-foreground">I start with public data, model it at a clear grain, and test the rules. Local runs use full source snapshots; CI checks fixtures, dbt seeds, and published evidence.</p>
          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Button size="lg" asChild><Link href="/projects">View projects <span className="ml-3 text-lg" aria-hidden="true">→</span></Link></Button>
            <Button size="lg" variant="outline" asChild><a href="mailto:hadi.budhy@gmail.com">Get in touch</a></Button>
          </div>
        </div>
      </section>

      <section aria-labelledby="pipeline-heading">
        <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 md:py-14">
          <h2 id="pipeline-heading" className="section-title">How the portfolio is built</h2>
          <figure className="surface-card mt-6 max-w-3xl p-3 sm:p-5">
            <PipelineDiagram />
            <figcaption className="mx-auto mt-4 max-w-xl border-t border-border pt-4 text-sm leading-6 text-muted-foreground">Full source processing and chart generation are separate from the CI path. Pytest uses temporary fixtures; dbt uses committed CI seeds. The workflow verifies checked-in evidence and chart files before it builds the site.</figcaption>
          </figure>
        </div>
      </section>

      <section aria-labelledby="experience-heading">
        <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 md:py-14">
          <h2 id="experience-heading" className="section-title">How I&apos;ve worked</h2>
          <p className="mt-5 max-w-3xl text-base leading-7 text-muted-foreground">{howIveWorked}</p>
        </div>
      </section>

      <section aria-labelledby="tools-heading">
        <div className="mx-auto max-w-6xl px-4 pb-14 pt-10 sm:px-6 md:pb-20">
          <h2 id="tools-heading" className="section-title">Tools and methods with evidence</h2>
          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {toolGroups.map((group) => (
              <div key={group.area} className="surface-card p-5 sm:p-6">
                <h3 className="font-semibold tracking-tight text-foreground">{group.area}</h3>
                <ul className="mt-3 space-y-2 text-sm leading-6">
                  {group.links.map(([label, href]) => (
                    <li key={label}><EvidenceLink href={href} label={label} /></li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
