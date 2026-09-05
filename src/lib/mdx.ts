import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

export type ProjectKind = "flagship" | "completed" | "methods";
export type ProjectTrack = "analytics-engineering" | "product-analytics" | "experimentation-growth";

const contentDirectory = path.join(process.cwd(), 'src/content/projects');

export interface ProjectMeta {
  title: string;
  excerpt: string;
  date: Date;
  tags: string[];
  categories: string[];
  teaser?: string;
  problem?: string;
  result?: string;
  featured?: boolean;
  published?: boolean;
  kind: ProjectKind;
  artifactLabel?: string;
  evidenceVisuals: string[];
  caseId: string;
  primaryTrack: ProjectTrack;
  secondaryTracks: ProjectTrack[];
  displayOrder: number;
  evidenceManifest: string;
}

export interface Project {
  slug: string;
  meta: ProjectMeta;
  content: string;
}

function toStringArray(value: unknown): string[] {
  if (Array.isArray(value)) return value.filter((item): item is string => typeof item === 'string');
  return typeof value === 'string' ? [value] : [];
}

function parseDate(value: unknown): Date | null {
  const date = value instanceof Date ? value : new Date(String(value));
  return Number.isNaN(date.getTime()) ? null : date;
}

function normalizeMeta(data: Record<string, unknown>): ProjectMeta | null {
  const date = parseDate(data.date);
  if (typeof data.title !== 'string' || typeof data.excerpt !== 'string' || !date) return null;

  const published = data.published === true;
  const kind = data.kind;
  const validKind = kind === "flagship" || kind === "methods" || kind === "completed";
  const primaryTrack = data.primaryTrack;
  const validTrack = primaryTrack === "analytics-engineering" || primaryTrack === "product-analytics" || primaryTrack === "experimentation-growth";
  if (published && !validKind) {
    throw new Error(`Published project is missing a valid kind. Use flagship, completed, or methods.`);
  }
  if (published && kind === "methods") {
    throw new Error("Methods-only projects must remain unpublished until they have a completed project-specific result.");
  }
  if (published && (typeof data.caseId !== "string" || !validTrack || typeof data.displayOrder !== "number" || typeof data.evidenceManifest !== "string")) {
    throw new Error("Published project requires caseId, primaryTrack, displayOrder, and evidenceManifest.");
  }

  return {
    title: data.title,
    excerpt: data.excerpt,
    date,
    tags: toStringArray(data.tags),
    categories: toStringArray(data.categories),
    teaser: typeof data.header === 'object' && data.header !== null && 'teaser' in data.header && typeof data.header.teaser === 'string'
      ? data.header.teaser
      : undefined,
    problem: typeof data.problem === 'string' ? data.problem : undefined,
    result: typeof data.result === 'string' ? data.result : undefined,
    featured: data.featured === true,
    published,
    kind: validKind ? kind : "methods",
    artifactLabel: typeof data.artifactLabel === 'string' ? data.artifactLabel : undefined,
    evidenceVisuals: toStringArray(data.evidenceVisuals),
    caseId: typeof data.caseId === "string" ? data.caseId : "",
    primaryTrack: validTrack ? primaryTrack : "product-analytics",
    secondaryTracks: toStringArray(data.secondaryTracks) as ProjectTrack[],
    displayOrder: typeof data.displayOrder === "number" ? data.displayOrder : 999,
    evidenceManifest: typeof data.evidenceManifest === "string" ? data.evidenceManifest : "",
  };
}

export function getProjectBySlug(slug: string): Project | null {
  const realSlug = slug.replace(/\.md$/, '');
  if (realSlug !== path.basename(realSlug)) return null;

  const fullPath = path.join(contentDirectory, `${realSlug}.md`);
  
  if (!fs.existsSync(fullPath)) {
    return null;
  }
  
  const fileContents = fs.readFileSync(fullPath, 'utf8');
  const { data, content } = matter(fileContents);
  const meta = normalizeMeta(data);
  if (!meta) {
    throw new Error(`Invalid project front matter in ${fullPath}: title, excerpt, and a valid date are required.`);
  }
  
  if (meta.published === false) return null;

  const manifestPath = path.join(process.cwd(), "public", meta.evidenceManifest.replace(/^\//, ""));
  if (!fs.existsSync(manifestPath)) {
    throw new Error(`Published project ${realSlug} is missing evidence manifest ${meta.evidenceManifest}.`);
  }

  const visuals = new Set([...content.matchAll(/!\[[^\]]*\]\((\/images\/[^)]+)\)/g)].map((match) => match[1]));
  const evidenceVisuals = [...new Set(meta.evidenceVisuals)].filter((visual) => {
    const visualPath = path.join(process.cwd(), "public", visual);
    if (!visuals.has(visual) || !fs.existsSync(visualPath)) return false;
    return path.extname(visualPath) !== ".svg" || !fs.readFileSync(visualPath, "utf8").includes("CONCEPTUAL DESIGN");
  });
  if (evidenceVisuals.length < 3) {
    throw new Error(`Published project ${realSlug} has ${evidenceVisuals.length} valid declared evidence visuals; at least 3 are required.`);
  }

  return {
    slug: realSlug,
    meta,
    content,
  };
}

export function getAllProjects(): Project[] {
  if (!fs.existsSync(contentDirectory)) return [];
  
  const slugs = fs.readdirSync(contentDirectory);
  const projects = slugs
    .map((slug) => getProjectBySlug(slug))
    .filter((post): post is NonNullable<typeof post> => Boolean(post))
    .sort((post1, post2) => post1.meta.displayOrder - post2.meta.displayOrder || post1.meta.date.getTime() - post2.meta.date.getTime());

  const seen = new Set<string>();
  for (const project of projects) {
    if (seen.has(project.meta.caseId)) throw new Error(`Duplicate published caseId: ${project.meta.caseId}`);
    seen.add(project.meta.caseId);
  }
    
  return projects;
}
