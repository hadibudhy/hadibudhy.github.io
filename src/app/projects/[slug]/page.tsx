import { getProjectBySlug, getAllProjects } from "@/lib/mdx";
import { notFound } from "next/navigation";
import { MDXRemote } from "next-mdx-remote/rsc";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { ArrowLeft, Calendar, Tag } from "lucide-react";
import Link from "next/link";
import { format, parseISO } from "date-fns";

interface Props {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  const projects = getAllProjects();
  return projects.map((post) => ({
    slug: post.slug,
  }));
}

export async function generateMetadata({ params }: Props) {
  const resolvedParams = await params;
  const project = getProjectBySlug(resolvedParams.slug);
  if (!project) return {};

  return {
    title: project.meta.title,
    description: project.meta.excerpt,
  };
}

// Custom components for MDX
const components = {
  h2: (props: any) => <h2 className="text-2xl font-bold mt-12 mb-6 tracking-tight text-slate-100 border-b border-border pb-2" {...props} />,
  h3: (props: any) => <h3 className="text-xl font-bold mt-8 mb-4 tracking-tight text-slate-200" {...props} />,
  p: (props: any) => <p className="leading-7 [&:not(:first-child)]:mt-6 text-muted-foreground" {...props} />,
  ul: (props: any) => <ul className="my-6 ml-6 list-disc [&>li]:mt-2 text-muted-foreground" {...props} />,
  ol: (props: any) => <ol className="my-6 ml-6 list-decimal [&>li]:mt-2 text-muted-foreground" {...props} />,
  li: (props: any) => <li className="leading-7" {...props} />,
  blockquote: (props: any) => (
    <blockquote className="mt-6 border-l-4 border-primary pl-6 italic text-slate-300 bg-slate-900/50 py-4 pr-4 rounded-r-lg" {...props} />
  ),
  img: (props: any) => (
    <div className="my-10 rounded-xl overflow-hidden border border-border/50 bg-slate-900/50 shadow-lg">
      <img className="w-full h-auto object-cover" loading="lazy" {...props} />
    </div>
  ),
  a: (props: any) => <a className="font-medium text-primary underline underline-offset-4 hover:text-primary/80" {...props} />,
  table: (props: any) => (
    <div className="my-8 w-full overflow-y-auto rounded-lg border border-border">
      <table className="w-full overflow-hidden text-sm" {...props} />
    </div>
  ),
  th: (props: any) => <th className="border-b border-border bg-slate-900 px-4 py-3 text-left font-bold text-slate-200" {...props} />,
  td: (props: any) => <td className="border-b border-border/50 px-4 py-3 text-muted-foreground" {...props} />,
};

export default async function ProjectPage({ params }: Props) {
  const resolvedParams = await params;
  const project = getProjectBySlug(resolvedParams.slug);

  if (!project) {
    notFound();
  }

  const formattedDate = project.meta.date 
    ? (typeof project.meta.date === 'string' 
        ? format(parseISO(project.meta.date), 'MMMM yyyy')
        : format(new Date(project.meta.date), 'MMMM yyyy'))
    : '';

  return (
    <article className="py-16 md:py-24">
      <div className="container mx-auto max-w-3xl px-4 md:px-8">
        <Button variant="ghost" asChild className="mb-10 -ml-4 text-muted-foreground hover:text-foreground">
          <Link href="/projects">
            <ArrowLeft className="mr-2 h-4 w-4" /> Back to projects
          </Link>
        </Button>

        <header className="mb-16">
          <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight mb-6 leading-tight">
            {project.meta.title}
          </h1>
          
          <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground mb-8">
            {formattedDate && (
              <div className="flex items-center">
                <Calendar className="mr-2 h-4 w-4" />
                {formattedDate}
              </div>
            )}
            {project.meta.categories && (
              <div className="flex items-center capitalize">
                <Tag className="mr-2 h-4 w-4" />
                {project.meta.categories}
              </div>
            )}
          </div>

          {project.meta.tags && (
            <div className="flex flex-wrap gap-2">
              {project.meta.tags.map((tag: string) => (
                <Badge key={tag} variant="secondary" className="uppercase tracking-wider text-[10px]">
                  {tag}
                </Badge>
              ))}
            </div>
          )}
        </header>

        {/* TL;DR Section - A strong addition for recruiters */}
        {project.meta.excerpt && (
          <div className="bg-primary/5 border border-primary/20 rounded-2xl p-6 md:p-8 mb-16">
            <h3 className="text-lg font-bold text-primary mb-3 uppercase tracking-wider text-sm">TL;DR Impact</h3>
            <p className="text-lg text-slate-200 leading-relaxed font-medium">
              {project.meta.excerpt}
            </p>
          </div>
        )}

        <div className="prose prose-invert max-w-none">
          <MDXRemote source={project.content} components={components} />
        </div>
      </div>
    </article>
  );
}
