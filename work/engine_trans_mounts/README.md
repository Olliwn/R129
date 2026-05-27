# Engine & Transmission Mount Replacement

**Vehicle:** 1991 Mercedes-Benz 500 SL (R129) | **Engine:** M119.960 V8 | **Trans:** 722.3

## Overview

Replace both fluid-filled engine mounts and the transmission mount. The original mounts are 35 years old and almost certainly collapsed, causing drivetrain vibration, excess engine movement, and poor idle quality. This is a Phase 4 item from the [Master Plan](../../docs/R129%20Master%20Plan.md) and cross-referenced in the [Baseline Service](../baseline_service/README.md) sections F and H.

**Estimated time:** 2–3 hours total (engine mounts ~90 min, trans mount ~15 min additional).

---

## Key Decision: Jack from Below vs. Lift from Above

**Answer: Jack the engine up from below.** Every documented R129/M119 DIY procedure uses this method.

### Why jacking from below works
- A floor jack under the **oil pan** (with a thick wood block to spread the load) lifts the engine just enough (~10–15mm) to unload the mounts and slide them out.
- No need to disconnect anything above the engine (intake, wiring harness, hood, etc.).
- The fan shroud just needs to be unclipped/loosened so it doesn't bind as the engine rises slightly.

### Why lifting from above is impractical
- The R129 has no engine hoist points designed for in-situ lifting — the factory only lifts the engine from above during full removal (engine + trans as a unit, dropping the subframe).
- Using a cherry picker / engine hoist from above would require removing the hood, potentially the radiator, and rigging a lifting bracket across the intake manifold — massively more work for no benefit.
- The mounts only need ~10–15mm of relief, not a full engine lift.

**Verdict:** Floor jack + wood block under the oil pan. No overhead lifting needed.

---

## Custom Tool Needed?

**Short answer: Probably not, but a 16mm offset wrench helps a lot.**

### The tight bolt problem
The **top 16mm bolt** that secures the engine mount bracket to the mount sits in a very tight space between the engine block and the chassis rail. A straight socket or ratchet may not fit.

### Options (pick one)
1. **16mm offset wrench** — the "correct" tool. Cheap and reusable. Check Motonet/Kärkkäinen.
2. **Flex-head ratchet + 16mm socket** — works once the bolt is broken loose. A stubby ratchet also works.
3. **DIY fabricated tool** — some owners weld/bend a piece of flat steel with a 16mm socket welded on. Overkill for this job.

**Recommendation:** Buy a 16mm offset wrench or confirm your flex-head ratchet fits before starting. No truly custom tooling is required.

---

## Parts

| Qty | Part | MB Part Number | Notes |
| :-- | :--- | :------------- | :---- |
| 2 | Engine Mount (fluid-filled) | 124 240 26 17 | Left and right are identical. Fits M119 R129 1990–1995. |
| 1 | Transmission Mount (722.3) | 129 240 04 18 | Inspect; replace if sagging or cracked. |
| 2 | Engine Mount Bracket Bolt (top) | — | M10×1.5, reuse if in good condition. Torque: 55 Nm. |
| 4 | Engine Mount to Subframe Bolts | — | M8, 13mm head. Torque: 35 Nm. Blue Loctite. |

**Sourcing:** MB-osat.fi, Autodoc.fi, or The SL Shop (parts.theslshop.com).

---

## Tools Required

| Tool | Size | Purpose |
| :--- | :--- | :------ |
| Floor jack (2+ ton) | — | Lift the engine from below via oil pan |
| Jack stands (3-ton) | — | Support the car (see [Jacking Instructions](../baseline_service/Jacking_Instructions.md)) |
| Wood block | ~150×150×40mm | Distribute jack load on oil pan |
| Socket set | 8mm, 13mm, 16mm | Splash shield, mount-to-subframe bolts, top bracket bolt |
| 16mm offset wrench or flex-head ratchet | 16mm | Top mount bolt (tight clearance) |
| Torque wrench | 35–55 Nm range | Final tightening |
| Breaker bar | 1/2" drive | Breaking loose the old bolts |
| Blue Loctite (242) | — | Subframe bolts on reassembly |
| Penetrating oil (WD-40 / PB Blaster) | — | Soak bolts the night before if possible |

---

## Procedure

### Preparation
- [ ] **0.1** — Order parts and confirm delivery.
- [ ] **0.2** — Soak all visible mount bolts with penetrating oil the evening before the job.
- [ ] **0.3** — Gather all tools listed above. Confirm the 16mm offset wrench or flex-head ratchet fits the top bolt.

### Phase 1: Access
- [ ] **1.1** — Lift the front of the car and place on jack stands per [Jacking Instructions](../baseline_service/Jacking_Instructions.md).
- [ ] **1.2** — Remove the front belly pan / splash shield (4× 8mm screws).
- [ ] **1.3** — Loosen (do not remove) the fan shroud clips/bolts so it can float upward when the engine is jacked.
- [ ] **1.4** — If needed for access, loosen or remove the front exhaust section and heat shields on the affected side.

