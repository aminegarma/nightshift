# Contrast measured in the rendered mocks

Measured 2026-11-03 on `key-b3-approval.html`, `key-a1-fleet-overview.html` and `key-b3m-manual-repair.html` in this folder, light and dark. These are measurements of the mocks as rendered, not a WCAG compliance claim.

**Result: 0 pairs below threshold** out of 2244 measured pairs (text ≥4.5:1, large text ≥3:1, UI boundaries, term underlines and focus rings ≥3:1).

## Lowest pairs per screen and mode

| Screen | Mode | Lowest text pair (ratio · fg / bg · sample) | Lowest non-text pair (ratio · fg / bg · what) | Lowest focus ring |
|---|---|---|---|---|
| B3 approval | Light | 5.62:1 · `#146C3A` / `#E1F3E8` · "Verified facts" (14px/700) | 6.33:1 · `#2B59C3` / `#FFFFFF` · Approve this repair (fill vs surroundings (no border)) | 6.05:1 · `#2B59C3` / `#F9FAFB` · "‹ Back" |
| B3 approval | Dark | 6.02:1 · `#A3A9B3` / `#15301F` · "Updated 40 s ago" (14px/400) | 5.9:1 · `#6E9BF5` / `#1E2126` · Approve this repair (fill vs surroundings (no border)) | 6.68:1 · `#8AB0FF` / `#262A30` · "‹ Back" |
| A1 fleet overview | Light | 5.62:1 · `#146C3A` / `#E1F3E8` · "Resolved" (12px/600) | 6.87:1 · `#4B5563` / `#F3F4F6` · Pause live updates (1px solid border) | 5.45:1 · `#2B59C3` / `#EDEEEF` · "Out of date: last data 0" |
| A1 fleet overview | Dark | 5.7:1 · `#A3A9B3` / `#2B2F34` · "Unknown" (13px/400) | 6.1:1 · `#A3A9B3` / `#262A30` · browser-frame dots, scaffolding (1px solid border; lowest product pair: the same `#A3A9B3` tile outline on `#1E2126`, 6.83:1) | 6.24:1 · `#8AB0FF` / `#2B2F34` · "Out of date: last data 0" |
| B3-M manual repair | Light | 6.33:1 · `#FFFFFF` / `#2B59C3` · "Approve this manual repair" (17px/600) | 6.33:1 · `#2B59C3` / `#FFFFFF` · Approve this manual repair (fill vs surroundings (no border)) | 6.05:1 · `#2B59C3` / `#F9FAFB` · "‹ Back" |
| B3-M manual repair | Dark | 6.73:1 · `#0E1420` / `#6E9BF5` · "Approve this manual repair" (17px/600) | 5.9:1 · `#6E9BF5` / `#1E2126` · Approve this manual repair (fill vs surroundings (no border)) | 6.68:1 · `#8AB0FF` / `#262A30` · "‹ Back" |

## Pairs below threshold

None. Every visible text pair, control or tile boundary, term underline and focus ring measured at or above its threshold, in both modes and with the collapsible sections both closed and open.

## Hatched backgrounds (each stripe tested separately)

