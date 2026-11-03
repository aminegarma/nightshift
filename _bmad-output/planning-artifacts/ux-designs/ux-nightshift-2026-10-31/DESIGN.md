---
name: Nightshift
description: Neutral visual system for Nightshift's two experiences, the dense Orvex console and the calm customer view in the Quornex portal. Graphite Ledger palette, light and dark, mapped onto Quornex's design system later.
status: final
sources:
  - '{planning_artifacts}/prds/prd-nightshift-2026-10-28/prd.md'
  - '{planning_artifacts}/prds/prd-nightshift-2026-10-28/addendum.md'
  - ./.memlog.md
  - ./mockups/color-themes-1.html
  - ./.working/stale-decisions-2026-11-03.md
  - ./.working/open-items-2026-11-03.md
  - ./.working/ia-proposal-v3.md
  - ./wireframes/flow-orvex-console-2026-11-03.excalidraw
  - ./wireframes/flow-customer-view-2026-11-03.excalidraw
created: 2026-10-31
updated: 2026-11-03
colors:
  # Graphite Ledger (v1), light. Every token has a -dark twin below.
  background: '#F3F4F6'
  surface: '#FFFFFF'
  surface-raised: '#F9FAFB'
  border: '#D1D5DB'
  text-primary: '#111827'
  text-secondary: '#4B5563'
  primary: '#2B59C3'
  primary-ink: '#FFFFFF'
  focus-ring: '#2B59C3'
  critical-fill: '#FDE8E8'
  critical-ink: '#9B1C1C'
  critical-line: '#9B1C1C'
  warning-fill: '#FDEBD8'
  warning-ink: '#8A3B0C'
  warning-line: '#8A3B0C'
  info-fill: '#E3ECFB'
  info-ink: '#1E429F'
  info-line: '#1E429F'
  waiting-fill: '#EDE9FB'
  waiting-ink: '#5B32B4'
  waiting-line: '#5B32B4'
  success-fill: '#E1F3E8'
  success-ink: '#146C3A'
  success-line: '#146C3A'
  explanation-fill: '#FCF4CF'
  explanation-ink: '#6B4E00'
  explanation-line: '#6B4E00'
  neutral-fill: '#ECEDEF'
  neutral-ink: '#444B55'
  neutral-line: '#444B55'
  stale-hatch-base: '#ECEDEF'
  stale-hatch-stripe: '#D4D6D9'
  stale-row-base: '#FFFFFF'
  stale-row-stripe: '#EDEEEF'
  # Graphite Ledger (v1), dark.
  background-dark: '#16181C'
  surface-dark: '#1E2126'
  surface-raised-dark: '#262A30'
  border-dark: '#3A3F47'
  text-primary-dark: '#E8EAED'
  text-secondary-dark: '#A3A9B3'
  primary-dark: '#6E9BF5'
  primary-ink-dark: '#0E1420'
  focus-ring-dark: '#8AB0FF'
  critical-fill-dark: '#3D1A1C'
  critical-ink-dark: '#FFA8A8'
  critical-line-dark: '#FFA8A8'
  warning-fill-dark: '#3B2614'
  warning-ink-dark: '#FFC08A'
  warning-line-dark: '#FFC08A'
  info-fill-dark: '#182A47'
  info-ink-dark: '#A9C6FF'
  info-line-dark: '#A9C6FF'
  waiting-fill-dark: '#2A2045'
  waiting-ink-dark: '#CDB8FF'
  waiting-line-dark: '#CDB8FF'
  success-fill-dark: '#15301F'
  success-ink-dark: '#8FE0AE'
  success-line-dark: '#8FE0AE'
  explanation-fill-dark: '#3A3112'
  explanation-ink-dark: '#F2D675'
  explanation-line-dark: '#F2D675'
  neutral-fill-dark: '#2A2D33'
  neutral-ink-dark: '#BCC2CB'
  neutral-line-dark: '#BCC2CB'
  stale-hatch-base-dark: '#2A2D33'
  stale-hatch-stripe-dark: '#383B41'  # was #3E4248; raised text-secondary on it to 4.75:1 (target >= 4.5:1)
  stale-row-base-dark: '#1E2126'
  stale-row-stripe-dark: '#2B2F34'
typography:
  # System stack until Quornex brand fonts are mapped [OPEN: Orvex].
  # Decided: console body ~13px (dense), customer body 16-18px (calm).
  # The rest of the ramp is [ASSUMPTION], taken from the Graphite Ledger sheet render.
  console-body:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 20px
  console-title:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
    fontSize: 16px
    fontWeight: '600'
    lineHeight: '1.3'
  console-column-label:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
    fontSize: 11px
    fontWeight: '700'
    lineHeight: '1.4'
    letterSpacing: 0.03em
  console-chip:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 20px
  console-mono:
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 20px
  customer-body:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.55'
  customer-lead:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
    fontSize: 18px
    fontWeight: '600'
    lineHeight: '1.4'
  customer-title:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
    fontSize: 22px
    fontWeight: '700'
    lineHeight: '1.3'
  customer-action:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
    fontSize: 17px
    fontWeight: '600'
    lineHeight: '1.3'
  customer-chip:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
    fontSize: 15px
    fontWeight: '600'
    lineHeight: '1.35'
  customer-block-title:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
    fontSize: 14px
    fontWeight: '700'
    lineHeight: '1.4'
  customer-meta:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.4'
