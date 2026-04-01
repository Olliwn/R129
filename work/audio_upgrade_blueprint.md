# R129 Audio Upgrade Blueprint (OEM+ 2.1 System)

## Philosophy & Architecture
This document details a "First Principles" audio upgrade for the Mercedes R129. The goal is to provide modern, high-fidelity sound with sufficient dynamic headroom while maintaining a strictly 100% factory aesthetic.

Since restoring the rest of the car is a priority, this architecture optimizes for **time savings and proven drop-in fitment** over absolute cost savings. 

### The 2.1 Channel Strategy
The R129 is a 2-seat convertible. Rear speakers only muddy the soundstage. The optimal setup is a powerful 2.1 system:
1. **Front Stage:** High-quality 3-way speakers in the factory door/dash locations.
2. **Subwoofer:** A dedicated 10" subwoofer hidden in the rear driver-side storage cubby.
3. **Amplification:** A micro Class-D 4-channel amplifier hidden behind the dashboard.
   - Channels 1 & 2: Power the front door 3-way speakers.
   - Channels 3 & 4 (Bridged): Power the subwoofer.
   - **Trick:** By wiring the Becker BE2210's "Rear" outputs to the amplifier's Subwoofer inputs, the physical "Fader" dial on the radio becomes the Subwoofer Bass Knob.

---

## Bill of Materials & Budget

### 1. Front Stage (Doors & Dash)
There are two paths here depending on how far down the audiophile rabbit hole you want to go.

**Option A: The Time-Saver (Jehnert Drop-In) - RECOMMENDED**
Instead of fabricating custom mounts and wrestling with crossover wiring, this system is a proven drop-in solution specifically tuned for the R129's cabin acoustics.
*   **Component:** **Jehnert 3-Way Retrofit System (R129)**
*   **Details:** Includes 6.5" woofers, midrange drivers, angled tweeters, and pre-wired R129-specific crossovers. Drops perfectly behind factory grilles.
*   **Cost:** ~€299.00
*   **Time Savings:** Massive. The R129 door cards are notoriously complex. Fabricating custom adapters that seal properly against the door panel (to prevent frequency cancellation) is incredibly time-consuming. This kit preserves your sanity.

**Option B: The Audiophile Route (Focal / Morel / Audison + Adapters)**
If you want absolutely world-class front imaging, you can run high-end aftermarket 3-way components. This requires mounting adapters, as modern speakers don't fit the R129 door cards naturally.
*   **Component 1 (Adapters):** **MR129.com Front 3-Way Component Speaker Upgrade Bracket Kit** ($39 for 3D printing STL files, or ~$150 for physical plastic brackets).
*   **Component 2 (Speakers):** High-end 6.5" 3-way set. 
    *   *Mid-Tier Audiophile:* **Audison Prima APK 163** (~€400)
    *   *High-End:* **Focal PS 165 F3E Flax Evo** (~€499)
    *   *Ultra High-End:* **Focal ES 165 KX3E (K2 Power Series)** (~€1,399)
*   **Cost:** ~€450 to €2,300+ (depending on speaker choice)
*   **Time Cost:** Requires printing/buying adapters, potentially trimming door plastic, custom wiring the crossovers, and finding space inside the door card for the crossover boxes.

### 2. Subwoofer (Phase 2 / Long-Term Project)
The rear storage compartments are the perfect acoustic chambers. Since this is hidden beneath the factory locking lids, cosmetic perfection is not required—just a clean, vibration-free installation that doesn't damage the car.

**Option A: The Time-Saver (Jehnert Drop-In)**
*   **Component:** **Jehnert R129 Bassreflex Subwoofer**
*   **Details:** Custom fiberglass enclosure with a 10" (250mm) double voice coil woofer. Replaces the cubby liner to maximize air volume.
*   **Cost:** ~€735.00
*   **Pros:** Zero fabrication time. Perfectly tuned port for the exact volume of the R129 cubby.

**Option B: The High-Tech "Dual Drive" DIY Route (Punch over Volume)**
Since cosmetic perfection isn't required beneath the factory lid, you can build a custom sealed MDF enclosure. For a "Genelec" style tight, punchy, and distortion-free bass response (rather than booming volume), dual small-diameter high-tech woofers are ideal. This pairs perfectly with the Match UP 6DSP, utilizing its two 160W channels.

