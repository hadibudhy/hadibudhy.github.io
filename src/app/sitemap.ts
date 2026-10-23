import type { MetadataRoute } from "next";
import { getAllProjects } from "@/lib/mdx";

export const dynamic = "force-static";

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = "https://hadibudhy.github.io";
  const routes = ["", "/about", "/projects", "/privacy", "/terms"].map((path) => ({
    url: `${baseUrl}${path}`,
  }));
  const projects = getAllProjects().map((project) => ({
    url: `${baseUrl}/projects/${project.slug}`,
  }));

  return [...routes, ...projects];
}
