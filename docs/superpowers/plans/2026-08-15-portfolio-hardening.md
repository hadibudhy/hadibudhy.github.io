# Portfolio Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix the portfolio’s confirmed broken CTA, lint/type issues, static-rendering behavior, metadata, image handling, stale links, and deployment documentation without changing its static Next.js architecture.

**Architecture:** Keep local Markdown as the source of truth and normalize its front matter in `src/lib/mdx.ts`. Keep pages server-rendered and make project cards progressively enhanced. Add file-based metadata for static SEO and retain the legacy Jekyll tree unchanged.

**Tech Stack:** Next.js 16 App Router, React 19, TypeScript, Tailwind CSS 4, gray-matter, next-mdx-remote, Next metadata file conventions.

## Global Constraints

- Do not fabricate a resume PDF; replace the broken Resume link with the existing email CTA until a real PDF is supplied.
- Do not delete `legacy_jekyll/` or the untracked `runs.json`.
- Do not add dependencies.
- Preserve static export deployment to GitHub Pages.

### Task 1: Normalize project content metadata

**Files:** Modify `src/lib/mdx.ts`, `src/components/ui/ProjectCard.tsx`, `src/app/page.tsx`, `src/app/projects/page.tsx`, `src/app/projects/[slug]/page.tsx`.

- Define typed project metadata.
- Normalize scalar/array categories and tags.
- Validate dates before sorting and formatting.
- Remove `any` casts.

### Task 2: Fix progressive rendering, image accessibility, and navigation

**Files:** Modify `src/components/ui/ProjectCard.tsx`, `src/app/projects/[slug]/page.tsx`, `src/components/layout/Navbar.tsx`, `src/app/about/page.tsx`, `src/components/layout/Footer.tsx`.

- Remove client-only card animation so static HTML remains visible.
- Require MDX image alt text and retain responsive native image behavior.
- Replace the broken Resume link with email.
- Remove unused imports and add navigation/focus polish.

### Task 3: Add static SEO metadata

**Files:** Modify `src/app/layout.tsx`; create `src/app/robots.ts`, `src/app/sitemap.ts`.

- Add canonical URL, Open Graph, Twitter card, and JSON-LD person metadata.
- Generate static sitemap and robots output for the deployed site.

### Task 4: Repair content links and project documentation

**Files:** Modify the three case-study Markdown files with stale repository links, `.github/workflows/nextjs.yml`, `README.md`.

- Point analysis links at the current `legacy_jekyll/scripts` paths.
- Use reproducible CI installation.
- Document the actual Next.js workflow and resume behavior.

### Task 5: Verify and publish

- Run source lint, TypeScript, build, and static output/link checks.
- Confirm only intended files changed.
- Commit the feature branch and push it to `origin`.
