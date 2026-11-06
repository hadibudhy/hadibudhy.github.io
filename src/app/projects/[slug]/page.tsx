import { getProjectBySlug, getAllProjects } from "@/lib/mdx";
import { notFound } from "next/navigation";
import { MDXRemote } from "next-mdx-remote/rsc";
import { Button } from "@/components/ui/Button";
import Link from "next/link";
import { format } from "date-fns";
import remarkGfm from "remark-gfm";
import type { ComponentProps } from "react";

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
    alternates: { canonical: `/projects/${project.slug}` },
    openGraph: {
      type: "article",
      url: `https://hadibudhy.github.io/projects/${project.slug}`,
      title: project.meta.title,
      description: project.meta.excerpt,
      siteName: "Hadi Budhy",
      images: [{
        url: project.meta.teaser ?? "/images/profile-illustration.jpg",
        alt: project.meta.title,
      }],
    },
    twitter: {
      card: "summary",
      title: project.meta.title,
      description: project.meta.excerpt,
      images: [project.meta.teaser ?? "/images/profile-illustration.jpg"],
    },
  };
}

type MDXImageProps = ComponentProps<"img">;

// Custom components for MDX
const components = {
  h2: (props: ComponentProps<"h2">) => <h2 className="mt-12 mb-4 break-words text-xl font-semibold tracking-normal text-foreground sm:mt-14 sm:text-2xl" {...props} />,
  h3: (props: ComponentProps<"h3">) => <h3 className="mt-8 mb-4 break-words text-lg font-bold tracking-tight text-foreground sm:text-xl" {...props} />,
  p: (props: ComponentProps<"p">) => <p className="leading-7 [&:not(:first-child)]:mt-6 text-muted-foreground" {...props} />,
  ul: (props: ComponentProps<"ul">) => <ul className="my-6 ml-6 list-disc [&>li]:mt-2 text-muted-foreground" {...props} />,
  ol: (props: ComponentProps<"ol">) => <ol className="my-6 ml-6 list-decimal [&>li]:mt-2 text-muted-foreground" {...props} />,
  li: (props: ComponentProps<"li">) => <li className="leading-7" {...props} />,
  blockquote: (props: ComponentProps<"blockquote">) => <blockquote className="mt-6 border-l-2 border-primary pl-5 italic text-foreground/80" {...props} />,
  img: ({ alt = "", ...props }: MDXImageProps) => (
    <span className="my-10 block min-w-0 border border-border bg-muted">
      <span role="group" aria-label="Scrollable chart; scroll horizontally to inspect labels" tabIndex={0} className="block min-w-0 max-w-full overflow-x-auto focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary">
        {/* MDX images have author-provided dimensions and are served from the static export. */}
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img className="block h-auto min-w-[672px] max-w-none w-full md:min-w-0 object-cover" loading="lazy" decoding="async" alt={alt} {...props} />
      </span>
      <span className="block px-4 pt-2 text-xs text-muted-foreground md:hidden">Scroll horizontally to inspect chart labels.</span>
      {alt && <span className="block border-t border-border px-4 py-3 text-sm leading-6 text-muted-foreground sm:px-5"><span className="font-semibold text-foreground">Chart takeaway:</span> {alt}</span>}
    </span>
  ),
  a: (props: ComponentProps<"a">) => <a className="font-medium text-primary underline underline-offset-4 hover:text-primary/80" {...props} />,
  pre: (props: ComponentProps<"pre">) => (
    <pre className="my-6 max-w-full overflow-x-auto border border-border bg-foreground p-4 text-sm leading-6 text-background" {...props} />
  ),
  table: (props: ComponentProps<"table">) => (
    <div className="my-8 w-full max-w-full overflow-x-auto border border-border">
      <table className="min-w-full text-sm" {...props} />
    </div>
  ),
  th: (props: ComponentProps<"th">) => <th className="border-b border-border bg-muted px-4 py-3 text-left font-bold text-foreground" {...props} />,
  td: (props: ComponentProps<"td">) => <td className="border-b border-border px-4 py-3 text-muted-foreground" {...props} />,
};

export default async function ProjectPage({ params }: Props) {
  const resolvedParams = await params;
  const project = getProjectBySlug(resolvedParams.slug);

  if (!project) {
    notFound();
  }

  const formattedDate = format(project.meta.date, 'MMMM yyyy');
  const kindLabel = project.meta.artifactLabel ?? {
    "analytics-engineering": "Analytics engineering",
    "product-analytics": "Product analytics",
    "experimentation-growth": "Experimentation & growth",
  }[project.meta.primaryTrack];
  const categoryLabel = project.meta.categories.join(", ");
  const technicalStart = project.content.search(/\n(?=## Technical (?:appendix|design)\b)/i);
  const summaryContent = technicalStart === -1 ? project.content : project.content.slice(0, technicalStart);
  const technicalContent = technicalStart === -1 ? "" : project.content.slice(technicalStart + 1);

  return (
    <article className="py-12 sm:py-16 md:py-24">
      <div className="container mx-auto min-w-0 max-w-3xl px-4 sm:px-6 md:px-8">
        <Button variant="ghost" asChild className="mb-8 -ml-4 text-muted-foreground hover:text-foreground sm:mb-10">
          <Link href="/projects"><span className="mr-2 text-lg" aria-hidden="true">←</span> Back to projects</Link>
        </Button>

        <header className="mb-12 sm:mb-16">
          <h1 className="break-words text-3xl font-bold tracking-normal leading-tight sm:text-4xl md:text-5xl">
            {project.meta.title}
          </h1>
          
          <div className="mb-6 flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-muted-foreground">
            {formattedDate && (
              <div className="flex items-center">
                Published {formattedDate}
              </div>
            )}
            {categoryLabel ? <span className="capitalize">{categoryLabel}</span> : <span>{kindLabel}</span>}
          </div>

          {project.meta.tags.length > 0 && (
            <p className="mb-8 text-sm leading-6 text-muted-foreground">{project.meta.tags.join(" · ")}</p>
          )}
        </header>

        <div className="prose prose-invert max-w-none">
          <MDXRemote
            source={summaryContent}
            components={components}
            options={{ mdxOptions: { remarkPlugins: [remarkGfm] } }}
          />
          {technicalContent && (
            <details className="my-10 border border-border bg-muted/30 p-5 sm:p-6">
              <summary className="cursor-pointer font-bold text-foreground">Read technical details</summary>
              <div className="mt-6 border-t border-border pt-2">
                <MDXRemote source={technicalContent} components={components} options={{ mdxOptions: { remarkPlugins: [remarkGfm] } }} />
              </div>
            </details>
          )}
        </div>
      </div>
    </article>
  );
}
