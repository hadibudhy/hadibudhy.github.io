import type { MetadataRoute } from "next";
import { getAllProjects } from "@/lib/mdx";

export const dynamic = "force-static";

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = "https://hadibudhy.github.io";
  const routes = ["", "/about", "/projects", "/resume", "/privacy", "/terms"].map((path) => ({
    url: `${baseUrl}${path}`,
    lastModified: new Date("2026-08-30T00:00:00Z"),
  }));
  const projects = getAllProjects().map((project) => ({
    url: `${baseUrl}/projects/${project.slug}`,
    lastModified: project.meta.date,
  }));

  return [...routes, ...projects];
}