*   **Approach 1: Dual Audison Prima APS 8 D (8" Shallow)**
    *   **The Tech:** Specifically designed for ultra-small sealed boxes. Flat cone geometry and suspension built to handle high box pressure.
    *   **Required Box Volume:** 7.5 to 8.5 liters per woofer (approx. 16 liters total for the dual box). This is incredibly small, leaving room in the cubby for the DSP or other storage.
    *   **Cost:** ~€159/each (~€320 total) + MDF materials.
*   **Approach 2: Dual Dayton Audio Epique E150HE-44 (5.5" Extended Range)**
    *   **The Tech:** Pure acoustic engineering marvel. Uses a patented "MMD" dual magnetic gap motor to drastically lower distortion and allow massive 14.7mm excursion. It's technically a 5.5", but plays like an 8".
    *   **Required Box Volume:** Approx. 4 to 5 liters per woofer (approx. 10 liters total for the dual box). The box could literally be the size of two shoeboxes.
    *   **Cost:** ~€139/each (~€280 total) + MDF materials.
*   **Next Step:** Build a cardboard mockup of the R129 storage tub to determine how to best utilize the space. Because these require so little volume (10-16 liters), you may only need to use the bottom half of the tub, leaving the top half usable for storage by building a false floor.

### 3. Amplification & Digital Signal Processing (Fully Active 8-Channel Approach)
If the goal is to run all three front elements (tweeter, midrange, mid-bass) independently—bypassing passive crossovers entirely for ultimate "Genelec-level" control—you need an 8-channel DSP amplifier. This gives every single speaker in the car its own dedicated amplifier channel, time-alignment, and EQ.

*   **Component: Match UP 8DSP** (~€749.00)
    *   **Details:** 8-channel DSP Amplifier (6 × 65W + 2 × 160W). Made by Audiotec Fischer.
    *   **Why it's the Holy Grail:** 
        *   **Channels 1 & 2 (65W):** Left/Right Tweeters
        *   **Channels 3 & 4 (65W):** Left/Right Midranges
        *   **Channels 5 & 6 (65W):** Left/Right Mid-bass Woofers
        *   **Channels 7 & 8 (160W):** Left/Right Subwoofers (Perfect for the dual-drive DIY box).
    *   **Size:** Astonishingly compact (153 x 130 x 46 mm), making it very easy to mount in the rear cubby.

---

## 4. Alternative Front Stage (2-Way)
If simplifying the door wiring (omitting the midrange speaker entirely) is preferred while maintaining high-end build quality.
*   **Component:** **Ground Zero GZHC 165.2** (6.5" 2-way component set)
*   **Details:** 220W power handling, cast aluminum basket. 
*   **Cost:** ~€349.00
*   **Trade-off:** Losing the 3-way midrange means you lose some of the vocal richness the R129 door placement naturally supports, but installation is much faster as there is one less speaker per door to mount.

### 4. Wiring & Connectors
*   **ISO Speaker Harness Extensions:** To run from the BE2210 to the amp, and amp back to the factory wiring.
*   **Speaker Wire:** 10m OFC 2x1.5mm² (Already in inventory: SP Elektroniikka).
*   **Cost:** ~€30.00

---

## Total Estimated Budget: ~€1,314.00

## Installation Workflow (Time-Optimized)
1. **Amp Placement (Revised):** DO NOT mount the DSP amplifier behind the climate control/ashtray. That cavity sits above the transmission tunnel and is a notorious heat trap, leading to thermal shutdown. Route the high-level inputs from the BE2210 under the center console carpet to the **rear storage cubby**, and mount the DSP amplifier there alongside the subwoofer.
2. **Wiring Upgrade (Fully Active & Reversible):** To maintain the ability to restore the car to factory 100% original spec, **do not cut or remove the 1991 factory door wiring.** Simply unplug the factory harness from the old speakers, tape off the connectors, and tuck them safely inside the door cavity. Run fresh 16-gauge OFC speaker wire from the rear-mounted Match UP 8DSP directly to *each individual new speaker* in the doors (3 pairs of wire per door). 
    *   *Critical R129 Warning (The Door Boots):* Snaking three pairs of new speaker wire through the R129's rubber door boots is notoriously difficult. These boots also contain the fragile plastic vacuum lines for the PSE central locking system. If you force a coat hanger through and crack a 35-year-old vacuum line, your door locks will stop working. 
    *   *Pro-Tip:* Do the easy work yourself (mount speakers, mount amp, run wire under sills), and consider paying a professional high-end car audio shop for 2-3 hours of labor *just* to safely fish the wires through the door boots. They have the specialized fiberglass fish-tape, lubricants, and liability insurance.
3. **Front Doors:** Remove door panels. Remove old speakers. Screw in the Jehnert (or Focal + adapter) 3-way components. 
4. **Subwoofer:** Build the custom sealed MDF dual-drive enclosure or install the Jehnert drop-in box into the rear cubby. 
5. **Final Connection:** Connect all fresh wiring to the rear-mounted DSP amplifier and tune via laptop.
