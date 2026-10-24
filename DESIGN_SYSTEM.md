# Portfolio design system

This system applies the "Buletin" digest design (Blog Plan 3, selected 2026-10-24) to Hadi Budhy's own content, with the site's original copywriting unchanged. It uses a wide digest shell: identity first, a short plain-language positioning statement, then selected work as dated digest rows with chart thumbnails, and supporting detail in a sidebar.

## Tokens

| Token | Value | Use |
|---|---|---|
| Background | `#f4f4f0` | Page canvas |
| Surface | `#ffffff` | Cards and readable content blocks |
| Foreground | `#181914` | Headings and primary actions |
| Muted text | `#62655c` | Explanations and metadata |
| Border | `#dcdcd4` | Dividers and card boundaries |
| Accent | `#1e4d3b` | Links, buttons, labels, and focus |
| Small radius | `3px` | Controls |
| Card radius | `3px` | Surfaces |

Typography uses self-hosted IBM Plex Sans for text and IBM Plex Mono for labels, dates, and metadata (`public/fonts/`, loaded with `@font-face` in `globals.css`). Headings are bold with tight tracking. Body text is 16–18px. Labels use 11px uppercase mono text with expanded tracking.

## Layout

- Primary shell: `max-width: 1060px`, centered, for the header, footer, homepage, and projects index.
- Gutters: 1rem on narrow screens, 1.5rem from 640px upward.
- Homepage below the hero is a digest grid: main column (career arc, selected work) plus a 300px sidebar (toolkit) from 1024px upward; it stacks on smaller screens.
- Featured project cards are horizontal rows: chart thumbnail on the left (190px, 250px from 1024px), content on the right. Completed-analysis cards keep a two-column grid from 640px upward.
- Grid children use `min-width: 0`; media uses intrinsic width limits and `object-fit`.
- Project detail, privacy, and terms pages keep a `max-w-3xl` reading shell so long-form text stays readable.

## Components

- `Navbar`: sticky, compact, keyboard-focusable navigation with a square forest `HB` mark and a 2px foreground bottom rule.
- `ProjectCard`: chart thumbnail, category, title, plain-language summary, business question, decision signal, and a clear text CTA.
- `Button`: solid primary action, bordered secondary action, and visible focus ring; 3px radius.
- `Badge`: small mono metadata labels that wrap instead of forcing horizontal overflow.
- `Footer`: short identity statement, external links, privacy, and terms; 2px foreground top rule.

## Motion and states

Motion is limited to color, border, and small text-link feedback. Loading and error routes use skeleton blocks and recovery actions. No animation is required for understanding a chart or case study.

## Accessibility rules

- Every image has meaningful alternative text or an intentionally empty alt when decorative.
- Links and buttons retain visible keyboard focus.
- Text stays readable at narrow widths and does not rely on hover.
- Tables scroll inside their own container rather than widening the page.
- Content grows with text; fixed card heights are avoided.
