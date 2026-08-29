# Portfolio design system

This system adapts the observed structure of `renlenon.vercel.app` to Hadi Budhy's own content. It uses a compact editorial portfolio layout: identity first, a short plain-language positioning statement, then selected work and supporting detail.

## Tokens

| Token | Value | Use |
|---|---|---|
| Background | `#fafafa` | Page canvas |
| Surface | `#ffffff` | Cards and readable content blocks |
| Foreground | `#171717` | Headings and primary actions |
| Muted text | `#737373` | Explanations and metadata |
| Border | `#e5e7eb` | Dividers and card boundaries |
| Accent | `#171717` | Links, buttons, and focus |
| Small radius | `0.5rem` | Controls |
| Card radius | `0.75rem` | Surfaces |

Typography uses the system sans stack: `system-ui`, `-apple-system`, and `Segoe UI`. Headings are light or regular with tight tracking. Body text is 16–18px with 1.75–2 line-height. Labels use 11px uppercase text with expanded tracking.

## Layout

- Primary shell: `max-width: 48rem` (`max-w-3xl`), centered.
- Gutters: 1rem on narrow screens, 1.5rem from 640px upward.
- Sections use 3.5–5rem vertical padding, reduced on phones.
- Project grids are one column below 640px and two columns from 640px upward.
- Grid children use `min-width: 0`; media uses intrinsic width limits and `object-fit`.
- Project detail pages use the same shell so the reading width does not jump between routes.

## Components

- `Navbar`: sticky, translucent, compact, keyboard-focusable navigation.
- `ProjectCard`: image, category, title, plain-language summary, business question, decision signal, and a clear text CTA.
- `Button`: solid primary action, bordered secondary action, and visible focus ring.
- `Badge`: small metadata labels that wrap instead of forcing horizontal overflow.
- `Footer`: short identity statement, external links, privacy, and terms.

## Motion and states

Motion is limited to color, border, and small text-link feedback. Loading and error routes use skeleton blocks and recovery actions. No animation is required for understanding a chart or case study.

## Accessibility rules

- Every image has meaningful alternative text or an intentionally empty alt when decorative.
- Links and buttons retain visible keyboard focus.
- Text stays readable at narrow widths and does not rely on hover.
- Tables scroll inside their own container rather than widening the page.
- Content grows with text; fixed card heights are avoided.
