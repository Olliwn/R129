# AOK912 -- Engineering & Maintenance Diary

**Vehicle:** 1991 Mercedes-Benz 500 SL (R129)

**Engine:** M119.960 V8 (32V, KE-Jetronic)

**Transmission:** 722.3 (4-Speed Automatic)

**Chassis:** ADS -- Niveauregulierung mit adaptivem Dämpfungs-System (Level Control with Adaptive Damping)

## Vehicle Data Card (Factory Build Data)
*(Decoded from lastvin.com, 2026-04-01. Order Nr. 0156948800. Built 1991-09, ordered for Sweden.)*
* **VIN:** WDB 129066 1F 044414
* **Model:** 500 SL
* **Engine:** 119960 12 024990 | **Transmission:** 722353 03 604950
* **Paint Code:** 744 (Brilliant Silver Metallic)
* **Interior Code:** 271 A (Leather Anthracite)
* **Weights:** GVWR: 2190 kg | Front Axle: 1010 kg | Rear Axle: 1180 kg
* **Factory Option Codes:** **216 (ADS + self-leveling)**, 236 (DRL), 241/242 (memory seats), 246 (mirror memory), 291 (passenger airbag), 341 (additional blinkers), 406 (orthopaedic seats), 440 (cruise control), 524 (paint preservation), 538 (antenna + speakers, no radio), 551 (ATA anti-theft), 581 (auto A/C), 592 (heated rear glass), 600 (headlamp wash), 630 (ECE triangle), 682 (fire extinguisher), 740 (black soft top), 825 (Sweden pack), 873 (heated seats), 880 (IRCL remote), 881 (roadster storage locking)

## Quick Links

| Document | Purpose |
|----------|---------|
| [Known Issues](known_issues.md) | Current state of all confirmed defects |
| [Active Tasks](tasks.md) | Work queue with priorities and links to work/ READMEs |
| [Budget](budget.md) | Parts and service cost tracking |
| [References & Tools](references.md) | Documentation links and tool inventory |
| [r129_data/SKILL.md](../r129_data/SKILL.md) | Technical data repository search instructions |

## Swedish Registration History

First registered 1991-09-26 at 0 km. 14 total owners. Latest inspection: 2026-01-02 at 139,970 km (Besikta Vellinge). Finnish registration pending (autovero paid 2026-03-27, awaiting rekisteröintilupa). Full vehicle insurance based on VIN is active.

**Odometer analysis:** Smooth readings from 2013 onward (~340 km/year by 16-year previous owner). Cluster confirmed as non-ADS swap (no ADS symbol on indicator strip) -- swap occurred before 2013.

