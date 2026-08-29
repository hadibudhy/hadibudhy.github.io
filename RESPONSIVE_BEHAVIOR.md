# Responsive behavior

| Width | Navigation | Hero | Projects | Reading behavior |
|---|---|---|---|---|
| `<640px` | Links wrap into the existing compact menu | Circular identity image and text stack naturally | One card per row | Tables scroll locally; paragraphs keep normal word wrapping |
| `640–1023px` | Full navigation fits with compact gutters | Identity row remains horizontal | Two cards per row | Content remains inside the 48rem shell |
| `>=1024px` | Sticky navigation stays centered | Editorial hero keeps a narrow reading measure | Two cards per row with stable gaps | Project detail keeps a controlled prose width |

The implementation uses fluid width, `max-width`, `min-width: 0`, intrinsic images, `aspect-ratio`, wrapping tags, and content-driven heights. No project card depends on a fixed desktop height or a `100vw` child inside a padded container.

## Mobile checks

- Cards stack media before category, title, description, metrics, and CTA.
- Long titles use normal word wrapping, not character-level breaking.
- Media stays within its card and preserves its ratio.
- Buttons expand to the available width only where that improves reachability.
- Navigation remains reachable without horizontal scrolling.
