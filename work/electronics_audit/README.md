# Predictive Electronics Maintenance -- Capacitor & Solder Joint Audit

**Vehicle:** 1991 Mercedes-Benz 500 SL (R129) | VIN: WDB 129066 1F 044414

*Prompted by the OVP relay failure (2026-03-30). If the OVP -- which lives inside a sealed, relatively protected box -- had thermal fatigue cracks on 25% of its joints after 35 years, other modules exposed to the same engine bay thermal cycling are almost certainly showing similar degradation. Early '90s electrolytic capacitors are a known ticking time bomb: when they leak, the acidic electrolyte eats through PCB copper traces, permanently destroying the board.*

---

## Hit List (ranked by failure consequence)

| # | Module | Location | Risk | What to Inspect | Priority |
|---|--------|----------|------|-----------------|----------|
| 1 | **N4/1 EA/CC/ISC** (E-Gas / Cruise Control) | Electronics bay, far left (tall silver module, wavy ribs, lever lock) | Controls electronic throttle actuator. Dried/leaking elcos can cause erratic throttle voltage, sudden limp mode, surging idle, or burning out the throttle body motor (very expensive). | Open case. Inspect elcos for bulging/leaking. Reflow heavy transistor legs (thermal cycling cracks). | HIGH |
| 2 | **MAS (N16)** (Mixture Adjustment System) | Electronics bay, middle left (twist-knob lock, next to OVP) | Handles high-amperage current for fuel pump relay. Same cracked-solder-joint failure mode as OVP. If fuel pump circuit cracks → car dies on the highway. High-resistance joint → engine runs lean under load. | Open case. Inspect solder joints on heavy pins (same technique as OVP). Inspect elcos. | HIGH |
| 3 | **Instrument Cluster (KI)** | Dashboard | Early R129 clusters infamous for leaking elcos. Leaked electrolyte eats PCB traces → coolant temperature or oil pressure gauge reads falsely or dies. Driving the M119 V8 without knowing it's overheating = blown head gasket. | Pull cluster (Phase 3 in ADS diagnostic plan). Inspect/replace the 4-5 electrolytic capacitors on the back board. | HIGH (sneaky) |
| 4 | **EZL (Ignition Control Module)** | Usually driver-side inner fender well (large black box, heavy cooling fins) -- or possibly the heavily finned front module in the electronics bay | If this dies, car cranks but never starts. Replacements extremely rare (>$1,000). Internals are potted -- **DO NOT OPEN**. The thermal paste between the module and its mounting surface has dried to chalk after 35 years. | **Do NOT open.** Unbolt from mounting. Clean off old thermal paste. Apply fresh thermal compound (Arctic MX-6 or similar). Remount securely. | CRUCIAL |
| 5 | **N51 ADS** (Adaptive Damping System) | Electronics bay, second from right | Now that OVP is fixed, N51 should boot. If it still shows "dim glow" after OVP reinstall, may have its own internal elco/solder issues. ADS failure = limp mode ride, not stranding. | Inspect only if N51 fails to boot after OVP fix. Open case, inspect elcos and solder joints. | CONDITIONAL |

## Approach

- Combine with existing planned work where possible (cluster is already scheduled for Phase 3 ADS investigation).
- Modules can be pulled one at a time during workshop sessions -- each inspection takes 30-60 minutes.
- Photograph all PCBs before touching anything (reference for trace damage assessment).
- Any replaced elcos should use 105°C-rated, long-life replacements (e.g., Nichicon UHE or Panasonic EEU-FR series).
- **EZL thermal paste refresh is the single highest-value preventive action** -- a dead EZL is a >$1,000 replacement and can kill the car without warning.

## Electronics Bay Layout Reference

See [diary/2026-03.md](../../docs/diary/2026-03.md) Appendix for the full module layout map with positions and descriptions.