rounded:
  control: 4px     # --rc: chips, inputs, small controls
  block: 5px       # --rk / 2: verified-facts and explanation blocks [ASSUMPTION]
  button: 8px      # --rk / 1.2 as rendered: customer buttons [ASSUMPTION]
  container: 10px  # --rk: panels, tables, cards
spacing:
  # [ASSUMPTION] 4-based scale; console compact, customer generous.
  '1': 4px
  '2': 8px
  '3': 12px
  '4': 16px
  '5': 20px
  '6': 24px
  '8': 32px
  console-cell-y: 4px
  console-cell-x: 8px
  console-panel-gap: 8px
  customer-gutter: 20px
  customer-section-gap: 16px
  customer-tap-min: 44px
components:
  # Light references shown; in dark mode each colour reference resolves to its -dark twin.
  # Hatch = repeating-linear-gradient(<angle>, <base> 0 <width>, <stripe> <width> <2 x width>).
  chip-critical:
    background: '{colors.critical-fill}'
    foreground: '{colors.critical-ink}'
    border: '1px solid {colors.critical-line}'
    radius: '{rounded.control}'
    typography-console: '{typography.console-chip}'
    typography-customer: '{typography.customer-chip}'
  chip-warning:
    background: '{colors.warning-fill}'
    foreground: '{colors.warning-ink}'
    border: '1px solid {colors.warning-line}'
    radius: '{rounded.control}'
    typography-console: '{typography.console-chip}'
    typography-customer: '{typography.customer-chip}'
  chip-info:
    background: '{colors.info-fill}'
    foreground: '{colors.info-ink}'
    border: '1px solid {colors.info-line}'
    radius: '{rounded.control}'
    typography-console: '{typography.console-chip}'
    typography-customer: '{typography.customer-chip}'
  chip-waiting:
    background: '{colors.waiting-fill}'
    foreground: '{colors.waiting-ink}'
    border: '1px solid {colors.waiting-line}'
    radius: '{rounded.control}'
    typography-console: '{typography.console-chip}'
    typography-customer: '{typography.customer-chip}'
  chip-success:
    background: '{colors.success-fill}'
    foreground: '{colors.success-ink}'
    border: '1px solid {colors.success-line}'
    radius: '{rounded.control}'
    typography-console: '{typography.console-chip}'
    typography-customer: '{typography.customer-chip}'
  chip-neutral:
    background: '{colors.neutral-fill}'
    foreground: '{colors.neutral-ink}'
    border: '1px solid {colors.neutral-line}'
    radius: '{rounded.control}'
    typography-console: '{typography.console-chip}'
    typography-customer: '{typography.customer-chip}'
  chip-stale:
    hatch-base: '{colors.stale-hatch-base}'
    hatch-stripe: '{colors.stale-hatch-stripe}'
    hatch-angle: 135deg
    hatch-stripe-width: 5px
    foreground: '{colors.neutral-ink}'
    border: '1px solid {colors.neutral-line}'
    radius: '{rounded.control}'
    typography-console: '{typography.console-chip}'
    typography-customer: '{typography.customer-chip}'
  severity-chip:
    critical: '{components.chip-critical}'
    warning: '{components.chip-warning}'
    informational: '{components.chip-info}'
  incident-status-chip:
    being-watched: '{components.chip-info}'
    needs-attention: '{components.chip-warning}'
    waiting-for-customer: '{components.chip-waiting}'
    waiting-for-orvex: '{components.chip-waiting}'
    resolved: '{components.chip-success}'
  repair-status-chip:
    waiting-for-approval: '{components.chip-waiting}'
    manual-repair-needed: '{components.chip-waiting}'
    work-in-progress: '{components.chip-info}'
    running: '{components.chip-info}'
    verifying: '{components.chip-info}'
    succeeded: '{components.chip-success}'
    mitigated: '{components.chip-warning}'            # [ASSUMPTION] not green: the fault stays open
    problem-still-there: '{components.chip-critical}' # [ASSUMPTION] reads like Failed
    failed: '{components.chip-critical}'
    rejected: '{components.chip-neutral}'
    blocked: '{components.chip-neutral}'
    cancelled: '{components.chip-neutral}'
    expired: '{components.chip-neutral}'
  freshness-chip:
    out-of-date: '{components.chip-stale}'
  risk-level-chip:
    safe: '{components.chip-success}'
    risky: '{components.chip-warning}'
    dangerous: '{components.chip-critical}'
  verified-facts-block:
    background: '{colors.success-fill}'
    foreground: '{colors.success-ink}'
    accent-border: '4px solid {colors.success-line}'
    radius: '{rounded.block}'
    title-typography: '{typography.customer-block-title}'
  explanation-block:
    background: '{colors.explanation-fill}'
    foreground: '{colors.explanation-ink}'
    accent-border: '4px solid {colors.explanation-line}'
    radius: '{rounded.block}'
    title-typography: '{typography.customer-block-title}'
  button-primary:
    background: '{colors.primary}'
    foreground: '{colors.primary-ink}'
    border: 'none'
    radius: '{rounded.button}'
    typography: '{typography.customer-action}'
    min-height: '{spacing.customer-tap-min}'
    typography-console: '{typography.console-body}'  # console size [ASSUMPTION]
    min-height-console: '{spacing.8}'                # console size [ASSUMPTION]
    focus-width: 3px
    focus-colour: '{colors.focus-ring}'
    focus-offset: 2px
  button-secondary:
    background: 'transparent'
    foreground: '{colors.text-primary}'
    border: '1.5px solid {colors.text-secondary}'
    radius: '{rounded.button}'
    typography: '{typography.customer-action}'
    min-height: '{spacing.customer-tap-min}'
    typography-console: '{typography.console-body}'  # console size [ASSUMPTION]
    min-height-console: '{spacing.8}'                # console size [ASSUMPTION]
    focus-width: 3px
    focus-colour: '{colors.focus-ring}'
    focus-offset: 2px
  link:
    # [ASSUMPTION] text links: underlined, never colour alone.
    foreground: '{colors.text-primary}'
    underline: '1px solid {colors.text-primary}'
    focus-width: 3px
    focus-colour: '{colors.focus-ring}'
    focus-offset: 2px
  confirmation-sheet:
    background: '{colors.surface}'
    foreground: '{colors.text-primary}'
    outline: '1px solid {colors.text-secondary}'
    radius: '{rounded.container}'
    padding: '{spacing.customer-gutter}'
    lead-typography: '{typography.customer-lead}'
    body-typography: '{typography.customer-body}'
    console-typography: '{typography.console-body}'
    confirm: '{components.button-primary}'
    cancel: '{components.button-secondary}'
  what-were-asking-summary:
    background: '{colors.surface-raised}'
    foreground: '{colors.text-primary}'
    border: '1px solid {colors.border}'
    radius: '{rounded.block}'
    padding: '{spacing.4}'
    title-typography: '{typography.customer-block-title}'
    line-typography: '{typography.customer-body}'
  approval-card:
    background: '{colors.surface}'
    foreground: '{colors.text-primary}'
    border: '1px solid {colors.border}'
    radius: '{rounded.container}'
    padding: '{spacing.customer-gutter}'
    lead-typography: '{typography.customer-lead}'
    body-typography: '{typography.customer-body}'
    summary: '{components.what-were-asking-summary}'
    section-toggle-outline: '1.5px solid {colors.text-secondary}'
    term-underline: '1px dotted {colors.text-secondary}'  # [ASSUMPTION] marks a word with a plain explanation
    changed-banner-background: '{colors.warning-fill}'     # [ASSUMPTION]
    changed-banner-foreground: '{colors.warning-ink}'
    changed-banner-border: '1px solid {colors.warning-line}'
  cluster-card:
    background: '{colors.surface}'
    foreground: '{colors.text-primary}'
    outline: '1px solid {colors.text-secondary}'
    radius: '{rounded.container}'
    padding: '{spacing.customer-gutter}'
    impact-typography: '{typography.customer-lead}'
    meta-typography: '{typography.customer-meta}'
    stale-hatch-base: '{colors.stale-hatch-base}'
    stale-hatch-stripe: '{colors.stale-hatch-stripe}'
    stale-foreground: '{colors.neutral-ink}'
    mode-label: '{components.chip-neutral}'
  timeline-entry:
    background: '{colors.surface}'
    divider: '1px solid {colors.border}'
    time-typography-customer: '{typography.customer-meta}'
    time-typography-console: '{typography.console-mono}'
    body-typography-customer: '{typography.customer-body}'
    body-typography-console: '{typography.console-body}'
    status: '{components.repair-status-chip}'
    progress: '{components.progress-steps}'
  attention-queue-row:
    background: '{colors.surface}'
    header-background: '{colors.surface-raised}'
    header-typography: '{typography.console-column-label}'
    header-foreground: '{colors.text-secondary}'
    divider: '1px solid {colors.border}'
    severity-bar-width: 3px
    severity-bar-position: inset-left
    severity-bar-critical: '{colors.critical-line}'
    severity-bar-warning: '{colors.warning-line}'
    severity-bar-informational: '{colors.info-line}'
    cell-padding: '{spacing.console-cell-y} {spacing.console-cell-x}'
    typography: '{typography.console-body}'
    id-typography: '{typography.console-mono}'
    mode-label: '{components.chip-neutral}'
  attention-queue-row-stale:
    hatch-base: '{colors.stale-row-base}'
    hatch-stripe: '{colors.stale-row-stripe}'
    hatch-angle: 135deg
    hatch-stripe-width: 6px
  freshness-line:
    foreground: '{colors.text-secondary}'
    typography-console: '{typography.console-body}'
    typography-customer: '{typography.customer-meta}'
    paused-label: '{components.chip-neutral}'
  stale-panel:
    hatch-base: '{colors.stale-hatch-base}'
    hatch-stripe: '{colors.stale-hatch-stripe}'
    hatch-angle: 135deg
    hatch-stripe-width: 5px
    foreground: '{colors.neutral-ink}'
    border: '1px solid {colors.neutral-line}'
    radius: '{rounded.container}'
  summary-tile:
    background: '{colors.surface}'
    outline: '1px solid {colors.text-secondary}'
    radius: '{rounded.container}'
    critical-background: '{colors.critical-fill}'
    critical-outline: '1px solid {colors.critical-line}'
  health-grid-tile:
    critical: '{components.chip-critical}'
    warning: '{components.chip-warning}'
    no-open-problem-background: '{colors.surface}'
    no-open-problem-outline: '1px solid {colors.text-secondary}'
    fleet-reports-off-background: '{colors.surface}'
    fleet-reports-off-outline: '1px dashed {colors.text-secondary}'  # letter "F" [ASSUMPTION]
    out-of-date: '{components.chip-stale}'                           # letter "?" [ASSUMPTION]
    radius: '{rounded.control}'
  info-card:
    background: '{colors.info-fill}'
    foreground: '{colors.info-ink}'
    border: '1px solid {colors.info-line}'
    radius: '{rounded.container}'
  manual-repair-panel:
    background: '{colors.surface}'
    foreground: '{colors.text-primary}'
    border: '1px solid {colors.text-secondary}'
    radius: '{rounded.container}'
    status: '{components.chip-waiting}'
  check-table:
    background: '{colors.surface}'
    divider: '1px solid {colors.border}'
    pass: '{components.chip-success}'
    fail: '{components.chip-critical}'
    typography: '{typography.console-body}'
  progress-steps:
    current: '{components.repair-status-chip}'
    connector: '{colors.text-secondary}'
    typography-customer: '{typography.customer-body}'
  settings-row:
    background: '{colors.surface}'
    divider: '1px solid {colors.border}'
    control-outline: '1.5px solid {colors.text-secondary}'
    required-label: '{components.chip-neutral}'
    tick-again-badge: '{components.chip-warning}'