Source: [biluppgifter.se/fordon/AOK912](https://biluppgifter.se/fordon/AOK912). Full data in [diary/2026-03.md](diary/2026-03.md).

## Timeline

*Summary with key technical facts. Full details, exact readings, and context are in the monthly diary files -- always read those when investigating an issue.*

### [March 2026](diary/2026-03.md)

| Date | Summary |
|------|---------|
| Pre-purchase | Dealer restoration: new OEM soft top (~40k SEK), front bumper repaint, driver seat leather, interior trim. ADS/PSE/cluster issues not discovered at sale. |
| Mar 13 | **Purchase & 700km shakedown** (Vellinge → Kapellskär). M119 cold start healthy, no cam oiler ticking. 722.3 fluid level correct at 80°C. Slight 700-800 RPM idle vibration (engine mounts). Soft top cycle fast and quiet (dark ZH-M fluid noted). Missing cluster lamp noticed. PSE central locking completely silent/dead. |
| Mar 14 | **Finland arrival.** ADS confirmed in failsafe/limp mode (rear sits ~2cm low). Hybrid R129 project kickoff -- RPi5 + components from Verkkokauppa (€200). |
| Mar 15 | **Helsinki → Oulu transit** (600km). Wiper does not park correctly. Only 2 of 4 washer nozzles work. Rear fender paint cracking below trunk lid. Bare steel behind front wheels. |
| Mar 17 | **UI architecture finalized.** RPi5 + 5.5" OLED cubby display + Alps RKJXT1F42001 encoder. DigiKey order: ADC (ADS1115), level shifters (TXB0108), TVS diodes, Murata DC-DC converters. Owon HDS242 oscilloscope ordered. |
| Mar 18 | **First blink-code diagnostics** (X11/4 connector, battery <12V). Pin 9 (ADS): dim static glow only -- later proved to be low voltage, not a fault. DI/EZL (Pin 8): 17 pulses, cleared. RST (Pin 10): 11/20/28/29, required two reset cycles. ESMC (Pin 14): 11/12, cleared. **ATA (Pin 11) & IRCL (Pin 12): static glow, no valid blink -- diagnosis "dead modules" but see Apr 1 caveat (may have been unpowered by blown trunk fuse).** Michelin tires ordered (~€1,350). |
| Mar 21 | **First wash.** No-start resolved (loose negative battery terminal). Belt squeal on cold start discovered. Wiper blade replaced. |
| Mar 22 | **Tool procurement** (Motonet/Puuilo, €548). Autodoc baseline service parts ordered (MANN filters, NGK plugs, ATE brake fluid). Datakarte decoded -- factory options confirmed: ADS (211), heated seats (873). **Trunk F20 fuse box inspected:** 6 torpedo fuse positions (P/N A 129 540 04 50), all original aluminum fuses. Fuse #6 (8A white, bottom position) found blown. No fuses replaced yet; copper/ceramic replacements on hand. |
| Mar 23 | **ADS MODULE ALIVE** -- re-tested Pin 9 at >13V (engine running): 1 blink = no stored faults. Earlier dim glow was purely a voltage issue. Console switch LED illuminates and turns red in Sport. **European ADS I includes level control** (Niveauregulierung) -- German Betriebsanleitung p.97 confirms, correcting earlier US-manual assumption. **Cluster swap confirmed** (2026-03-26 photo: no ADS symbol on indicator strip = non-ADS cluster). Fahrzeugniveau switch present. ADS hydraulic reservoir below MIN mark. **ATA Pin 11 re-tested at >13V: still static glow -- concluded "Genuine module fault" but see Apr 1 caveat.** |
| Mar 27 | **Swedish papers received.** Autovero €837.05 paid. Finnish registration process unblocked. ADS code 14 (steering angle sensor) appeared. Battery voltage drops ~13V → ~12V in 2 days idle (parasitic drain investigation opened). |
| Mar 28 | **ADS back online.** Code 14 cleared by lock-to-lock steering at standstill. Both ADS console switch and Fahrzeugniveau switch functional. Fluid circulating through system, no visible leaks. Rear height still static (~2-3cm low). |
| Mar 29 | **Phase 1 ADS flush & air-lock confirmed.** Baseline ride heights: FL 67.5cm, FR 67.0cm, RL 64.0cm, RR 64.5cm (rear ~2-3cm low). 4L ZH-M (Febi 02615) flushed through system. Air entrapment confirmed (bubbles in reservoir). ADS went offline mid-flush (diagnostic bus dim glow on Pin 9). BE2210 Becker radio installed. Driver seat lower latch repaired. |
| Mar 30 | **OVP RELAY ROOT CAUSE FOUND.** 3-4 cracked solder joints visible under magnification (thermal fatigue, worst on 87L pin = N51 ADS power feed). Explains all intermittent ADS behavior (module losing power under thermal expansion). Deliveries received: hood insulation pad, MANN filters, Corteco engine + transmission mounts. Air filters (2x MANN C 3388) and cabin filter (CU 5041) installed. Electronics bay modules mapped (N51, KE-Jetronic ECU, etc.). |
| Mar 31 | **OVP relay re-soldered** (Sn63/Pb37 on all pins). Optical inspection: good wetting, no ring cracks, no cold joints, no bridges. Awaiting reinstall + test. **R129 technical data repository built:** 150 PDFs curated (110 included, 40 excluded), 2,435 JSONL chunks with Gemini Vision image transcription, embedding search (768-dim vectors). |

### [April 2026](diary/2026-04.md)

| Date | Summary |
|------|---------|
| Apr 1 | **OVP REINSTALLED — ADS SYSTEM ONLINE.** Re-soldered OVP relay installed. N51 boots cleanly, both cabin switches show red LEDs, diagnostic bus stable. Pin 9 returns code 14 only (steering angle sensor — clear with lock-to-lock). **OVP 87L solder joint confirmed as sole root cause of all intermittent ADS failures.** Next: clear code 14, closed-loop bleed. |
| Apr 1 | **Trunk fuse 6 investigation.** Fuse designation card in data repo is for **post-facelift F4** (1996+), not this car's **pre-facelift F20**. Forum evidence: fuse 6 = central locking on pre-facelift. March ATA/IRCL "dead module" diagnosis needs recheck after fuse replacement (modules may have been unpowered). |
| Apr 1 | **Factory build data decoded** (lastvin.com). Paint corrected: **744 Brilliant Silver Metallic** (was 199 Blauschwarz — wrong). ADS confirmed factory option **216** (self-leveling + ADS). Non-ADS cluster is a confirmed previous-owner swap. Option 538: car delivered without radio (common European practice) — BE2210 and prior Sony are both aftermarket. Engine serial 119960 12 024990, built 1991-09 for Sweden. |
| Apr 2 | **MB-osat Oulu first visit.** Ordered: ADS suction filter, thermostat (82°C), valve cover gasket sets (L+R), upper timing chain guide slide rails (>100 €/side). Intake hoses discontinued — need DIY repair. MB klubi -15% discount. |
| Apr 2 | **REGISTRATION COMPLETE — JNY-315.** Finnish plates issued. First real drive post-OVP fix. **ADS Sport/Comfort CONFIRMED WORKING** — inspector independently commented on smooth ride. **All four spheres healthy** (earlier FR stiffness was air-lock). **Fahrzeugniveau switch STUCK** (red LED permanently on, new symptom). **⚠️ Dust boots missing lower sections** — ADS shock shafts exposed, urgent order needed (A 129 323 01 92). Underbody clean (summer car), no transmission leaks, exhaust center silencer starting to rust, rear diff surface rust. |
| Apr 17 | **New summer tires installed.** Staggered Michelin 17" set fitted: front 245/45 ZR17 Pilot Sport 5 (99Y XL), rear 275/40 ZR17 Pilot Sport PS2 (98Y FSL). Retires 2015-dated tires. **Cold pressures for this fitment: 2.3 bar / 33 psi front, 2.5 bar / 36 psi rear** (factory fuel-flap placard applies only to the original 225/55 R16 size, not this upgrade). Tire shop delivered at **2.8 bar all round — excessive** (common shop over-inflation habit); to be bled down cold. Wheel bolts to 110 Nm (manual p.69); re-torque after ~50 km. Expect closure of the 2026-03-13 "skittish on old rubber" observation. |
| Apr 18 | **Tire pressures corrected + new battery installed.** Bled all four tires from as-delivered 2.8 bar to target 2.3 F / 2.5 R cold; first drive confirms new Michelins + correct pressure restore the expected ADS ride quality and straight-line stability. **New battery:** Kärkkäinen Oulu, €159 — replaces the sulfated Varta H3 (67 mΩ DC impedance, 3–4× healthy, cranking dip to 8.5 V at 3 °C). Closes the open "Battery / Parasitic Drain" known-issue for the battery side and unblocks a clean re-run of the parasitic-draw test. Trickle charger disconnected; Owon waveform re-capture pending. |
| Apr 18 evening | **Opportunistic underbody + engine inspection — three positive findings.** (1) **Rear ADS dust boots visually intact** — rear strut photo shows convoluted rubber bellows present, seated, no exposed chrome. Apr 2 "missing lower sections" note was front-biased; ADS boot order scope reduces from ×4 to ×2 fronts pending Apr 19 front photos. (2) **M119 oiler tube** visible through oil filler hole as silver/matte horizontal object — consistent with factory aluminum (P/N 119 187 00 87), the robust early-M119 spec. Tap/wipe confirmation tomorrow. (3) **Engine oil at 1800 km is light honey amber, translucent, no top-up** — indicates low blowby, no fuel dilution, no coolant intrusion, intact ring seal. **Reclassifies M119 internals from "unknown" to "cautiously healthy"** — first affirmative engine-health data point for this vehicle. New file `docs/engine_condition_baseline.md` started to capture this and future positive data. Oil change demoted to normal schedule (end of season); next change will pair with UOA + filter cut + magnetic sump plug install. |
| Apr 19 | **Four-job Sunday session.** (1) **Jack-stand saddle pads finished** — Carman kumityynyt cut to V-profile for Bahco BH33000; unlocks all future under-car work. (2) **Coolant cap replaced** (Febi 06568) — no bleeding required, no system opened. (3) **ADS suction filter replaced** (A 129 327 00 91) — opportunistic; primed cleanly, no pump cavitation on first start. (4) **Crankshaft position sensor replaced** (Topran 408 205) — old harness wire cut at extraction (factory routing looped around a bolted-on engine feature); new sensor uses same endpoints but bypasses the "top of engine" loop. **First-start clean** (1–2 min idle, no leaks, no abnormal noise). **Pin 8 = 1 blink with engine running = Code 17 cleared** — sensor swap confirmed successful. KOEO still reads 17, but this is a normal VR-sensor artifact (zero signal at zero RPM), not a fault — documented for future reference so Pin 8 is always read engine-running going forward. **Pending closure:** test drive + Pin 8 re-read *while engine is still running* + hot wire-routing inspection of the "top of engine" bypass section (thermal exposure risk to address with heat-shielded loom if needed). |
| Apr 19 (test drive) | **Two additional findings during the post-work drive.** (a) **Fahrzeugniveau ride-height switch — electrical side RESOLVED.** LED now toggles on/off correctly with the center-console switch (first normal behavior since Apr 2 "stuck" observation). Likely self-healed via new battery + exercised contacts + ZH-M flush. **However, no observable ride-height change** from raise commands, so the rear-droop problem is now **confirmed hydraulic**, not electrical. Narrows the diagnosis meaningfully: next ADS session needs manual rear-valve test (ARB linkage disconnected, lever moved by hand on jack stands) to isolate mechanical valve vs. solenoid/pump/leak/sphere. (b) **Engine belt squeal re-emerged, spray treatment exhausted** — confirms the Apr 3 glazed-belt hypothesis beyond doubt. Belt set promoted from Priority 4 "inspect first" to new **Priority 1B — order now** in `parts_to_order.md`. Tensioner inspection flagged as co-requirement (weak tensioner is often the root cause of belt glazing; replacing the belt without inspecting the tensioner risks repeat failure). |
| Apr 19 (post-drive) | **Crank sensor job CLOSED ✅.** After ~15 km drive including throttle excursions to ~6 k RPM, Pin 8 re-read with engine still running returns **1 blink, no faults.** Apr 4 failure mode ("Code 17 returns after every drive") no longer present under identical load conditions. Topran 408 205 swap confirmed successful; re-routed sensor wire survived the run with no burnt-plastic / smoke / abnormal engine behavior. `known_issues.md` moved OPEN → RESOLVED. Still open: hot wire-routing walk-through of the "top of engine" bypass, Owon cranking-waveform baseline on new battery + sensor, and Apr 17 wheel-bolt re-torque. **New finding: exhaust center-silencer shell perforated** (load-range resonance 2–3.2 k observed under load, absent in neutral, absent above 3.5 k — classic V8 mid-silencer cavity resonance; photo confirms visible through-hole in silencer shell + detached heat shield). Initially misidentified as a catalytic converter before owner corrected: cats are separate units per bank further forward in the tunnel. Added as OPEN / MEDIUM known issue; under-car inspection now unblocked by today's saddle-pad fabrication. Decision gate after inspection: weld-patch (€50–150) vs. silencer replacement (€80–250 part + €80–150 install) vs. full mid-section if cats also failing. **Sidebar:** Biltema car-stereo install kit (art. 84-574) bought with intent to cover UP 6DSP power wiring; closer strand-tip inspection revealed CCA (not OFC) — return planned, proper OFC to be sourced from SP Elektroniikka locally. |