### Phase 2: Engine Mount Replacement (×2)
- [ ] **2.1** — From above, loosen the **top 16mm bolt** on the first (passenger-side) mount bracket. Do not remove yet.
- [ ] **2.2** — From below, place the floor jack with wood block under the oil pan. Jack up the engine just enough (~10–15mm) to unload the mount. Watch the fan shroud for binding.
- [ ] **2.3** — Remove the two **13mm bolts** securing the old mount to the subframe.
- [ ] **2.4** — Remove the **top 16mm bolt** fully. Wiggle the old mount out. It may require some jiggling — the space is tight, especially on the driver's side.
- [ ] **2.5** — Compare old and new mounts side by side (collapsed mounts will be visibly shorter/sagging).
- [ ] **2.6** — Slide the new mount into position. Hand-start the top 16mm bolt and the two 13mm subframe bolts.
- [ ] **2.7** — Torque: top bolt to **55 Nm**, subframe bolts to **35 Nm** with **blue Loctite**.
- [ ] **2.8** — Lower the jack slightly to seat the mount, then repeat steps 2.1–2.7 for the **driver's side** mount.

### Phase 3: Transmission Mount Replacement
- [ ] **3.1** — With the engine still slightly raised, locate the 722.3 transmission mount at the rear of the gearbox.
- [ ] **3.2** — Support the transmission with the floor jack (or a second jack) under the trans pan with a wood block.
- [ ] **3.3** — Remove the mount-to-crossmember and mount-to-transmission bolts.
- [ ] **3.4** — Swap in the new mount. Torque to spec.

### Phase 4: Reassembly & Verification
- [ ] **4.1** — Lower the engine fully onto the new mounts. Remove the floor jack.
- [ ] **4.2** — Re-secure the fan shroud.
- [ ] **4.3** — Reinstall heat shields and front exhaust (if removed).
- [ ] **4.4** — Reinstall the belly pan / splash shield.
- [ ] **4.5** — Lower the car off the jack stands.
- [ ] **4.6** — Start the engine and verify: idle vibration should be noticeably reduced. Check for any exhaust leaks if the front pipe was disturbed.
- [ ] **4.7** — After a short test drive, re-check all bolts for tightness.

---

## References

- [BenzWorld: R129 Engine & Transmission Mount Replacement](https://www.benzworld.org/threads/r129-engine-transmission-mount-replacement.1409629/)
- [500E Board: HOW-TO Replacing M119 Engine Mounts](https://500eboard.co/forums/threads/how-to-replacing-m119-engine-mounts.18976)
- [The SL Shop: R129 Engine Mount 1242402617](https://parts.theslshop.com/mercedes-benz-sl-500-r129-engine-mounting-1242402617/)
- [Jacking Instructions](../baseline_service/Jacking_Instructions.md)

---

## Work Log

| Date | Status | Notes |
| :--- | :----- | :---- |
| 2026-03-26 | Created | Work item created. Parts not yet ordered. |
| 2026-05-05 | Promoted to next-weekend slot | Parts confirmed on hand (Corteco 80001913 engine mounts ×2 + Corteco 21652116 trans mount, per `docs/parts_to_order.md` "Engine & Drivetrain Mounts (acquired, awaiting install)" inventory section). Promoted from Phase 4 backlog to **the same session as the next-weekend belt swap (2026-05-09/10)** so the front belly pan + jack-stand setup are shared between both jobs. Trigger: 2026-05-05 distributor cap + rotor swap completed without resolving the cabin vibration → engine mounts now top suspect. The mount swap also removes engine-mount inspection as an open question on the MB-osat suspension quote (see `docs/diary/2026-05.md` 2026-05-05 late entry and `docs/parts_to_order.md` Priority 4B open question #7). **Pre-session prep:** confirm 16 mm offset wrench (or that the flex-head ratchet fits the top bolt) by Friday 2026-05-08; soak mount bolts with penetrating oil Friday evening. **Diagnostic value:** provides an independent A/B on cabin vibration before the MB-osat suspension job — if vibration substantially improves with fresh mounts, residual is more clearly attributable to steering/suspension joints; if unchanged, suspension job becomes the next variable to remove. |
| 2026-05-22 | Slipped past suspension visit, diagnostic value increased | Mount swap was NOT executed alongside the May 6 belt swap (audio + rear-cubby work consumed the planned slot) and was NOT bundled into the MB-osat 2026-05-22 steering/suspension visit (per the May 5 late decision to keep mounts DIY — the engine-mount inspection question was removed from the MB-osat scope, not added). Receipt confirms no mount-related lines were invoiced. **Net state:** parts still on the shelf, procedure unchanged, but the *diagnostic value* of the swap has gone up: with new tie rods, ball joints, lower control arms, wheel bearing, and fresh alignment, the chassis-side noise floor has dropped meaningfully — any cabin vibration that remains after May 22 is much more likely to be drivetrain (mounts, viscous fan, exhaust resonance) and much less likely to be steering/suspension. The "vibration through the cabin" finding from the May 5 distributor entry can now be re-evaluated under cleaner conditions. **Next:** book a Saturday in early June for the swap. **Pre-swap data capture:** take an m1 idle + m2 rev-sweep UMIK-1 capture equivalent to the May 13–14 reference set *before lifting the car* — this lets the post-swap re-measurement quantify what dropped vs what remains, and protects against the May 5 "no pre/post video baseline" mistake repeating itself. The 1×-rev infrasonic line documented in `work/audio_exhaust_synth/m119_sideband_diagnosis.md` is the specific quantitative target to look for attenuation in. |