---

# Nightshift: Design Spine

> Visual reference for both experiences. Behaviour lives in [EXPERIENCE.md](EXPERIENCE.md). Wireframes, the palette sheet and the key-screen mocks are linked in the sections they illustrate; **the spines win on any conflict with a wireframe or mock.**

## Brand & Style

Nightshift is an operations agent that may change a customer's production at 3 AM. The look has one job: to make it obvious what needs a person, what is verified and what is only an explanation. The register is **Graphite Ledger**: "composed and accountable: a well-kept operations ledger, nothing louder than it needs to be" (Amine). Cool graphite neutrals, white working surfaces, medium-strength tinted status chips, one steady cobalt accent.

Two densities share one palette:

- **Orvex console**: dense and formal. Compact tables, small type, many rows. Inspired by Grafana's monitoring dashboards and Better Stack's formal, professional look.
- **Customer view**: calm. Large type, generous spacing, one thing at a time. Inspired by PagerDuty's incident status, notifications and action history, simplified for a business owner without infrastructure expertise.

These are references for look and feel, not integrations.

**Brand layer.** This file defines neutral Nightshift tokens. Quornex's brand colours and fonts are mapped onto the Quornex portal's design system later **[OPEN: Orvex, O-12]**. No private Orvex brand material is used or stored here. Light and dark are both defined for both experiences; the person or their device chooses.

