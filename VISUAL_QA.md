# Visual QA matrix

The portfolio visual gate was re-run against the local Next.js site after adding three evidence-backed visuals to every published project. This matrix records the current render checks; it is not a claim of pixel identity against an external reference.

| Route | Viewport set | Status | Main differences / next check |
|---|---|---|---|
| `/` | 375, 430, 768, 1024, 1280, 1440, 1920 | Build/lint pass | Homepage layout remains covered by the existing visual matrix |
| `/projects` | 375, 430, 768, 1024, 1280, 1440, 1920 | Build/lint pass | Project index renders published content from the same metadata loader |
| All 20 published project details | Local browser render at default and 360px viewport | Pass | Every page has 3 figures, non-empty alt text, loaded assets after lazy-load scroll, and no horizontal overflow |
| Representative detail: Census expansion | Desktop and 360px viewport | Pass | Three visual roles render in sequence; mobile tables remain contained and page width stays within viewport |

The local build and lint checks plus the connected-browser DOM audit are the current automated evidence. The audit checked all 20 published detail routes for figure count, image alt text, image loading, and document overflow. The three visual roles are context, main finding/evidence boundary, and decision/control design; conceptual diagrams are explicitly labeled in the image footer and adjacent page copy.
