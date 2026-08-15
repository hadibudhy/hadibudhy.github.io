import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

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
    // Sort projects by date in descending order
    .sort((post1, post2) => post2.meta.date.getTime() - post1.meta.date.getTime());
    
  return projects;
}