## Colors

Source: the Graphite Ledger (v1) block in the [palette sheet](mockups/color-themes-1.html) (round 1: five candidate palettes in light and dark), with one change (the dark hatch stripe, below). Ratios are WCAG 2.x, **computed from the token values**. They are design targets: contrast is to be measured in the rendered result, not claimed. Measurements of the rendered key-screen mocks, light and dark, are in the [contrast report](mockups/contrast-measured.md).

Rules that carry the meaning:

- **Colour always repeats a word, never replaces it.** A chip says "Critical"; a tile carries "C" and a legend; a hatched panel says "No data since 02:10 CET".
- **Green means verified, never assumed.** A panel past its freshness threshold turns grey and hatched; it never stays green.
- **Yellow marks "explanation, not verified fact"**, whoever wrote it. The block keeps its colour when the label says "written from a template".
- **Blue is shared** by Informational / Running / Verifying and the primary action. The primary button is a solid `primary` fill; status chips are tinted fills with a border, so the two never read alike.
- Severity, incident status, repair status, risk level and freshness are separate fields, each with its own chip (see Components).

**Neutrals.**

| Token | Light | Dark | Role | Contrast (computed) |
|---|---|---|---|---|
| `background` | `#F3F4F6` | `#16181C` | Page behind panels | text-primary 16.1:1 / 14.7:1 |
| `surface` | `#FFFFFF` | `#1E2126` | Working surfaces: panels, cards, table rows | text-primary 17.7:1 / 13.4:1 |
| `surface-raised` | `#F9FAFB` | `#262A30` | Table headers, panel bars, the "What we're asking" summary | text-primary 17.0:1 / 12.0:1 |
| `border` | `#D1D5DB` | `#3A3F47` | **Dividers only** | 1.47:1 / 1.52:1 vs surface |
| `text-primary` | `#111827` | `#E8EAED` | Body text, link text | 17.7:1 / 13.4:1 on surface |
| `text-secondary` | `#4B5563` | `#A3A9B3` | Freshness lines, labels, control outlines | 7.6:1 / 6.8:1 on surface (min 6.9 / 6.1 on `background` or `surface-raised`) |
| `primary` | `#2B59C3` | `#6E9BF5` | Primary action only ("Approve this repair") | label `primary-ink` 6.3:1 / 6.7:1 |
| `primary-ink` | `#FFFFFF` | `#0E1420` | Label on primary | |
| `focus-ring` | `#2B59C3` | `#8AB0FF` | Keyboard focus | 5.7:1 / 8.2:1 vs background (target ≥3:1) |

