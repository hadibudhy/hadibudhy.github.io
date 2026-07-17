import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Mail, FileText, ArrowRight } from "lucide-react";
import Link from "next/link";

export const metadata = {
  title: "About",
  description: "About Hadi Budhy - Senior Data Analyst & Analytics Engineer",
};

export default function AboutPage() {
  const skills = [
    "SQL (BigQuery, Window Functions)",
    "Python (Pandas, scikit-learn, XGBoost)",
    "Google BigQuery",
    "dbt",
    "Apache Airflow",
    "ELT Pipelines (Stitch)",
    "n8n Workflow Automation",
    "Star/Dimensional Schema Design",
    "K-Means Clustering",
    "Predictive Modeling (Churn/LTV)",
    "A/B Testing & Cohort Analysis",
    "Looker Studio / Tableau / Power BI",
    "REST API Integration"
  ];

  return (
    <div className="py-24 md:py-32">
      <div className="container mx-auto max-w-4xl px-4 md:px-8">
        
        <div className="grid md:grid-cols-[1fr_300px] gap-12 items-start mb-24">
          <div>
            <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-6">
              About Me
            </h1>
            <p className="text-xl text-primary font-medium mb-8 leading-relaxed">
              I am a Senior Data Analyst and Analytics Engineer with ~6 years of experience based in Jakarta, Indonesia.
            </p>
            <div className="space-y-6 text-muted-foreground leading-relaxed text-lg">
              <p>
                I started in Business Intelligence and quickly grew into full-stack data work, driven by a desire to turn messy, fragmented pipelines into cohesive business decisions at scale.
              </p>
              <p>
                My expertise spans across the entire data lifecycle. From robust data engineering and dimensional modeling to predictive machine learning and building actionable dashboards, I focus on solutions that drive growth and operational efficiency.
              </p>
            </div>
            
            <div className="mt-10 flex gap-4">
              <Button asChild size="lg">
                <a href="mailto:hadi.budhy@gmail.com">
                  <Mail className="mr-2 h-4 w-4" /> Get in Touch
                </a>
              </Button>
              <Button variant="outline" asChild size="lg">
                <Link href="/projects">
                  View Projects <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </div>
          </div>
          
          <div className="sticky top-24 bg-card border border-border/50 rounded-2xl p-6 md:p-8 shadow-sm">
            <h3 className="font-bold text-lg mb-6">Core Skills</h3>
            <div className="flex flex-wrap gap-2">
              {skills.map(skill => (
                <Badge key={skill} variant="secondary" className="font-normal text-slate-300">
                  {skill}
                </Badge>
              ))}
            </div>
          </div>
        </div>

        <section className="mb-24">
          <h2 className="text-3xl font-bold tracking-tight mb-10 text-center">Quantified Impact</h2>
          <div className="grid sm:grid-cols-3 gap-6">
            <div className="bg-primary/5 border border-primary/20 rounded-2xl p-8 text-center transition-transform hover:-translate-y-1">
              <div className="text-4xl font-extrabold text-primary mb-2">&lt;10 min</div>
              <div className="text-sm font-medium text-slate-300 uppercase tracking-wide">Incident Response Time</div>
            </div>
            <div className="bg-primary/5 border border-primary/20 rounded-2xl p-8 text-center transition-transform hover:-translate-y-1">
              <div className="text-4xl font-extrabold text-primary mb-2">12-18%</div>
              <div className="text-sm font-medium text-slate-300 uppercase tracking-wide">Marketing Engagement Increase</div>
            </div>
            <div className="bg-primary/5 border border-primary/20 rounded-2xl p-8 text-center transition-transform hover:-translate-y-1">
              <div className="text-4xl font-extrabold text-primary mb-2">10M+</div>
              <div className="text-sm font-medium text-slate-300 uppercase tracking-wide">Rows Clustered</div>
            </div>
          </div>
        </section>

      </div>
    </div>
  );
}
