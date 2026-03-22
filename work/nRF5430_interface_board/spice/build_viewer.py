#!/usr/bin/env python3
"""Build inline HTML viewer embedding all SVG schematics."""
import os

SVG_DIR = os.path.join(os.path.dirname(__file__), 'schematics')
HTML_PATH = os.path.join(SVG_DIR, 'viewer.html')

TABS = [
    ('01_power_supply.svg',        '01 — Power Supply',
     '12V automotive → fuse → reverse-polarity → TVS → OKI-78SR (5V) → LD1117V33 (3.3V) + Si2301 P-FET enable → V_DIAG bus'),
    ('02_rx_single_channel.svg',   '02 — RX Channel (Blink Read)',
     'Car diagnostic pin → 1kΩ → TLP521 optocoupler → MCU_RX GPIO (inverted, 13kΩ pull-up)'),
    ('03_tx_single_channel.svg',   '03 — TX Channel (Code Clear)',
     'MCU_TX GPIO → 330Ω → TLP521 (emitter-follower) → 2N2222 driver → car diagnostic pin (pull-low)'),
    ('04_analog_conditioning.svg', '04 — Analog Conditioning',
     'Battery voltage (0–14.4V → 0–2.6V) and airflow pot (0–5V → 0–2.5V) with op-amp buffers + RC filters'),
    ('05_full_diag_channel.svg',   '05 — Full Bidirectional Channel',
     'Complete bidirectional channel: RX (blink read) + TX (code clear) sharing one diagnostic pin'),
]

svg_data = {}
for fname, _, _ in TABS:
    with open(os.path.join(SVG_DIR, fname)) as f:
        svg_data[fname] = f.read()

btn_html = []
panel_html = []
for i, (fname, label, desc) in enumerate(TABS):
    active = ' active' if i == 0 else ''
    display = 'block' if i == 0 else 'none'
    btn_html.append(f'<button class="tab{active}" onclick="showTab({i})">{label}</button>')
    panel_html.append(
        f'<div class="panel" id="panel-{i}" style="display:{display}">'
        f'<h2>{label}</h2>'
        f'<p class="desc">{desc}</p>'
        f'<div class="svg-container">{svg_data[fname]}</div>'
        f'</div>'
    )

html = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<title>nRF5430 Interface Board — Circuit Schematics</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:system-ui,-apple-system,sans-serif;background:#1a1a2e;color:#eee;padding:20px}}
  h1{{font-size:1.4em;margin-bottom:2px}}
  .subtitle{{color:#999;font-size:0.85em;margin-bottom:16px}}
  .tabs{{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:16px}}
  .tab{{background:#2a2a4a;border:1px solid #444;color:#ccc;padding:8px 16px;cursor:pointer;border-radius:6px 6px 0 0;font-size:0.85em}}
  .tab.active{{background:#e74c6f;color:#fff;border-color:#e74c6f}}
  .tab:hover:not(.active){{background:#3a3a5a}}
  .panel{{background:#fff;border-radius:0 8px 8px 8px;padding:20px;color:#222}}
  .panel h2{{font-size:1.1em;margin-bottom:4px}}
  .desc{{color:#666;font-size:0.85em;margin-bottom:12px}}
  .svg-container{{overflow:auto;border:1px solid #ddd;border-radius:6px;padding:12px;background:#fafafa;min-height:200px}}
  .svg-container svg{{max-width:100%;height:auto}}
</style>
</head><body>
<h1>nRF5430 Interface Board — Circuit Schematics</h1>
<p class="subtitle">AOK912 R129 SL · Generated from SPICE netlists via schemdraw</p>
<div class="tabs">
{"".join(btn_html)}
</div>
{"".join(panel_html)}
<script>
function showTab(idx){{
  document.querySelectorAll('.tab').forEach((t,i)=>{{t.classList.toggle('active',i===idx)}});
  document.querySelectorAll('.panel').forEach((p,i)=>{{p.style.display=i===idx?'block':'none'}});
}}
</script>
</body></html>"""

with open(HTML_PATH, 'w') as f:
    f.write(html)
print(f"Written {HTML_PATH} ({len(html):,} bytes)")