`border` is faint by design. It separates rows and panels; it is **never a control's only outline**. Controls and anything clickable (buttons, checkboxes, cluster cards, summary tiles, tiles with no status) take a `text-secondary` outline instead.

**Status roles.** The wireframe colour key is the semantic palette. The meaning of each hue is fixed; only the shades differed between the rendered palette options. Each role is a fill / ink / line triple; ink and line share a value.

| Role | Light fill / ink | Dark fill / ink | Ink on fill | Means (always with the word) |
|---|---|---|---|---|
| `critical` (red) | `#FDE8E8` / `#9B1C1C` | `#3D1A1C` / `#FFA8A8` | 6.9 / 8.4 | Critical · Failed · Problem still there · Dangerous |
| `warning` (orange) | `#FDEBD8` / `#8A3B0C` | `#3B2614` / `#FFC08A` | 6.7 / 8.9 | Warning · Needs attention · Mitigated · Risky; "This request has changed" banner |
| `info` (blue) | `#E3ECFB` / `#1E429F` | `#182A47` / `#A9C6FF` | 7.6 / 8.4 | Informational · Work in progress · Running · Verifying · Being watched; Orvex-only information card |
| `waiting` (violet) | `#EDE9FB` / `#5B32B4` | `#2A2045` / `#CDB8FF` | 6.9 / 8.6 | Waiting for a person: Waiting for approval · Waiting for customer · Waiting for Orvex · Manual repair needed |
| `success` (green) | `#E1F3E8` / `#146C3A` | `#15301F` / `#8FE0AE` | 5.6 / 9.1 | Succeeded · Resolved · Safe; the **Verified facts** block |
| `explanation` (yellow) | `#FCF4CF` / `#6B4E00` | `#3A3112` / `#F2D675` | 7.0 / 9.0 | **Nightshift's explanation**, whether written by AI or from a template |
| `neutral` (grey) | `#ECEDEF` / `#444B55` | `#2A2D33` / `#BCC2CB` | 7.5 / 7.7 | Rejected · Blocked · Cancelled · Expired; "Required" label; "Alert-only" mode label; "Live updates paused" |
| stale hatch | `#ECEDEF` / `#D4D6D9` stripes | `#2A2D33` / **`#383B41`** stripes | neutral-ink 6.1 / 6.3; text-secondary 5.2 / 4.75 (on the stripe) | No data / out-of-date data, always labelled ("No data since 02:10 CET") |
| stale row hatch | `#FFFFFF` / `#EDEEEF` | `#1E2126` / `#2B2F34` | text-secondary 6.5 / 5.7 | Out-of-date row in a console table |

**Dark stale-hatch stripe.** `stale-hatch-stripe-dark` is `#383B41` (was `#3E4248`, 4.28:1), so `text-secondary` on it reaches **4.75:1 (target ≥4.5:1)** and `neutral-ink` 6.3:1. The stripe still differs from its base by 1.23:1, the same as the light hatch (1.24:1). To be measured in the rendered result.

