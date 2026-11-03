"""Regenerate review artifacts locally; never writes outside this research folder."""
from pathlib import Path
import csv
import html
import json
import re
from urllib.parse import urlparse
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent
report = ROOT / 'research.md'
text = report.read_text()
replacements = {
    'positive-schema egress service': 'service that constructs outbound requests using only explicitly allowed fields',
    'VM has separate Enterprise features': 'VictoriaMetrics has separate Enterprise features',
    'Benchmark VM single-node locally and VM cluster': 'Benchmark VictoriaMetrics single-node locally and its cluster edition',
    'switch to VM only': 'switch to VictoriaMetrics only',
    'Prometheus vs VM and pipeline/backends': 'Prometheus vs VictoriaMetrics and pipeline/backends',
    'execute once logically using idempotent handlers': 'use idempotent handlers so retries do not repeat the action’s effects',
    'At 250 assumed fleet incidents/night and ten calls/incident, that is 75,000 calls/month': 'Assuming a 30-day month, 250 fleet incidents/night and ten calls/incident yield 75,000 calls/month',
    'One such call per cluster daily adds 300,000 calls/month': 'One such call per cluster daily adds 300,000 calls per 30-day month',
    'Resource/latency targets below are proposed test thresholds to agree later.': 'Resource and latency thresholds remain to be agreed before testing.',
    'Kill Prometheus, checker, API connection and fleet link separately': 'Stop Prometheus and the checker, and interrupt the API connection and fleet link, in separate tests',
    ' Exact stable versions must be pinned at implementation freeze. PRD, decision log, AI_LOG.md and Claude files are unchanged.': ' Exact stable versions must be pinned at implementation freeze.',
    'A shared inference process is not a strong customer isolation boundary.': 'Its API-key mechanism alone does not protect all exposed endpoints: use an authenticated gateway with an explicit route allowlist and restrict network access. A shared inference process is not a strong customer isolation boundary.',
    'The observability and AI digests include release-page snapshots.': 'The evidence digests linked in §14 include release-page snapshots.',
}
for old, new in replacements.items():
    if old in text and new not in text:
        text = text.replace(old, new)

old_identity = next((line for line in text.splitlines() if line.startswith('| Identity/secrets |')), None)
if old_identity:
    text = text.replace(old_identity, '''| Human identity | [Keycloak](https://github.com/keycloak/keycloak) and [Dex](https://github.com/dexidp/dex), Apache-2.0 | Authentication does not establish repair approval/delegation. Central identity refresh can break offline approval workflows. | Reuse Quornex IdP; develop approval authorization separately. | Keycloak for full IAM; Dex for federation. |
| Workload identity/PKI | [SPIRE](https://github.com/spiffe/spire) and [cert-manager](https://github.com/cert-manager/cert-manager), Apache-2.0 | Attested workload identity versus certificate management: distinct approaches, not interchangeable products. Test trust/expiry during disconnection. | Existing PKI and scoped service accounts; cert-manager if already present. | SPIRE when workload attestation and federation justify its control plane/agents. |
| Secret storage/delivery | [OpenBao](https://github.com/openbao/openbao) and [SOPS](https://github.com/getsops/sops), MPL-2.0 | Online secrets service versus encrypted configuration files; different rotation/availability trade-offs. Neither guarantees offline credential continuity. | Encrypted Kubernetes Secrets; SOPS if Git carries secrets. | OpenBao when dynamic secrets/rotation warrant the service; retain local outage plan. |''')
old_display = next((line for line in text.splitlines() if line.startswith('| Notification/display |')), None)
if old_display:
    text = text.replace(old_display, '''| Notification/escalation | [Alertmanager](https://github.com/prometheus/alertmanager), Apache-2.0; [ntfy](https://github.com/binwiederhier/ntfy), dual Apache-2.0/GPLv2; [Gotify](https://github.com/gotify/server), MIT | Alertmanager groups/routes alerts; ntfy/Gotify supply push transports. Push is not guaranteed voice escalation; receipt is not approval. | Alertmanager + portal/Slack adapters; existing transports first. | Delivery receipts, escalation scheduling and independent phone transport; measure carrier/delivery costs. |
| Dashboard/customer views | [Grafana](https://github.com/grafana/grafana), AGPL-3.0 core; native Quornex portal using backend APIs | Grafana plugins/editions have separate terms. Native portal work costs development time. Neither is the local rule evaluator. | Existing Grafana for engineers; develop plain-language portal views. | Tenant-scoped queries, dashboard performance tests and customer evidence permissions. |''')

