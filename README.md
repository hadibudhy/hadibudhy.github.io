# Hadi Budhy Portfolio

Static Next.js portfolio for Hadi Budhy, built with the App Router, TypeScript, Tailwind CSS, and Markdown case studies.

## Development

Requirements: Node.js 20 or newer.

```bash
npm ci
npm run dev
```

Open http://localhost:3000.

Project case studies live in `src/content/projects/`. Images and other static assets live in `public/`.

## Validation

```bash
npm run lint
npx tsc --noEmit --incremental false
npm run build
```

The production build is a static export written to `out/`.

## Deployment

GitHub Actions deploys `out/` to GitHub Pages when changes are pushed to `master`. See `.github/workflows/nextjs.yml`.

The navigation Contact button uses email; the public site presents the work and experience directly.
