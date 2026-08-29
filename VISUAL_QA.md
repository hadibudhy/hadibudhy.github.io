# Visual QA matrix

The reference audit was completed over HTTP. A browser renderer was unavailable for screenshot capture, so the following matrix records the required rerun rather than claiming pixel-level pass status.

| Route | Viewport set | Status | Main differences / next check |
|---|---|---|---|
| `/` | 375, 430, 768, 1024, 1280, 1440, 1920 | Pending browser runtime | Compare hero proportions, featured card rhythm, and footer position |
| `/projects` | 375, 430, 768, 1024, 1280, 1440, 1920 | Pending browser runtime | Compare compact shell, card grid, and text wrapping |
| Representative project detail | 375, 430, 768, 1024, 1280, 1440, 1920 | Pending browser runtime | Compare prose width, tables, chart sizing, and navigation |

The local build and lint checks are the current automated evidence. Screenshot, hover, menu, console, and overflow checks require a connected browser.
