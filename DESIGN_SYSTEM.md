# Portfolio design system

## Direction

An editorial data portfolio: clear type, restrained forest-green accents, and real charts and workflow diagrams. The evidence carries the visual interest. Layout stays compact and readable on phones.

## Tokens

| Token | Value | Use |
|---|---|---|
| Background | `#f6f8f4` | Page canvas |
| Surface | `#fffefa` | Cards and readable content blocks |
| Foreground | `#17251e` | Headings and primary text |
| Muted text | `#52635a` | Explanations and metadata |
| Border | `#d8e2da` | Dividers and card boundaries |
| Accent | `#155b49` | Links, buttons, and focus |
| Accent wash | `#e5efe8` | Small evidence and process panels |
| Card radius | `0.75rem` | Cards and image frames |
| Control radius | `0.375rem` | Buttons, menus, and inputs |

Typography uses self-hosted IBM Plex Sans. Body copy is 16px with 1.5–1.75 line-height. Headings use medium or semibold weight, balanced wrapping, and tight tracking. Labels stay at 14px or larger.

## Layout

- The homepage and project index use a centered shell up to `72rem` wide.
- Case studies stay at a centered reading width of `48rem`.
- Gutters are 1rem on narrow screens and 1.5rem from 640px upward.
- Project grids use one column on phones and two or three columns on larger screens.
- Content height follows the text. Nothing is clipped to force a screen-sized section.
- Charts have a readable text takeaway and a full-chart link on narrow screens.

## Components

- `Navbar`: sticky, opaque, compact, and keyboard-focusable.
- `ProjectCard`: evidence image, work area, title, short summary, finding, and text link.
- `Button`: forest-green primary action, bordered secondary action, and visible focus ring.
- Diagrams: real project and portfolio workflows with accessible names and descriptions.
- `Footer`: short identity statement, external links, privacy, and terms.

## Motion and states

Motion is limited to a small card lift, image zoom, and link or button feedback. Reduced-motion preferences remove movement. Focus remains visible, and content does not rely on hover.