def slug(s):
    return re.sub(r'[^\w\- ]', '', s.lower()).replace(' ', '-')

headings = re.findall(r'^## (.+)$', text, re.M)
nav = '**Navigate:** ' + ' · '.join(f'[{name.split(". ", 1)[-1]}](#{slug(name)})' for name in headings)
if '**Navigate:**' not in text:
    text = text.replace('\n## 1. Requirements', '\n' + nav + '\n\n## 1. Requirements', 1)
report.write_text(text)

# Export the two major comparison matrices, preserving their exact content.
matrix_rows = []
capture = False
for line in text.splitlines():
    if line.startswith('## '):
        capture = line.startswith('## 2.') or line.startswith('## 3.')
    if capture and line.startswith('| '):
        row = [c.strip() for c in line.strip('|').split('|')]
        if len(row) == 5 and not row[0].startswith('---') and row[0] != 'Component':
            matrix_rows.append(row)
with (ROOT / 'comparison-matrix.csv').open('w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Component', 'Alternatives and licences', 'Limitations', 'MVP', 'Enterprise'])
    writer.writerows(matrix_rows)

diagram = re.search(r'```mermaid\n(.*?)\n```', text, re.S)
assert diagram, 'Missing Mermaid architecture'
(ROOT / 'architecture.mmd').write_text(diagram.group(1) + '\n')

# Every indexed URL occurs in a report or evidence digest, not a generated search list.
entries = {}
inputs = [report] + sorted((ROOT / 'digests').glob('*.md'))
for path in inputs:
    content = path.read_text()
    for label, url in re.findall(r'\[([^\]]+)\]\((https?://[^\s)]+)\)', content):
        e = entries.setdefault(url, {'url': url, 'label': label, 'publisher_host': urlparse(url).netloc, 'accessed': '2026-10-29', 'publication_date': 'undated living source; see digest for release-specific date', 'files': []})
        if str(path.relative_to(ROOT)) not in e['files']:
            e['files'].append(str(path.relative_to(ROOT)))
    for url in re.findall(r'https?://[^\s|<>]+', content):
        url = url.rstrip(').,;')
        if url not in entries:
            entries[url] = {'url': url, 'label': url, 'publisher_host': urlparse(url).netloc, 'accessed': '2026-10-29', 'publication_date': 'undated living source; see digest for release-specific date', 'files': [str(path.relative_to(ROOT))]}
(ROOT / 'sources.json').write_text(json.dumps(list(entries.values()), indent=2) + '\n')
source_lines = ['# Source index', '', 'Accessed 2026-10-29. Official project maintainers/documentation publishers only. This index records sources referenced by the report and digests, not independently verified claims. Release-specific publication dates and confidence limits are in the digests. Undated documentation must not be assigned an invented publication date.', '', '| Source | Publisher host | Used in |', '|---|---|---|']
for e in entries.values():
    source_lines.append(f'| [{e["label"]}]({e["url"]}) | {e["publisher_host"]} | {", ".join(e["files"])} |')
(ROOT / 'sources.md').write_text('\n'.join(source_lines) + '\n')

# Markdown rendering with raw HTML disabled; no runtime/CDN/network dependencies.
md = MarkdownIt('commonmark', {'html': False}).enable('table')
original_heading = md.renderer.rules.get('heading_open')
def heading_open(tokens, idx, options, env):
    title = tokens[idx+1].content
    return f'<{tokens[idx].tag} id="{html.escape(slug(title), quote=True)}">'