**`text-secondary` on tinted fills** (freshness lines inside blocks, cards and tiles), computed light / dark: critical 6.4 / 6.5 · warning 6.5 / 6.0 · info 6.4 / 6.1 · waiting 6.4 / 6.4 · success 6.6 / 6.0 · explanation 6.8 / 5.5 · neutral 6.5 / 5.8.

The `[ASSUMPTION]` chip colours for Work in progress (info), Mitigated (warning) and Problem still there (critical) follow the key: Work in progress reads like Running; a workaround leaves the fault open, so it is not green; a problem still there reads like Failed.

## Typography

System font stack (`system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif`) and a system monospace stack for cluster and customer IDs in the console. Brand fonts are mapped later **[OPEN: Orvex, O-12]**.

| Role | Size / weight | Use |
|---|---|---|
| `console-body` | 13px / 400, 20px line | **Decided density:** table cells, panel text, console buttons |
| `console-column-label` | 11px / 700, uppercase, +0.03em | Table headers [ASSUMPTION] |
| `console-chip` | 12px / 600 | Chips in the console [ASSUMPTION] |
| `console-mono` | 12px / 400 | Cluster and customer IDs (`shop-eu-1`, `Customer C-0142`), console timeline times [ASSUMPTION] |
| `console-title` | 16px / 600 | Screen and panel titles [ASSUMPTION] |
| `customer-body` | 16px / 400, 1.55 | **Decided density:** customer body text |
| `customer-lead` | 18px / 600, 1.4 | **Decided density:** the one-sentence problem at the top of B2, B3, B3-M; the impact line on a cluster card |
| `customer-action` | 17px / 600 | Button labels, action names [ASSUMPTION] |
| `customer-chip` | 15px / 600 | Chips in the customer view [ASSUMPTION] |
| `customer-block-title` | 14px / 700 | "Verified facts", "Nightshift's explanation (written by AI)", "What we're asking" [ASSUMPTION] |
| `customer-meta` | 14px / 400 | Freshness line, "Asked 02:13 CET", timeline times [ASSUMPTION] |
| `customer-title` | 22px / 700 | Screen titles ("Good morning, Samira.") [ASSUMPTION] |

The [ASSUMPTION] sizes are those rendered in the Graphite Ledger sheet; the console 13px body and the customer 16–18px range (body and lead) were decided. No all-caps outside console column labels.

## Layout & Spacing

Spacing scale [ASSUMPTION]: 4 / 8 / 12 / 16 / 20 / 24 / 32 px.

- **Console (dense).** Desktop, wide screens. Table cells `{spacing.console-cell-y}` × `{spacing.console-cell-x}`; panels `{spacing.console-panel-gap}` apart. Many rows on screen at once; tables scroll horizontally rather than wrap columns. Fleet overview order, top to bottom: summary tiles, attention queue, cluster health grid. Problem detail puts Verified facts and Nightshift's explanation side by side. See the [console wireframe](wireframes/flow-orvex-console-2026-11-03.excalidraw) (frame A1) and the [A1 fleet overview mock](mockups/key-a1-fleet-overview.html) (the console home at 1440 px, light and dark).
- **Customer (calm).** One column on a phone, side gutter `{spacing.customer-gutter}`, `{spacing.customer-section-gap}` between sections, one thing at a time. The approval screens are a single column: the "What we're asking" summary first, then the sections in the fixed order EXPERIENCE.md sets for B3 and B3-M, with full-width buttons at the end. Desktop shows the same content in a wider column; settings are desktop-first. Spacing values are [ASSUMPTION]; generous-versus-compact is decided. See the [customer wireframe](wireframes/flow-customer-view-2026-11-03.excalidraw) (frames B3, B3-M, B6 and B6b; the summary and collapsible sections are newer than the wireframe), the [B3 approval mock](mockups/key-b3-approval.html) (B3 on a phone, request open and after Approve) and the [B3-M manual repair mock](mockups/key-b3m-manual-repair.html) (B3-M on a phone, request open and after Approve).

## Elevation & Depth

[ASSUMPTION] No shadows. Depth comes from tone only: `background` behind, `surface` for working panels, `surface-raised` for table headers, panel bars and the "What we're asking" summary, plus 1px `border` dividers. This matches the Graphite Ledger render, which uses none. The confirmation sheet separates from the page with a `text-secondary` outline, not a shadow. Status never uses elevation.

## Shapes

Two radii come from the palette sheet: `{rounded.control}` 4px (`--rc`) for chips, inputs and small controls; `{rounded.container}` 10px (`--rk`) for panels, tables, cards and the confirmation sheet. Two derived radii appear in the render: `{rounded.block}` 5px for the facts, explanation and "What we're asking" blocks and `{rounded.button}` 8px for buttons [ASSUMPTION]. No pills.

