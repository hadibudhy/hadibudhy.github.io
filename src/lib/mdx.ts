import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

const contentDirectory = path.join(process.cwd(), 'src/content/projects');

export function getProjectBySlug(slug: string) {
  const realSlug = slug.replace(/\.md$/, '');
  const fullPath = path.join(contentDirectory, `${realSlug}.md`);
  
  if (!fs.existsSync(fullPath)) {
    return null;
  }
  
  const fileContents = fs.readFileSync(fullPath, 'utf8');
  const { data, content } = matter(fileContents);
  
  return {
    slug: realSlug,
    meta: data,
    content,
  };
}

export function getAllProjects() {
  if (!fs.existsSync(contentDirectory)) return [];
  
  const slugs = fs.readdirSync(contentDirectory);
  const projects = slugs
    .map((slug) => getProjectBySlug(slug))
    .filter((post): post is NonNullable<typeof post> => Boolean(post))
    // Sort projects by date in descending order
    .sort((post1, post2) => ((post1.meta.date > post2.meta.date) ? -1 : 1));
    
  return projects;
}