md.renderer.rules['heading_open'] = heading_open
body = re.sub(r'^---\n.*?\n---\n', '', text, count=1, flags=re.S)
rendered = md.render(body)
toc = ''.join(f'<a href="#{html.escape(slug(h), quote=True)}">{html.escape(h)}</a>' for h in headings)
source_html = md.render((ROOT / 'sources.md').read_text())
page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Nightshift OSS architecture research</title>
<style>:root{color-scheme:light dark;--bg:#f6f7f9;--fg:#182332;--panel:#fff;--line:#ccd4df;--accent:#075ca9}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,sans-serif}header{padding:2rem max(2rem,6vw);background:var(--panel);border-bottom:1px solid var(--line)}header p{margin:.25rem 0}main{max-width:1450px;margin:auto;padding:2rem}nav{display:flex;flex-wrap:wrap;gap:.4rem 1rem;padding:1rem;background:var(--panel);border:1px solid var(--line)}nav a{font-size:.85rem}a{color:var(--accent)}h1,h2,h3{line-height:1.25;scroll-margin-top:1rem}h2{margin-top:3rem;padding-top:1rem;border-top:1px solid var(--line)}table{border-collapse:collapse;width:100%;font-size:.88rem;display:block;overflow:auto;margin:1.2rem 0}td,th{border:1px solid var(--line);padding:.65rem;vertical-align:top;min-width:140px}th{background:var(--panel);text-align:left}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:var(--panel);padding:1rem;border:1px solid var(--line);font-size:.8rem}code{overflow-wrap:anywhere}.badge{display:inline-block;padding:.25rem .65rem;border-radius:.3rem;background:#fff0cc;color:#623c00;font-weight:600;margin:.4rem .3rem .4rem 0}details{padding:1rem;border:1px solid var(--line)}@media(prefers-color-scheme:dark){:root{--bg:#111923;--fg:#e1e6ef;--panel:#1c2836;--line:#405166;--accent:#8ac8ff}}@media(max-width:700px){main{padding:1rem}header{padding:1.3rem}td,th{min-width:170px}}@media print{nav{display:none}body{background:white;color:black}main{padding:0}a{color:inherit}pre{font-size:8pt}}</style>
<header><h1>Nightshift: open-source architecture research</h1><p>Technical selection · 29 October 2026 · full approved scope</p><p>Decision: choose practical MVP components and enterprise evaluation candidates.</p><span class="badge">Proposal for review</span><span class="badge">Primary-source facts: medium confidence</span><span class="badge">Sizing and 10k capacity: unverified estimates</span><p>Canonical source: research.md. Offline copy: no external scripts, fonts or rendering services. Mermaid source is preserved in the architecture section and architecture.mmd.</p></header><main><nav>''' + toc + '</nav>' + rendered + '<details><summary>Full source index</summary>' + source_html + '</details></main></html>'
(ROOT / 'research-briefing.html').write_text(page)

# Mechanical integrity checks, not a claim of semantic correctness or live-link health.
local_links = re.findall(r'\]\((?!https?://|#)([^)]+)\)', text)
missing = [p for p in local_links if not (ROOT / p).exists()]
anchors = set(map(slug, headings))
anchor_links = re.findall(r'\]\(#([^)]+)\)', text)
bad_anchors = [a for a in anchor_links if a not in anchors]
assert not missing, missing
assert not bad_anchors, bad_anchors
assert len(matrix_rows) >= 25, len(matrix_rows)
assert all(urlparse(e['url']).scheme in ('http', 'https') for e in entries.values())
assert 'CHECK --> HB --> WATCH' in diagram.group(1)
checks = {'local_links_missing': missing, 'bad_section_anchors': bad_anchors, 'matrix_rows': len(matrix_rows), 'source_urls_indexed': len(entries), 'mermaid_source_present': True, 'html_external_runtime_requests': False, 'arithmetic': {'base_cpu': [0.5, 2.6], 'base_ram_GiB': [1.375, 5.1], 'heartbeat_GB_per_30_day_month': 1024*1440*10000*30/1e9, 'series_sample_GB_seven_days': [100000/30*604800/1e9, 2*100000/30*604800/1e9]}, 'limits': 'No software benchmarks, security clearance, live URL sweep or rendered Mermaid parser test performed.'}
(ROOT / 'validation.json').write_text(json.dumps(checks, indent=2) + '\n')
print(json.dumps(checks, indent=2))