## Components

Dark mode: every colour reference in a component resolves to its `-dark` twin (for example `{colors.critical-fill}` → `{colors.critical-fill-dark}`). Hatches are built from their `hatch-*` keys as a 135° repeating gradient.

### Status and evidence

- **Status chips** (`chip-critical` … `chip-neutral`, `chip-stale`). Tinted fill, ink text, line border, `{rounded.control}`, console or customer chip type. Always contain the word. Five families map onto them, never merged into one field:
  - **Severity chip**: Critical (critical) · Warning (warning) · Informational (info). Customer label: "Severity: Warning".
  - **Incident status chip**: Being watched (info) · Needs attention (warning) · Waiting for customer (waiting) · Waiting for Orvex (waiting) · Resolved (success). Customer label: "Status: Waiting for customer".
  - **Repair status chip**: Waiting for approval (waiting) · Manual repair needed (waiting) · Work in progress (info) · Running (info) · Verifying (info) · Succeeded (success) · Mitigated (warning) · Problem still there (critical) · Failed (critical) · Rejected / Blocked / Cancelled / Expired (neutral). Customer label: "Repair status: Running".
  - **Risk level chip**: Safe (success) · Risky (warning) · Dangerous (critical).
  - **Freshness chip**: "Out of date (02:10 CET)" in the stale hatch. Freshness is not a repair status.
- **Verified facts block.** Success fill and ink, accent border in `success-line`, `{rounded.block}`. Title "Verified facts" with the subtitle "from Nightshift's rule-based checks" (customer) or "(rule-based checks)" (console). Bulleted facts; freshness line at the end.
- **Explanation block.** Same anatomy in the explanation role. Title "Nightshift's explanation (written by AI)" or "(written from a template)". Never adjoins the facts block without a gap: the two are always separate, labelled blocks.
- **What Nightshift cannot see** (A2, B2) is neither fact nor explanation: plain `surface`, no status colour, a plain heading.

### Actions and focus

- **Primary button.** Solid `{colors.primary}`, `{colors.primary-ink}` label. Customer size: full width on phone, at least `{spacing.customer-tap-min}` high [ASSUMPTION]. Console size: console body type, at least `{spacing.8}` high [ASSUMPTION]. One per decision: "Approve this repair", "Approve this manual repair", "Give Orvex technical approval", "Approve on the customer's behalf (delegated)", "Start now", "I've done it: check now", "Accept this change", "Approve rollback for these 288 clusters" and the confirm button in a confirmation sheet.
- **Secondary button.** Transparent, `text-primary` label, `text-secondary` outline; same two sizes. "Reject", "Withdraw my approval", "Undo reject", "Cancel" (in a confirmation sheet), "Review the proposed repair", "Review approval →", "See full activity", "Read what changed", "Back to my clusters", "Dispute", "Revoke delegation", "Pause live updates" / "Resume live updates". Reject is not red: rejecting is a normal, safe choice.
- **Link** [ASSUMPTION]. `text-primary`, always underlined, focus ring as buttons. For navigation inside text: "Ticked in your settings on 12 Oct", "Read the policy", "Data leaving your cluster and management policy ›". "Open in Quornex portal to review" is the notification's own link or button.
- **Focus.** 3px `{colors.focus-ring}` outline, 2px offset, on every interactive element.
- **Interactive states** [ASSUMPTION]. Hover and pressed: the row, card or tile takes `surface-raised`. Selected (A1 group selector, a selected row): a 3px `primary` left bar plus the selected word or state, never colour alone. Read-only settings (not an administrator) show the current value as text in place of the control, with the sentence from EXPERIENCE.md › Surface states (Not an administrator).

### Decision surfaces

- **Confirmation sheet** (B3, B3-M, A3, A3-M, A4, B6b). On a phone, a sheet over the lower part of the screen; on desktop, a small dialog. `surface`, `text-secondary` outline, `{rounded.container}`. A `customer-lead` sentence restates the decision ("Approve the restart of checkout-api on shop-eu-1? Checkout may be unavailable for 30–60 seconds."), then the confirm button (primary) and **Cancel** (secondary). The fleet version restates the counts. Console screens use console type.
- **"What we're asking" summary** (top of B3 and B3-M). `surface-raised` block, `{rounded.block}`, title "What we're asking" in `customer-block-title`, then exactly three lines in `customer-body`: the problem, the repair, what it means for you.
- **Approval card** (B3, B3-M). `surface`, 1px `border`, `{rounded.container}`, `{spacing.customer-gutter}` padding. Header chips (Severity, Repair status), then the "What we're asking" summary, then the numbered sections with plain headings, then the two buttons. Evidence and Recovery plan are collapsible: a heading row with a `text-secondary`-outlined toggle and a one-line summary while closed. A technical word with a plain explanation carries a dotted `text-secondary` underline [ASSUMPTION]; a tap opens the explanation in place, below the line. When the request has changed or is no longer needed, a banner in the warning role sits at the top, in words. B1's "Needs your decision" card is the compact version: problem sentence, severity chip and "Asked 02:13 CET"; the whole card is the tap target.
- **Manual-repair panel** (A3-M, B3-M). Plain `surface` with a `text-secondary` outline: it is neither a fact nor an AI explanation. Numbered steps, captioned "From the repair catalogue, not written by AI". Repair status chip above it ("Manual repair needed", then "Work in progress").
- **Check table** (A3 safety preconditions, A3-M pre-run check, A4 per-cluster table with an added repair-status column). Check and result; results as success "Pass" or critical "Fail: another repair is running" chips.