| Screen | Mode | fg / stripe | Ratio | Where |
|---|---|---|---|---|
| A1 fleet overview | Light | `#444B55` / `#ECEDEF` (text) | 7.52:1 | hatch base stripe: "Out of date (02:10 CET)" chip and "?" tiles (same pair as the neutral "Alert-only" label) |
| A1 fleet overview | Light | `#111827` / `#FFFFFF` (text) | 17.74:1 | "Out of date: last data 02:10 C" |
| A1 fleet overview | Light | `#111827` / `#EDEEEF` (text) | 15.27:1 | "Out of date: last data 02:10 C" |
| A1 fleet overview | Light | `#4B5563` / `#FFFFFF` (text) | 7.56:1 | "Unknown" |
| A1 fleet overview | Light | `#4B5563` / `#EDEEEF` (text) | 6.51:1 | "Unknown" |
| A1 fleet overview | Light | `#444B55` / `#D4D6D9` (text) | 6.05:1 | "Out of date (02:10 CET)" |
| A1 fleet overview | Dark | `#BCC2CB` / `#2A2D33` (text) | 7.7:1 | hatch base stripe: "Out of date (02:10 CET)" chip and "?" tiles (same pair as the neutral "Alert-only" label) |
| A1 fleet overview | Dark | `#E8EAED` / `#1E2126` (text) | 13.39:1 | "Out of date: last data 02:10 C" |
| A1 fleet overview | Dark | `#E8EAED` / `#2B2F34` (text) | 11.18:1 | "Out of date: last data 02:10 C" |
| A1 fleet overview | Dark | `#A3A9B3` / `#1E2126` (text) | 6.83:1 | "Unknown" |
| A1 fleet overview | Dark | `#A3A9B3` / `#2B2F34` (text) | 5.7:1 | "Unknown" |
| A1 fleet overview | Dark | `#BCC2CB` / `#383B41` (text) | 6.27:1 | "Out of date (02:10 CET)" |
| A1 fleet overview | Light | `#2B59C3` / `#FFFFFF` (focus-ring) | 6.33:1 | "Out of date: last data 02:10 C" |
| A1 fleet overview | Light | `#2B59C3` / `#EDEEEF` (focus-ring) | 5.45:1 | "Out of date: last data 02:10 C" |
| A1 fleet overview | Dark | `#8AB0FF` / `#1E2126` (focus-ring) | 7.48:1 | "Out of date: last data 02:10 C" |
| A1 fleet overview | Dark | `#8AB0FF` / `#2B2F34` (focus-ring) | 6.24:1 | "Out of date: last data 02:10 C" |

Not exercised by these mocks: `text-secondary` directly on the stale hatch (DESIGN.md computes 5.2:1 light and 4.75:1 dark on the stripe). No screen here puts `text-secondary` text on a hatched chip, tile or panel. The stale row hatch is a different pair, measured above. The 4.75:1 dark value is still a computed figure, not a measurement.

## Method

- **Renderer:** headless Chromium (Playwright `chromium_headless_shell-1228`, Linux, system fonts), viewport 1800 px wide and as tall as the page, so every element is on screen.
- **Text:** every non-empty text node whose element is visible (`checkVisibility`) and not covered. Covered means `elementFromPoint` at the text's first line box does not hit that element, which is how text under the confirmation sheet or clipped by the phone frame is excluded. Foreground is the computed `color`. Background is the first opaque `background-color` up the ancestor chain, with semi-transparent layers composited. For a `repeating-linear-gradient` hatch, each stripe colour is tested as its own background. "Large" means at least 24 px, or at least 18.66 px at weight 700 or more (needs 3:1); everything else needs 4.5:1.
- **Two passes:** once as published, with Evidence and Recovery plan closed, and once with every `<details>` opened, so the facts and explanation blocks are included.
- **Non-text (WCAG 1.4.11, ≥3:1):**
  - **Controls and tiles:** for buttons, summary tiles, section toggles, health-grid tiles and legend swatches, the border colour against the background just outside the element. A control without a border (the primary button) is measured by its fill against its surroundings.
  - **Term underlines:** the dotted underline colour against its background.
- **Focus rings:** real keyboard focus (Tab through every focusable element in both modes). The computed `outline-color` is measured against the parent's background, since the ring is drawn outside the element with a 2 px offset; on a hatched parent, both stripes are tested.
- **Contrast formula:** WCAG 2.x relative luminance, `(L1 + 0.05) / (L2 + 0.05)`, from rendered sRGB values. Anti-aliasing and subpixel rendering are ignored.
- **Not measured:** hover and pressed states (`surface-raised`; not rendered in the mocks), text at 200% zoom, the gallery header and mode labels around the frames (scaffolding, though they also pass), Windows and macOS font rendering, and real devices.