### Cards, rows and tiles

- **Cluster card** (B1, one per cluster). `surface`, `text-secondary` outline (the whole card opens B2), `{rounded.container}`, `{spacing.customer-gutter}` padding. Top line: cluster name and the severity and status chips when a problem is open. Then the impact line in `customer-lead` ("Checkout works normally"), then the freshness line. Out of date: the stale hatch with `neutral-ink` text, and the impact line becomes "Out of date: last data 02:10 CET"; no healthy words remain. Alert-only: a neutral "Alert-only" label beside the name.
- **Info card** (B1). Info fill and line: "For your information · shop-us-1 · Orvex is repairing a platform component. No effect on your service expected. No action needed." No buttons.
- **Attention-queue row** (A1). Dense table row; the "Customer impact" cell is semibold with a severity bar in the severity's line colour. IDs in `console-mono`. An "Alert-only" neutral label sits in the Customer cell when the customer is in alert-only mode. An out-of-date row takes the stale row hatch, "Out of date: last data 02:10 CET" in place of its impact and a freshness chip in the Updated column.
- **Summary tile** (A1 top strip). Count, label and one sub-line ("Oldest wait: 12 min"), `text-secondary` outline because it is clickable. The Critical problems tile takes the critical fill and line.
- **Health-grid tile** (A1). One small square per cluster, in groups of 100, with a legend beside the grid: critical fill with "C"; warning fill with "W"; plain `surface` with a `text-secondary` outline for "No open problem" (no green); dashed `text-secondary` outline with "F" for "Fleet reports not permitted" [ASSUMPTION]; stale hatch with "?" for "No data / stale" [ASSUMPTION].
- **Timeline entry** (B4, A2 timeline, A5 full record). One row per event or repair: time with zone (`customer-meta`, or `console-mono` in the console), a sentence in `customer-body` or `console-body`, the repair status chip and, for a repair, its progress steps and "Who permitted it" line. Entries are separated by `border` dividers.
- **Progress steps** (B3 after Approve, B4, A5, A4 wave progress). Repair-status words joined by arrows, current step as its chip: "Waiting for approval → Running → Verifying → Succeeded". Notes sit beside Failed ("Failed — did not work, undone"). A4 wave labels such as "Waiting for later waves" are plain-text counts, not chips.

### Freshness

- **Freshness line.** `text-secondary`, on every panel and card: "Updated 40 s ago". Never coloured. When the person pauses live updates, a neutral "Live updates paused" label sits beside it until they resume.
- **Stale panel.** Stale hatch, `neutral-ink`, a sentence in words: "No data from cluster eu-2 since 02:10 CET. What you see may be out of date." Replaces the panel's health colour entirely.

### Settings

- **Settings row** (B6, B6b). Label, explanation, control. Ticks and radios use a `text-secondary` outline. "Required" (heartbeat) is a neutral chip, not a disabled checkbox. "Tick again" is a warning chip with its sentence.

## Do's and Don'ts

| Do | Don't |
|---|---|
| Repeat every colour with a word | Use colour, icon or position as the only signal |
| Turn out-of-date panels and cards grey and hatched, with "No data since 02:10 CET" | Keep a stale panel green, or keep healthy words on a stale card |
| Show Verified facts (green) and Nightshift's explanation (yellow) as two separate, labelled blocks | Merge facts and explanation, or drop the yellow when a template wrote the text |
| Use `border` for dividers only; outline controls and clickable cards in `text-secondary` | Rely on `border` as a control's or a clickable card's only outline |
| Use tinted chips with a line border | Use solid saturated status fills (the rejected Clinical Contrast look) |
| Keep `primary` for the one primary action per decision | Colour "Reject" red or make it look disabled |
| Define light and dark for every token | Ship a token without its `-dark` twin |
| Keep tokens neutral until mapped to Quornex's system [OPEN: Orvex, O-12] | Import or store Orvex brand material in this repo |
| Keep "Manual repair" steps on a plain surface | Put catalogue steps in the yellow AI block |
| Measure contrast in the rendered result | Claim WCAG compliance from token ratios alone |
