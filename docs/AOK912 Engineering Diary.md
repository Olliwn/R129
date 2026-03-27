# **📖 AOK912 \- Engineering & Maintenance Diary**

**Vehicle:** 1991 Mercedes-Benz 500 SL (R129)

**Engine:** M119.960 V8 (32V, KE-Jetronic)

**Transmission:** 722.3 (4-Speed Automatic)

**Chassis:** ADS — Niveauregulierung mit adaptivem Dämpfungs-System (Level Control with Adaptive Damping)

## **📋 Vehicle Data Card (Datakarte) / Manufacturing Plate**
*(Decoded from vehicle body plate and verified against Swedish registration papers)*
* **VIN:** WDB 129066 1F 044414
* **Model:** 500 SL (Typ 500 SL)
* **Paint Code:** 199 M (Blauschwarz Metallic / Blue-Black Metallic)
* **Interior Code:** 271 A (Black/Anthracite Leather)
* **Weights:** GVWR: 2190 kg | Front Axle: 1010 kg | Rear Axle: 1180 kg
* **Option Codes:**
  * **211:** Adaptive Damping System (ADS)
  * **241:** Front seat LH electric adjustable with memory
  * **242:** Front seat RH electric adjustable with memory
  * **246:** Mirror with memory circuit
  * **283:** Draft deflector / wind deflector
  * **440:** Tempomat (Cruise control)
  * **581:** Automatic climate control
  * **592:** Heat-insulating glass, all-around, heated rear window pane
  * **600:** Headlamp wiper/washer
  * **740:** Black soft top fabric 9001
  * **873:** Seat heater for left and right front seats

## **🚨 Known Issues (Health Status)**

*A high-level summary of confirmed defects and mechanical faults requiring attention, separated from the general to-do list.*

*   **ADS System (Suspension) — TWO INDEPENDENT SUBSYSTEMS:**
    * **Subsystem A: Adaptive Damping (electronic, monitored by N51):** Module is **alive, reports no faults** (1 blink on Pin 9, confirmed 2026-03-23 with >13V). Console switch LED works, turns RED in Sport mode. ABS lamp works. **Front Right** accumulator sphere is ruptured/hydro-locked (invisible to N51). **ADS cluster warning lamp: CONFIRMED MISSING — indicator strip has NO ADS symbol at all (2026-03-26 photo).** Not a dead bulb — the printed symbol is absent. Strongly indicates **cluster swap from a non-ADS R129.** Odometer accuracy now in question.
    * **Subsystem B: Niveauregulierung / Level Control (mechanical/hydraulic, NOT monitored by N51):** This subsystem is **completely independent** from the damping electronics. On ADS I, height sensing is MECHANICAL (anti-roll bar linkage to proportioning valve — no electronic sensors). N51 does NOT monitor level control — Pin 9 blink codes cover ONLY damping. **The entire level control system can be dead and Pin 9 still reports "1 blink = healthy."** The only electronic indicator for level control faults is the cluster warning lamp (oil level float sensor) — which is MISSING because the cluster is a non-ADS variant (no symbol on the indicator strip).
    * **Level Control Status: PUMP CONFIRMED ALIVE (2026-03-26).** Quick pump test: topped reservoir to MAX, started engine — fluid level dropped ~2/3 of MAX-to-MIN range. Pump IS circulating. System was starved/air-locked, not dead. **However:** running air-contaminated circuit triggered a fault code → N51 shut down (both switch LEDs dark, unresponsive even during ignition-ON bulb check). **2026-03-27: Pin 9 returned code 14 (steering angle sensor not initialized) — soft fault from the shutdown. NEXT: clear code, re-initialize steering sensor (full lock L→R→center), top up reservoir, then full Phase 1 flush to purge air and stagnant fluid.**
*   **Central Locking (PSE):** Completely inoperative. The pneumatic pump in the trunk is silent when actuated.
*   **Windshield Wiper / Washer:** Wiper does not consistently stop in the correct park position. Washer fluid is only spraying from 2 out of 4 nozzles.
*   **Engine Mounts:** Slight vibration felt in the cabin at 700-800 RPM idle, indicating the fluid-filled engine mounts have collapsed.
*   **Hardtop Fitment:** The front latches bind when locking the hardtop down. Caused by excess thickness from a newly installed headliner; requires manual pull-down assist.
*   **Paint & Body:** Minor paint cracking on the rear fender (below trunk lid). Small deep scratch on the aluminum hood. Bare steel exposed behind the front wheels (requires rust-prevention touch-up).
*   **Engine Belt:** Squeals/chirps immediately after cold start. Needs diagnosis (slipping belt vs. bad tensioner pulley bearing).
*   **Instrument Cluster — Additional Faults (further evidence of swap/age):**
    * **Clock adjustment stuck/locked:** The clock setting mechanism is stale — turning the adjustment knob does not change the time. Workaround: disconnect battery to reset to 12:00, then let it run from there. May be a seized adjustment shaft or corroded internal contacts. Will be inspected when cluster is pulled for the ADS lamp investigation (Phase 3).
    * **Temperature LCD delaminated/washed out:** The small LCD panel that displays outside temperature is fading — segments are losing contrast and becoming difficult to read. This is a known Mercedes age issue (shared with W124/W126/W140) caused by UV degradation of early LCD glass. Fix: replace the LCD panel itself (available as a separate part — 4 screws to open the VDO housing, swap the glass). Verify sensor and connector first before assuming the display is at fault. Both faults will be addressed during the Phase 3 cluster pull.
*   **Battery / Parasitic Drain (NEW 2026-03-27):** Battery voltage drops from ~13V to ~12V in approximately two days of idle sitting. Either the battery itself is failing (age unknown — could be original to the dealer's cosmetic restoration or older) or there is a parasitic current draw in the electrical system. Candidates: the dead PSE pump circuit, ATA/IRCL modules (both show static glow on X11 = powered but not communicating), aftermarket radio wiring, or a stuck relay. **Action:** (1) Test battery CCA and internal resistance. (2) If battery is healthy, perform parasitic draw test (ammeter in series on negative terminal, pull fuses one by one to isolate the circuit). Trickle charger is keeping it alive for now but this needs resolution before summer driving.

## **📅 Log Entries**

### **Pre-Purchase History \- Dealer Restoration (Vellinge Bilbolag, 2024–2026)**

**Location:** Vellinge Bilbolag, Malmö/Vellinge area, Skåne, Sweden

**Event:** Cosmetic and mechanical restoration performed by the selling dealer between acquisition (~April 2024) and sale (March 2026). The dealer invested significantly in making the car presentable. Known work performed:

*   **Soft Top (Cabriolet Roof):** Replaced with a **new Mercedes-Benz OEM original cabriolet roof.** Dealer claimed the investment was approximately **40,000 SEK** (~€3,500) for the roof alone. The soft top cycles fast and quiet — the mechanism and hydraulics are in excellent condition.
*   **Front Bumper:** **Freshly repainted** — paint quality is good. *(Note: rear bumper was NOT repainted; has minor paint cracks underneath.)*
*   **Driver Seat Leather:** **New leather upholstery on the driver's seat** — specifically the outboard bolster (the side that wears from entry/exit). The repair is well done and matches the interior.
*   **Interior Trim:** **Miscellaneous plastic interior pieces replaced** — exact items unknown, but the interior presents well overall. Likely door trim, console pieces, or sun visor components that had become brittle with age.
*   **Detailing:** Thorough **exterior polish and interior deep cleaning.** The car was presented in very good cosmetic condition at the time of sale.
*   **What the dealer did NOT address (discovered post-purchase):**
    *   ADS hydraulic fluid level below MIN (invisible — cluster warning lamp missing due to non-ADS cluster swap)
    *   ADS system in failsafe/limp mode (would not have been obvious on short test drives)
    *   Inoperative PSE central locking
    *   Wiper park position and washer nozzle issues
    *   Engine mounts (requires driving to feel the idle vibration)
    *   Battery condition / parasitic drain
    *   The cluster swap itself — the dealer would not have known the ADS warning lamp was missing unless they were specifically familiar with ADS-equipped R129s

### **March 13, 2026 \- Initial Inspection & Purchase**

**Location:** Vellinge Bilbolag, Sweden

**Mileage:**

**![][image1]Event:** Pre-purchase inspection and acquisition.

* **Engine:** Cold start successful. M119 sounded heavy and healthy. No excessive ticking from cam oiler tubes. Slight vibration at 700-800 RPM idle, indicating likely collapsed fluid-filled engine mounts.  
* **Transmission:** Checked 722.3 fluid level at 80°C in Park. Level correct, shifted into reverse smoothly.  
* **Hydraulics/Roof:** Soft top cycle fast and quiet. Fluid in pump reservoir is dark (ZH-M needs flushing) but no audible pump strain. Hardtop binding at the front windshield latches noted; diagnosed as excess thickness from a newly installed headliner requiring manual pull-down assist.  
* **Chassis/Steering:** Recirculating ball steering box play is within normal limits (slight center dead-zone).  
* **Surprise Discovery:** Identified ADS (Adaptive Damping System) switch on the center console and hydraulic strut actuators under the hood.

### **March 13, 2026 \- The 700km Shakedown**

**Location:** Vellinge \-\> Kapellskär (E4 Highway)

**Event:** First long-distance transit.

* **Performance:** Car performed flawlessly at highway speeds. Engine temps stable.  
* **Ride Quality:** Extremely comfortable, "floating" ride, confirming ADS accumulators (spheres) are not completely blown out. However, the car felt slightly skittish, attributed to 9-year-old (2015) tires and likely a worn steering damper.  
* **Diagnostics (Ferry Transit):** Noticed a missing indicator lamp in the cluster. ~~Originally thought ADS~~ ~~Then thought ABS~~ **Re-opened 2026-03-23:** Downloaded the correct 1991 owner's manual — it confirms ADS **does** have a cluster warning lamp (unlike the 1990 manual we were using). ABS lamp confirmed functional. **The original "missing lamp" may actually be the ADS indicator.** Needs verification. Also noted the pneumatic central locking (PSE) is completely silent and inoperative.

### **March 14, 2026 \- Arrival in Finland & Failsafe Confirmation**

**Location:** Naantali Port \-\> Helsinki

**Event:** Morning systems check and arrival.

* **ADS "Sag" Test:** Noticed the rear of the car sitting lower than the front on the ferry deck. Started the engine; the rear suspension *did not* rise.  
* **Diagnosis:** ADS is confirmed to be in mechanical Failsafe/Limp mode (likely due to a rear leveling valve issue, low fluid, or electronic fault causing the module to cut power). The car is safe to drive, acting on base mechanical springs.  
* **Admin:** Removed Swedish license plates (cut and photo sent to dealer). Requested original Swedish export registration papers via tracked mail to Oulu.

### **March 14, 2026 \- "Hybrid R129" Project Kickoff**

**Location:** Helsinki, Finland

**Event:** Sourcing components for the Phase 2 Telematics architecture.

* Procured Raspberry Pi 5, temporary display, and NVMe hardware from Verkkokauppa.  
* Procured 4mm banana plugs for X11 diagnostic port tapping and Tesa cloth tape for period-correct wiring looms.  
* Prepared for Sunday transit to Oulu via E8.
* **Note:** Noticed a headlight warning light on the dashboard. It was likely triggered when trying the fog lights (pulling out the main headlight switch). Did not recur the following day.

### **March 15, 2026 \- Helsinki to Oulu Transit**

**Location:** Helsinki \-\> Oulu

**Event:** 600km transit, last 200km in rain.

* **Observations:** 
  * Wiper fluid is currently only spraying from 2 out of 4 nozzles (one functioning nozzle per side).
  * Windshield wipers do not always return to the correct park position. Added to Todo list for further investigation.
  * Noticed narrow cracks on the rear fender paint (on the upward-facing area just below the trunk lid) when the car was wet and dirty.
* **Admin:** Car is now safely parked in a warm garage to dry out, wait for Finnish registration, and wait for better weather.

### **March 17, 2026 \- UI Architecture & Component Sourcing**

**Location:** Oulu, Finland

**Event:** Finalizing Phase 2 Telematics hardware and placing electronics orders.

*   **UI Hardware Settled:** After reviewing the physical constraints of the R129's 1-DIN slot, I have finalized the core architecture for the custom UI. The system will be based around the Raspberry Pi 5.
    *   **Display:** The goal is to use a 5.5" AMOELD (from a repurposed smartphone panel) or a high-quality "bar type" IPS LCD (like the Waveshare 6.25" DSI). The display will be mounted as a "Full Cubby Replacement" behind custom machined dark glass/acrylic to maintain a 99% stock, hidden look when turned off. *(See project: [UI_rpi5/partslist.md](../UI_rpi5/partslist.md) for full specs)*.
    *   **Radio:** Ordered a Becker BE2210 ("Mercedes Special"), retrofitted with an internal AUX input for RPi5 audio routing, from [original-autoradio.de](https://original-autoradio.de/) on 2026-03-18. Order #187019, Customer #168451 (PayPal).
*   **Electronics & Prototyping Haul (DigiKey):** Placed a comprehensive order for the UI controls, interface circuits, and project prototyping.
    *   **Controls & Haptics:** ALPS Directional Switch/Encoder (RKJXT1F42001) paired with the Kilo International (OEDNI-90-4-7) matte black machined-aluminum knob for that solid, premium OEM "iDrive" feel.
    *   **Interface ICs & Signal Processing:** CD74HC4051E (8-channel Analog Multiplexer), ADS1115 (16-bit 4-channel ADC for precision analog reading), TXB0108 (Level Shifter Breakout) for logic conversion between 3.3V and 5V.
    *   **Power Supply Design:** Sourced a mix of efficient Murata switching converters (5V/8W and 3.3V/5W OKI-78SR series) alongside traditional LDO regulators (LM2940T 5V, LD1117 3.3V) for clean power rails.
    *   **Op-Amps & Sensing:** LM358P (General Purpose Op-Amps) and INA169 (Current Monitors) to interpret analog automotive signals.
    *   **Protection Circuitry:** 1.5KE18A TVS Diodes (critical for surviving 12V automotive load dumps) and assorted Schottky/Standard Diodes (1N5819, 1N4148, 1N4007) for reverse-polarity protection.
    *   **Prototyping Essentials:** Multiple breadboards, pluggable terminal blocks, jumper wires, pin headers, and SparkFun capacitor & resistor kits.
*   **Diagnostic Tools:** Ordered an **Owon HDS242 Handheld Oscilloscope**. An absolutely essential tool for analyzing CAN/LIN signals, noisy automotive sensors, and verifying the Phase 2 PCB logic timings while in the garage.

### **March 18, 2026 \- Blink-Code Diagnostics & Infotainment Architecture**

**Location:** Oulu, Finland

**Event:** First full diagnostic code extraction via X11/4 connector and documentation of the infotainment hardware architecture.

*   **Blink-Code Diagnostics (X11/4):** Performed a full sweep of the 16-pin diagnostic connector using the blink-code reader. Extracted fault codes from all accessible modules and performed resets where possible. Key findings:
    *   **ADS (Pin 9):** Weak static glow only — no blink codes returned. Confirms the ADS control module is not communicating properly, consistent with the earlier failsafe/limp-mode diagnosis.
    *   **SRS (Pin 6):** 3/8/9 pulses before reset; cleared to 1 blink after reset (was in a 2-blink fault state).
    *   **DI/EZL (Pin 8):** 17 pulses before reset; cleared to 1 blink.
    *   **RST (Pin 10):** 11/20/28/29 pulses; did **not** clear after a single reset (required two attempts). Must power cycle car btweeen resets.
    *   **ESMC (Pin 14):** 11/12 pulses; cleared to 1 blink after reset.
    *   **ATA (Pin 11) & IRCL (Pin 12):** Static glow (medium) — no valid blink response.
    *   Full results logged in: [work/ads_blink_reader/README.md](../work/ads_blink_reader/README.md)
*   **Display Ordered:** Ordered the 5.5" OLED display (1920×1080) for the cubby-mounted RPi5 interface. Expected delivery within one week.
*   **Infotainment Architecture Documented:** Wrote up the full three-zone infotainment system design — Audio Hub (Becker BE2210), Compute & Display (RPi5 + 5.5" OLED in the cubby), and HMI Controller (Alps RKJXT1F42001 joystick/encoder hidden in the ashtray). Includes GPIO pinout, debouncing strategy, and CAT6 wiring plan. *(See: [UI_rpi5/radio_uiknob.md](../UI_rpi5/radio_uiknob.md))*
*   **Summer Tire Selection & Order:** Researched replacement summer tires for the 17" RH wheels (current tires are from 2015). Initial pick was the Nexen N'Fera SU1 (best mid-range), but availability in Finland was zero. Ordered Michelin instead on 2026-03-20:
    *   **Rear:** 2× Michelin Pilot Sport PS2 275/40 ZR17 98Y FSL — 981,99 € (Order #FI-0326-04083)
    *   **Front:** 2× Michelin Pilot Sport 5 245/45 ZR17 99Y XL — 368,37 € (Order #FI-0326-04084)
    *   Total: ~1 350 €. Mixed-generation Michelin set (PS2 rear / PS5 front) due to the 275/40 ZR17 rear size being hard to source in PS5.

### **March 21, 2026 \- First Wash, Battery Fix & Belt Noise**

**Location:** Oulu, Finland

**Event:** First proper wash and exterior inspection. Resolved a no-start condition.

*   **Exterior Wash & Inspection:**
    *   **Body behind front wheels:** Bare steel may be exposed — looks like a previous owner ground down some rust. Needs protective treatment (primer/paint) before corrosion returns.
    *   **Rear bumper:** Confirmed the small paint cracks underneath (noted previously). No additional paint damage found elsewhere.
    *   **Aluminium roof (driver side):** Minor paint "bulging" at the very bottom edge, <1 mm² area. Not urgent — monitor.
    *   **Driver side mirror:** Stone chip damage (>10 hits) on the plastic mirror housing. Not urgent. Check if a replacement mirror is cheaper than repainting.
*   **No-Start Issue (Resolved):**
    *   Car would not start in the morning — appeared completely dead. Initially suspected a dead battery and charged it, but the car still struggled to start. Purchased a maintenance/trickle charger ("ylläpitolaturi") to keep the battery topped up during periods of inactivity.
    *   **Root cause:** Loose connection on the battery positive (+) terminal. Tightened the terminal bolt and the car now starts normally.
    *   **Action:** Added trickle charger to the garage routine for storage periods.
*   **Wiper Blade Replaced:** Installed a new Bosch Twin 600 wiper blade.
*   **Current Radio Noted:** The installed radio is a Sony CDX-410 (aftermarket, not original to the car). No collector value — to be removed and discarded/sold once the Becker BE2210 arrives.
*   **Belt Noise:**
    *   A belt squeals/chirps immediately after cold start. Needs diagnosis: spray water on the belt while running — if the noise stops momentarily, the belt is slipping (replace belt or adjust tension); if the noise persists or changes character, suspect a worn tensioner or idler pulley bearing. *(See baseline service section D: [work/baseline_service/README.md](../work/baseline_service/README.md))*

### **March 22, 2026 \- Tool & Equipment Procurement Run**

**Location:** Motonet & Puuilo Oulu (Vasaraperä)

**Event:** Acquired the core mechanical tooling, lifting equipment, and fluids required to execute the baseline service and ADS diagnostics. 

*   **Lifting Gear:** Secured 2 pairs of Bahco 3T Jack Stands and rubber lift pads for safe underbody access. (Using existing >2.5T low-profile floor jack).
*   **Specialty Tools:** Procured high-quality Bahco 1/4" Bit Socket Set (to safely remove delicate, seized aluminum M119 bolts), Bahco Pry Bar Set, 74mm/14-flute M119 oil filter wrench, and plastic trim removal tools.
*   **Workshop Organization:** Upgraded garage hygiene with a Kärcher WD3 wet/dry shop vacuum. Repurposing an existing 2-layer plastic toolbox to serve as the "Dedicated R129 Metric Tool Kit."
*   **Fluids & Chemicals:** Stocked up on MB 325.0 Blue Coolant, MB 236.3 Power Steering Fluid, and notably, **Febi 02615 (MB 343.0 / ZH-M) Hydraulic Fluid**. *Note:* Confirmed that the early R129 ADS I system shares this clear/yellow ZH-M fluid specification with the soft top mechanism, avoiding the later green Pentosin CHF 11S.
*   **Total Investment:** 548.52 € across Motonet and Puuilo. *(See full inventory in [docs/Karkkainen_Shopping_List.md](../docs/Karkkainen_Shopping_List.md))*

### **March 22, 2026 \- Autodoc Maintenance Parts Order & Datakarte Decode**

**Location:** Oulu, Finland

**Event:** Placed a comprehensive Autodoc order for the M119/722.3 baseline service and decoded the factory manufacturing plate.

*   **Manufacturing Plate Decoded:** Confirmed original specifications and options. Added full Datakarte to the top of the engineering diary. Crucial confirmation that the car was factory-equipped with ADS (Option 211) and Heated Seats (Option 873).
*   **Computer Box Inspection:** Opened the module "coffin" under the hood. All modules are dry and seated correctly. Located the ADS Control Module (012 545 26 32) and the KE-Jetronic ECU (011 545 97 32).
*   **Rear Fuses Inspected:** The 8-fuse auxiliary block in the trunk is physically intact, but still utilizes old aluminum torpedo fuses. Will be replacing all of them with new copper/ceramic fuses as a preventative measure.
*   **Autodoc Parts Order Placed:** Successfully navigated the "early M119 vs late M119" parts catalog issues. Ordered the following OEM-spec baseline maintenance parts:
    *   **Air Filters:** 2x MANN C 3388 (Specifically verified the 35mm thin filters required for the KE-Jetronic M119.960. Standard 44mm filters from Motonet were returned).
    *   **Cabin Filter:** 1x MANN CU 5041
    *   **Oil Filter:** 1x MANN H 829/1 x
    *   **Power Steering Filter:** 1x MANN H 85
    *   **Fuel Filter:** 1x MANN WK 830/3
    *   **Spark Plugs:** 8x NGK BP5ES (Crucial: Verified these are non-resistor copper plugs. Resistor plugs like the Bosch FR8DC+ will cause misfires with OEM wires).
    *   **Brake Fluid:** 1L ATE TYP200 (DOT 4)
    *   **Shop Supplies:** 50x Neo Tools heavy-duty diamond texture nitrile gloves.
*   **Club Membership:** Paid the official Mercedes-Benz Club membership fee for the year.
*   **Next Steps:** Awaiting parts delivery to begin the baseline fluid/filter flush.

### **March 23, 2026 \- ADS Module Alive & System Architecture Corrections**

**Location:** Oulu, Finland

**Event:** Critical breakthrough on ADS diagnostics. Re-tested blink-code interface with adequate battery voltage and achieved module communication. Corrected several earlier assumptions.

*   **ADS Module Communication (Pin 9):** Re-tested X11 Pin 9 with battery voltage >13V (vs. <12V during the 2026-03-18 test). The ADS control module (N51) is **alive and communicating** — returns **1 blink = no stored fault codes.** The earlier "weak static glow" was caused entirely by insufficient supply voltage. The module requires alternator-level voltage (>13V) to boot from sleep.
*   **ADS Console Switch:** ~~Tested the ADS Sport/Comfort console switch with engine running and off. The switch LED stays off in both conditions.~~ **CORRECTED (later same day):** Re-tested with adequate battery voltage (>13V, engine running). The switch LED **illuminates** (night illumination works) AND **turns RED when pressed to Sport/up position.** The module IS driving the switch correctly. All earlier "dead" observations were caused by insufficient voltage. **ADS console switch does NOT need replacement.**
*   **Pin 11/12 Sanity Check:** Re-tested one of Pin 11 (ATA) or Pin 12 (IRCL) with >13V as a sanity check. Still static glow — not communicating. Unlike ADS, the ATA/IRCL non-communication is NOT a voltage issue. Genuine module fault.
*   **~~Self-Leveling Correction~~** → **Self-Leveling RESTORED (CRITICAL CORRECTION):** Earlier conclusion (based on US manual) that ADS I is damping-only was **WRONG for European-spec cars.** The German Betriebsanleitung 1991–1993 page 97 states: **"Niveauregulierung mit adaptivem Dämpfungs-System (ADS)"** — Level Control WITH Adaptive Damping System. The European ADS I system includes hydraulic ride height control. Components confirmed: hydraulic pump + translucent plastic reservoir (engine bay, next to washer fluid bottle; fluid MB 343.0 / ZH-M, part no. 000 989 91 03), rear level control proportioning valve (mounted mid-rear-axle), anti-roll bar linkage to proportioning valve, and hydraulic lines from shocks to valve. **The rear sitting low (1–2 finger gap) is now the primary suspect for a hydraulic level control failure** — most likely a sheared rear linkage (known ADS I failure: plastic part breaks at lower mounting) or empty/low reservoir fluid. A MBClub UK user with a 1992 500SL had the same symptom caused by a broken linkage — ride height was instantly restored when the pieces were held together. **The "Plastic Reservoir (Next to washer fluid)" noted on 2026-03-17 at "just below minimum and clearer in color" may be the ADS hydraulic reservoir, not the coolant tank.** Needs visual verification: trace hose connections.
*   **Cluster Warning Lamp — RE-OPENED:** ABS indicator confirmed working (symbol present, bulb lights on bulb check). However, **downloading the correct 1991 owner's manual** revealed that ADS **does** have a dedicated cluster warning lamp (page 92: *"The indicator lamp comes on with the key in steering lock position 2 and goes out when the engine is running"*). The earlier conclusion "ADS was never in the standard indicator set" was based on the **1990** manual, which predates ADS entirely. The 1991 manual adds ADS, ASR, ASD, and snow chain indicators — none of which appear in the 1990 manual. **The original "missing lamp" observation from the ferry may have been the ADS indicator after all.**
*   **US vs European Manual + German Manual Confirmation:** Both English manuals (1990 and 1991) are **US-market** editions. The 1991 US diagram shows "CHECK ENGINE" (California-only, page 93) and "BRAKE" text — both correctly absent from the European cluster. Downloaded the German Betriebsanleitung 1991–1993 — its cluster diagram is a **perfect match** to the actual cluster, **except the ADS warning lamp is missing from the user's indicator strip.** This confirms the ADS indicator should be present on a Euro-spec ADS-equipped 1991 500SL but is not.
*   **CLUSTER SWAP CONFIRMED (2026-03-26 photo analysis):** Photo of the unlit indicator strip shows **NO ADS symbol at all** to the left of ASR. All other indicators (ASR, seatbelt, oil, etc.) have clearly visible printed symbols even when unlit. A dead or missing bulb would leave the printed symbol visible through the dead-fronted film. The **complete absence of the ADS symbol** means the indicator strip itself is a **non-ADS variant** — confirming a **cluster swap from a non-ADS R129**. This is NOT a cosmetic issue: (a) the oil-level float warning for the ADS/Niveauregulierung reservoir has been invisible since the swap, explaining why chronic low fluid went undetected for years; (b) the **odometer reading may be inaccurate** — need to compare against service records and Swedish public records when cluster is pulled. The Fahrzeugniveau switch and ADS console switch being original (confirmed working) prove the *car* is factory ADS-spec — only the cluster was swapped. Previous owner had the car for 16 years (Swedish public records); the swap likely predates the dealer who invested in cosmetic restoration but would not have known the ADS warning was missing.

*   **Swedish Registration & Inspection Records (biluppgifter.se, pulled 2026-03-27):**
    Source: [biluppgifter.se/fordon/AOK912](https://biluppgifter.se/fordon/AOK912)

    **Vehicle data:** Fordonsår 1992, modellår 1992. First registered 1991-09-26 at 0 km. Color: Flerfärgad (two-tone). 14 total owners. Current status: påställd (in traffic) since 2026-03-12. Latest inspection: 2026-01-02 at 139,970 km (Besikta Vellinge). Next inspection due by 2028-01-31. Tires: 255/55R16 all round. Service weight 1,940 kg.

    **Odometer history (from inspections):**

    | Date | km | Delta km | km/year |
    |------|---:|---:|---:|
    | 1991-09-26 | 0 | — | — |
    | *(no digital records 1991–2012)* | | | |
    | 2013-04-26 | 135,960 | 135,960 | ~6,270 avg |
    | 2014-04-28 | 136,860 | 900 | 900 |
    | 2015-04-23 | 137,260 | 400 | 400 |
    | 2015-05-11 | 137,330 | 70 | *(re-inspection)* |
    | 2016-04-22 | 137,540 | 210 | 210 |
    | 2017-04-21 | 138,020 | 480 | 480 |
    | 2018-04-30 | 138,370 | 350 | 350 |
    | 2019-05-06 | 138,660 | 290 | 290 |
    | 2020-06-18 | 138,900 | 240 | 240 |
    | 2021-06-30 | 139,270 | 370 | 370 |
    | 2023-07-14 | 139,680 | 410 | ~200 |
    | 2026-01-02 | 139,970 | 290 | ~116 |

    **Why no records before 2013:** Sweden HAS recorded odometer readings at inspections since at least the early 1990s (an SCB/Trafikanalys quality report covers Bilprovningen mätarställningsdata for 1993–1999). The gap is a **biluppgifter.se data availability limitation** — the platform only surfaces records from ~2013 onward. Older inspection protocols (including odometer readings) likely still exist in Transportstyrelsen's archives or Bilprovningen's historical records, but are not publicly accessible through biluppgifter.se. The car was almost certainly inspected every 1–2 years during 1991–2013 — we just can't see those readings online.

    **Owner history (visible entries):**

    | Date | Event |
    |------|-------|
    | 1991-09-26 | First registered (0 km) |
    | 2002-06-25 | Owner change |
    | 2008-07-10 | Owner change |
    | 2008-07-24 | Owner change (quick re-registration) |
    | 2021-01-12 | Finance / leasing company |
    | 2021-03-10 | Company |
    | 2024-04-23 | Dealer (bilhandlare) |
    | 2024-04-25 | Dealer (bilhandlare) |
    | 2024-05-14 | Private person |
    | 2024-08-04 | Current owner |

    The "16-year previous owner" = 2008-07-24 → 2024-04-23. During their ownership (2013–2024 visible period): ~3,720 km over ~11 years = **~340 km/year**. Classic seasonal use — avställd (off road) every October, påställd every April. All inspections in Malmö/Vellinge/Trelleborg area (Skåne).

    **Cluster swap & odometer analysis:** From 2013 onward, odometer readings are smooth and consistent — no jumps or drops suggesting a cluster swap in that period. If the swap happened (as the missing ADS symbol confirms), it was **before 2013** — most likely before 2008 (during the 2002–2008 ownership or earlier). The 22-year gap in publicly available records (1991–2013) means a cluster swap during that period would be invisible in the odometer history. Lifetime average of ~4,240 km/year is plausible for a well-kept convertible. **Pulling the cluster and reading its part number remains the only definitive way to confirm the swap and assess odometer accuracy.** Requesting historical inspection records from Transportstyrelsen directly could also reveal pre-2013 odometer readings and expose any step change.
*   **~~ADS Console Switch Replacement~~** ~~Part number 1298211951.~~ **CANCELLED — switch works fine.** LED illuminates and Sport indicator turns RED. Previous "dead" was low voltage.
*   **Fahrzeugniveau-Einstellung Switch DISCOVERED (German manual page 98):** A **second, separate suspension switch** exists on the car — the **Vehicle Level Adjustment Switch** at position 2 on the left instrument panel (next to the headlight switch). On ADS-equipped cars, this switch **replaces the headlight range adjuster** (Leuchtweiterregler). It controls ride height independently of the ADS Sport/Comfort console switch:
    - **Down = Normal Level:** Default for general driving. Above ~120 km/h, the car auto-lowers ~15mm.
    - **Up = Raised Level:** For poor roads. LED in switch illuminates. Below ~50 km/h, car raises ~30mm. Between 50–120 km/h, reverts to normal. At 120 km/h, auto-switches to Normal and LED goes out.
    This confirms the level control is a **speed-dependent, driver-selectable, fully active system** — not just passive load compensation. **CONFIRMED PRESENT on AOK912** — the owner confirms the switch is physically at position 2 but had mistaken it for an interior lighting dimmer based on the US manual. This confirms the car IS factory ADS-spec. **The cluster, however, is now confirmed to be a non-ADS swap (2026-03-26 photo: ADS symbol absent from indicator strip).**
*   **Fahrzeugniveau Switch & Hydraulic Reservoir Test (later 2026-03-23, engine running):**
    - **ADS console switch:** LED works, turns RED in Sport — electronics fully functional.
    - **Fahrzeugniveau switch:** LED illuminates. Pressing UP (Raised Level) has **NO effect on ride height.** System commands the raise but cannot execute it.
    - **Reservoir level:** The translucent reservoir next to the washer fluid is **below the MIN marking.** MAX/MIN markings are recessed deep inside the canister and hard to read — initial "almost empty" assessment was a misread. Level dropped only ~0.5 cm since 2026-03-17 (within temperature/measurement tolerance). **No active leak found** anywhere under the car. Fluid loss is gradual/historical over the car's 35-year life. Confirms this IS the ADS/Niveauregulierung fluid. **Next: top up to MAX with Febi 02615 ZH-M and retest level control.**
*   **Revised Working Hypothesis (updated 2026-03-26, LATEST):** **PUMP IS ALIVE.** Quick pump test (2026-03-26): topped reservoir to MAX, started engine — fluid level dropped ~2/3 of MAX-to-MIN range. The tandem pump ADS section IS circulating fluid. System was air-locked/starved from years of low fluid, not mechanically failed. **€850 rebuilt pump NOT needed.** However, running air-contaminated fluid through the circuit triggered a fault code — N51 entered full shutdown (both switch LEDs dark, system unresponsive). Left/right suspension stiffness difference felt smaller after the test run (subjective).
*   **NEXT SESSION ACTION PLAN:**
    1. **Read Pin 9 blink codes** — expect fault code(s) from air/pressure anomaly during the pump test. Record all codes.
    2. **Clear fault codes** via X11 Pin 9 procedure.
    3. **Top up reservoir** — level dropped significantly during pump test. Refill to MAX with Febi 02615 ZH-M.
    4. **Proceed with full Phase 1 flush** — purge air and 35 years of stagnant fluid. Parts acquired: 4L ZH-M fluid, PVC hoses (6mm + 8mm), brake cleaner. ADS suction filter (A 129 327 00 91) to be ordered online or clean old one during flush.
    5. **Re-test after flush + bleed** — clear codes again, start engine, verify switches illuminate, test Fahrzeugniveau UP.
    6. Full procedure documented in `work/ads_diagnostic/README.md` Phase 1.

### **March 27, 2026 \- Swedish Papers Received & Finnish Registration Preparation**

**Location:** Oulu, Finland

**Event:** Received original Swedish registration papers (both Part 1 & Part 2) by mail from the Swedish dealer. Finnish registration process now unblocked.

*   **VIN Correction:** Confirmed VIN from the Swedish registration papers: **WDB 129066 1F 044414**. Earlier body-plate decode in this diary was incorrect (misread of stamped characters). Corrected at the top of this document.
*   **Autovero Decision (Verotuspäätös) Received from OmaVero:**
    - Verotusarvo (taxable value): **€3,011.00**
    - Autoveroprosentti: **27.80%** (based on 238 g/km CO2)
    - **Autoveron määrä: €837.05**
    - Data used: Ensirekisteröintipäivä 28.10.1991, 141,000 km, 240 kW, 5,000 cm³
    - Significantly lower than anticipated (~€6,000 based on comparable recent import decisions). The low verotusarvo likely reflects Vero's automated valuation model for 35-year-old vehicles rather than collector market pricing.
*   **Liikennevakuutus:** Already active since 2026-03-16 (Pohjola, full kasko).
*   **Autovero Paid:** €837.05 paid 2026-03-27. Waiting for payment to clear on Verohallinto's account (letter states "muutaman päivän viiveellä") before rekisteröintilupa is released. OmaVero message will confirm.
*   **Finnish Registration — Remaining Steps:**
    1. ~~**Pay autovero** (€837.05)~~ **PAID 2026-03-27.** Wait for rekisteröintilupa confirmation in OmaVero (expected ~March 30–April 1).
    2. **Obtain siirtolupa** (transfer permit) with temporary plates to legally drive to the katsastus station (Swedish plates are cut, car currently has no plates).
    3. **Book rekisteröintikatsastus** at a station in Oulu (K1 Limingantulli, A-Katsastus Oulunportti, or Avainasemat). Car must be physically present for VIN verification.
    4. **Bring to rekisteröintikatsastus:** Both parts of Swedish registreringsbevis (surrendered permanently), Swedish besiktningsprotokoll from 2026-01-02 (to potentially exempt kunnon tarkastus per EU Directive 2014/45/EU), kauppakirja, ID, rekisteröintilupa printout, and liikennevakuutustodistus.
    5. **Ensirekisteröinti** at the same station after passing inspection — receive Finnish plates.
*   **ADS Blink-Code Read (Pin 9):** Read fault codes after the 2026-03-26 pump test shutdown. **Single fault: code 14 = steering angle sensor (N49) not initialized.** Soft calibration fault from the unexpected N51 shutdown — not hardware damage. Fix: clear code, start engine, turn steering full lock left → right → center. See `work/ads_diagnostic/README.md` and `work/ads_blink_reader/blinker_report.md` for full ADS fault code table.

## **📝 Task / Todo List & Quick Studies**

### **1. Windshield Wiper Parking Issue**
* **Symptom:** Wipers do not consistently park in the correct resting position when turned off.
* **Quick Study on Likely Causes:**
  * **Relay/Module Failure:** The N10 combination relay module (or K26 relay) frequently fails or gets dirty contacts, causing incorrect park detection. The internal park sensor contacts inside the wiper motor assembly could also be faulty.
  * **Mechanical Misalignment:** Loose or slipped nuts on the wiper mechanism linkage. The mechanism may need physical realignment to correct the resting blade position.
  * **Motor/Mechanism Binding:** The complex eccentric 'jumping' mono-wiper mechanism is notorious for needing periodic lubrication (under the plastic turtle-shell cover). A binding mechanism can stress the motor, slow it down, and cause erratic parking.
* **Action Item:** Lubricate the mechanism first (easiest fix), check linkage nuts, and if the issue persists, investigate the N10 relay and motor park contacts. *(See project: [Wiper & Washer System](../work/wiper_system/README.md))*

### **2. Washer Fluid Nozzles**
* **Symptom:** Fluid only spraying from 2 of 4 nozzles.
* **Action Item:** Clean and unclog the windshield washer nozzles. Inspect the fluid lines for cracks or leaks. *(See project: [Wiper & Washer System](../work/wiper_system/README.md))*

### **3. Paint Inspection (Rear Fender & Hood)**
* **Symptom:** 
  * Narrow cracks visible in the paint on the rear fender (upward-facing area just below the trunk lid) when wet and dirty.
  * Discovered a small but deep scratch on the hood (approx. 1cm long, fraction of a mm wide) during wash.
* **Action Item:** 
  * Test the hood with a magnet to confirm if it is aluminum (early R129s have aluminum hoods) or steel. If aluminum, it won't rust but should still be sealed. If steel, it needs immediate sealing.
  * Source an OEM-matched touch-up paint pen (base coat + clear coat) matching the car's color code (e.g. 199 Blauschwarz). Thoroughly wash and inspect the areas once the weather improves to determine the depth/severity of the cracking and plan for potential paint correction or preservation.

### **4. Suspension Refresh (ADS & Mechanical)**
* **Engineering Record: 1991 Mercedes-Benz R129 500 SL**
* **1. Vehicle Baseline & Current Status**
  * **Model:** 1991 500 SL (R129) with ADS I (Adaptive Damping System).
  * **Observed Symptoms:** 
    * Rear ride height is low (1-2 finger gap) vs. Front (3 finger gap).
    * ADS Lift Switch is non-functional.
    * ~~ADS Warning Lamp likely disabled/removed~~ ~~Corrected: Missing lamp is ABS, not ADS~~ ~~Re-opened: 1991 manual confirms ADS DOES have a cluster lamp~~ **CONFIRMED (2026-03-26): Cluster is a non-ADS swap — indicator strip has no ADS symbol. Odometer accuracy in question.**
    * System likely in "Limp/Safe Mode" (Defaulted to maximum stiffness).
    * **NEW (2026-03-23):** European ADS I INCLUDES hydraulic level control (Niveauregulierung). Low rear ride height is now suspected to be a failed level control linkage or low hydraulic fluid — not spring sag.
  * **Mechanical Condition:** Rear Nitrogen Accumulators (Spheres) passed the "Bounce Test" (system is firm but not "rock hard" or bouncing/oscillating), suggesting rear diaphragms are currently intact. However, after sitting >24h, the rear compresses significantly more than the front due to hydraulic pressure bleed-off. **CRITICAL FINDING (2026-03-22):** The Front Right shock is "rock hard" with almost zero travel under full body weight, confirming the Front Right nitrogen accumulator is ruptured and hydro-locked. Front Left compresses normally under body weight (feels stiffer than a standard car, consistent with the expected unpowered ADS "failsafe" firm mode), confirming the Front Left sphere is intact and the solenoid is likely defaulting correctly to the firm position.
* **2. Planned DIY Scope (Mechanical)**
  * **Front Axle:** Replace Lower Control Arms (LCA) as complete units (includes bushings and ball joints).
  * **Rear Axle:** Replace 5-link suspension set (8 links total) and outer "Squeak Bushings" (Carrier Support Joints).
  * **Steering:** Replace Steering Damper and Idler Arm Bushing to eliminate "slop."
  * **ADS Components:** Inspect/Replace Strut Mounts and Dust Boots. Replace Nitrogen Accumulators (Spheres) if ride becomes "pogo-like" after clearing codes.
* **3. Essential Tooling & Safety**
  * **Spring Compressor:** Must use Internal Telescopic Coil Spring Compressor (Mercedes-specific). Standard external clamps are prohibited due to safety risk.
  * **Torque Protocol:** All bushing bolts must be torqued at static ride height (wheels on ground/ramps) to prevent premature rubber shear.
  * **ADS Protection:** Disconnect Level Sensor Linkage Rods before lowering control arms to prevent breakage of brittle plastic sensors.
* **4. Ride Height Checkpoints**
  * Factory ride height for a 500 SL varies slightly by VIN and spring pad choice, but the standard benchmark for a level car is:
    
    | Location | Measurement Point | Target Value (approx.) |
    | :--- | :--- | :--- |
    | **Front** | Wheel Arch to Center of Hub | ~380mm - 390mm |
    | **Rear** | Wheel Arch to Center of Hub | ~375mm - 385mm |
    | **Visual** | Tire to Arch Gap | roughly equal (approx. 2-2.5 fingers) |

  * *Note:* If the rear is significantly lower, **FIRST check the hydraulic level control:** (a) reservoir fluid level in engine bay, (b) rear level control linkage integrity (anti-roll bar to proportioning valve — known plastic shear point). Only if hydraulic system is confirmed intact, check the Spring Pads (nubs 1 through 4) for incorrect thickness.
* **5. Next Diagnostic Steps**
  * **ADS Code Extraction:** Use a blink-code reader on Pin 9 of the 16-pin Diagnostic Connector. *(See project: [ADS Blink-Code Reader](../work/ads_blink_reader/README.md))*
  * **Warning Lamp Restoration:** Reinstall the ADS bulb in the instrument cluster to confirm system communication.
  * **Hydraulic Flush (Phase 6.0 — PRIORITY):** Full system flush with ZH-M fluid (4L), replace suction filter (A 129 327 00 91). This is the diagnostic test that determines if the tandem pump ADS section is alive. Procedure documented in `work/ads_diagnostic/README.md` Phase 6.0. **Do this BEFORE any mechanical suspension work.**

### **5. Central Locking (PSE) Inoperative**
* **Symptom:** Central locking system does not work. There is no sign of life from the vacuum pump; locks only operate manually.
* **Initial Assessment:** The PSE (Pneumatic System Equipment) pump is located under the right rear storage compartment. Since it is completely silent, it's likely an electrical issue (blown fuse, dead pump motor, or bad connection) rather than just a vacuum leak.
* **Action Item:** Investigate PSE pump and system. *(See project: [PSE Central Locking](../work/pse_central_locking/README.md))*

### **6. Engine Bay Maintenance (Intake, Filters & Fluids)**
* **Observation (March 17, 2026):** Checked engine bay during garage storage (cold engine, 10-15°C).
  * **Intake Hoses:** Passenger side intake hose is worn with holes in the flexible/thin section.
  * **Metal Cylinder (Front of engine):** Fluid level is just below the minimum line and very dark.
  * **Plastic Reservoir (Next to washer fluid):** Fluid level was below MIN on 2026-03-17, and dropped only ~0.5cm by 2026-03-23. **CONFIRMED (2026-03-23): This IS the ADS/Niveauregulierung hydraulic fluid reservoir** (not coolant). MAX/MIN markings are deep inside canister (hard to read — led to initial "almost empty" misread). No active leak found. Fluid loss is gradual/historical. Fluid: MB 343.0 / ZH-M (clear/amber). Top up to MAX and monitor.
* **Diagnosis:**
  * **Intake Hoses:** Brittle plastic/rubber hoses are a known M119 wear item. Vacuum leaks here bypass the MAF and allow unfiltered air.
  * **Metal Cylinder = Power Steering Pump Reservoir:** Sits directly behind the distributor on the front left (driver side) of the engine. Dark fluid means the old ATF/hydraulic fluid is oxidized and needs changing. Inside this canister, under the spring, is a replaceable paper filter. Note: on some R129s the ADS may share the power steering hydraulic circuit (Zentralhydraulik). If no separate ADS reservoir exists, this metal canister may serve both systems.
  * **Plastic Reservoir = CONFIRMED ADS/Niveauregulierung Hydraulic Fluid Reservoir:** Situated on the front right (passenger) side, next to the washer fluid. ~~Originally identified as coolant expansion tank (2026-03-17).~~ **CONFIRMED 2026-03-23:** This is the ADS hydraulic reservoir. Level is below MIN but stable (only ~0.5cm drop over 6 days, no active leak). Fluid is MB 343.0 / ZH-M (clear/amber). The coolant expansion tank is a separate container. **Top up to MAX with Febi 02615 and monitor.**
* **Action Items:**
  * **Air Intake & Filters:** Replace both left and right intake hoses entirely. Perform an engine air filter replacement (Left/Right) while the airbox is open.
  * **Power Steering Flush:** Syringe out old fluid, replace the internal reservoir filter (Part No. `A 000 466 21 04`), and refill/flush with MB 236.3 spec fluid (or equivalent approved ATF). *(See project: [Power Steering Flush](../work/power_steering_flush/README.md))*
  * **Coolant Top-up:** Top up the expansion tank to the cold fill line using a 50/50 mix of distilled water and MB 325.0 spec coolant (e.g., Glysantin G48/Blue-Green). Monitor for slow leaks.
* **Parts Needed:**
  * Right Intake Hose (Passenger Side): A 119 094 01 82
  * Left Intake Hose (Driver Side): A 119 094 00 82
  * Engine Air Filter Set (Left & Right)
  * Power Steering Filter: A 000 466 21 04
  * MB 236.3 Power Steering Fluid (1-2 Liters)
  * MB 325.0 Spec Coolant (Glysantin G48)
* **Sourcing:** MB-osat (primary source), Autodoc.fi, or local Kärkkäinen/Motonet for fluids.

### **8. Hood Insulation Pad Replacement**
* **Symptom:** The original hood pad has been completely removed by a previous owner, leaving behind a mess of hardened, baked-on factory adhesive. This risks heat damage to the exterior aluminum hood paint and increases engine noise.
* **Part Ordered (2026-03-22):** IPG-87742-Set — Insulation mat including test sticker & fastening clips for Mercedes R129 hood. Supplier: AMS Auto GmbH (Gevelsberg, DE) via oldtimer-Ersatzteile24.de. Invoice #566371, €93.80 incl. shipping. Paid via PayPal. ETA 2026-03-28 (DHL EU Parcel, tracking: CS743796387DE).
* **Action Item:** Safely dissolve and remove the old adhesive without scratching the aluminum, then install the new pad. *(See project: [Hood Pad Replacement](../work/hood_pad_replacement/README.md))*

### **9. Baseline Service — Unknown History (Spring 2026)**

*No written service history exists for this vehicle. Assume all consumables and wear items are overdue. This checklist establishes a known-good baseline for reliability and longevity. Items already tracked in detail elsewhere are cross-referenced, not duplicated. Full working document with detailed instructions: [work/baseline_service/README.md](../work/baseline_service/README.md)*

#### **A. Engine Oil & Filtration**
- [ ] **Engine Oil & Filter Change** — Drain and refill with MB 229.5 spec fully-synthetic (e.g., Mobil 1 0W-40 or Liqui Moly 5W-40). Replace oil filter (use OEM Mann/Mahle). Capacity: ~8L.
- [ ] **Oil Filter Housing Cap** — Inspect the plastic cap for cracks when removing (requires 36mm socket). Replace if cracked.

#### **B. Ignition System (M119 Twin-Distributor)**
- [ ] **Spark Plugs** — Replace all 8 (Bosch W5DTC or equivalent copper-core, OEM spec for KE-Jetronic M119). Gap to 0.8mm.
- [ ] **Distributor Caps & Rotors (×2)** — Replace both left and right distributor caps and rotors. Inspect for carbon tracking and corrosion.
- [ ] **Spark Plug Wires** — Inspect resistance (should be <10 kΩ per wire). Replace full set if any are out of spec or brittle.

#### **C. Fuel System**
- [ ] **Fuel Filter / Polttoainesuodatin** (MANN **WK 830/3** or Bosch `0 450 905 273`. OEM Part: `A 002 477 30 01`)
- [ ] **Fuel Accumulator** — Inspect (holds residual pressure for hot restart). If hard-start when hot, replace.

#### **D. Drive Belts**
- [ ] **Serpentine / V-Belts** — Inspect all belts for cracking, glazing, and tension. The M119 uses multiple V-belts (not a single serpentine). Replace the full set if age/condition is unknown.
- [ ] **Belt Tensioners & Idler Pulleys** — Check for bearing play/noise. Replace any that are rough.

#### **E. Cooling System**
- [ ] **Full Coolant Flush** — Drain, flush, and refill with MB 325.0 spec (Glysantin G48, 50/50 mix). *(Top-up already noted in Task #6; this upgrades it to a full flush.)*
- [ ] **Thermostat** — Replace (known M119 failure point, causes overcooling or overheating). OEM temp: 80°C.
- [ ] **Coolant Hoses** — Inspect all rubber hoses for swelling, cracking, and softness. Replace any suspect hoses (prioritize the lower radiator hose and heater hoses).
- [ ] **Radiator Cap** — Replace (cheap insurance; a weak cap lowers boiling point).

#### **F. Transmission (722.3)**
- [ ] **ATF Drain & Fill** — Drain and refill with MB 236.1 spec ATF. The 722.3 does not have a serviceable filter; fluid change is the maintenance item. Capacity: ~5L per drain cycle (do 2–3 drain-and-fill cycles for a near-complete exchange).
- [ ] **Transmission Mount** — Inspect for sagging/cracking. Replace if collapsed (causes drivetrain vibration).

#### **G. Brakes**
- [ ] **Brake Fluid Flush** — Complete flush with DOT 4+ (MB 331.0 spec). Brake fluid is hygroscopic; assume it hasn't been changed in years. Bleed all four corners (RR → LR → FR → FL).
- [ ] **Brake Pad Inspection** — Measure remaining pad thickness (front & rear). Replace if <3mm.
- [ ] **Brake Disc Inspection** — Check for scoring, lip, and minimum thickness markings. Measure with a micrometer.
- [ ] **Brake Hoses (×4)** — Inspect all four rubber flex hoses for cracking, swelling, or sponginess. Replace if any doubt (35-year-old rubber).

#### **H. Engine Mounts & Drivetrain Mounts**
- [ ] **Engine Mounts (×2)** — Replace both fluid-filled mounts. Collapsed mounts cause idle vibration and allow excess engine movement. *(Already noted in Master Plan Phase 4.)*
- [ ] **Transmission Mount** — See section F above.

#### **I. Electrical Baseline**
- [ ] **Battery (PRIORITY — observed drain)** — Test CCA and internal resistance. Battery age unknown. Observed ~1V drop (13V→12V) over ~2 days idle. Replace if CCA is marginal. Nordic winters are brutal on old batteries.
- [ ] **Parasitic Draw Test** — If battery tests healthy, measure resting current draw with ammeter in series on negative terminal (engine off, all doors closed, wait 30min for modules to sleep). Normal: <50mA. If high, pull fuses one by one to isolate the draining circuit. Suspects: PSE pump circuit (dead but powered?), ATA/IRCL modules (static glow on X11 = powered), aftermarket Sony CDX-410 radio wiring, stuck relay.
- [ ] **Alternator Output** — Verify 13.8–14.4V at idle with loads on. Check for AC ripple (indicates failing diodes).
- [ ] **All Exterior Lights** — Walk-around test: headlights (low/high), fog lights, turn signals, brake lights, reverse lights, license plate lights, side markers.
- [ ] **Fuse Box Inspection** — Open both fuse boxes (underhood + interior). Inspect for corrosion, melted terminals, and incorrect fuse ratings.

#### **J. Vacuum System**
- [ ] **Vacuum Lines** — The M119 KE-Jetronic relies heavily on vacuum. Inspect all rubber vacuum lines for cracks and hardening. Replace any brittle lines with silicone vacuum hose.
- [ ] **Idle Speed Check** — After addressing vacuum leaks (including intake hoses from Task #6), verify idle speed settles at ~650–700 RPM in Drive with A/C off.

#### **K. Rubber, Seals & Weatherstripping**
- [ ] **Door Seals** — Inspect and treat with rubber conditioner (Gummi Pflege). Check for tears or compression set.
- [ ] **Soft Top Seals** — Inspect the roof seals and rear window seal for leaks and hardening. Treat with conditioner.
- [ ] **Trunk Seal** — Inspect (water ingress to the trunk is common on R129s and can damage the PSE pump area).
- [ ] **Antenna Grommet / Antennin kumitiiviste** — Replace the rubber seal where the power antenna meets the rear fender. A cracked seal allows water to drip directly down onto the PSE (central locking) pump in the trunk! (OEM Parts: Upper `A 129 827 02 98`, Lower `A 129 827 03 98`).

#### **L. Under-Car Visual Inspection**
- [ ] **Exhaust System** — Inspect for rust-through, loose hangers, and leaks. Pay attention to the flex joints and catalyst connections.
- [ ] **Fluid Leaks** — Put clean cardboard under the car overnight. Map any drips (oil, ATF, PS fluid, coolant).
- [ ] **Underbody Rust** — Inspect floor pans, subframe, and rear wheel arches for corrosion.

#### **Cross-References (Already Tracked)**
* Air Intake Hoses & Engine Air Filters → Task #6
* Power Steering Flush & Filter → Task #6
* Coolant Top-up → Task #6 (upgraded to full flush above)
* Engine Mounts & Steering Damper → Master Plan Phase 4
* Suspension Refresh (LCA, Links, Bushings) → Task #4
* ADS Diagnostics → Task #4 / [ADS Blink-Code Reader](../work/ads_blink_reader/README.md)

## **💰 Budget & Parts Cost Tracking (2026)**

*Target: Keep total parts and service costs (excluding tools/equipment) near €5,000 for the 2026 restoration phase.*

| Date | Category | Item | Supplier | Cost (€) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-03-22 | Filters | MANN Engine Air Filters (C 3388) x2 | Autodoc | 34.00 | Purchased |
| 2026-03-22 | Filters | MANN Cabin Filter (CU 5041) | Autodoc | 14.00 | Purchased |
| 2026-03-22 | Filters | MANN Oil Filter (H 829/1 x) | Autodoc | 11.00 | Purchased |
| 2026-03-22 | Filters | MANN Power Steering Filter (H 85) | Autodoc | 6.00 | Purchased |
| 2026-03-22 | Filters | MANN Fuel Filter (WK 830/3) | Autodoc | 22.00 | Purchased |
| 2026-03-22 | Ignition | NGK Spark Plugs BP5ES x8 | Autodoc | 24.00 | Purchased |
| 2026-03-22 | Fluids | ATE TYP200 DOT4 Brake Fluid (1L) | Autodoc | 15.00 | Purchased |
| 2026-03-22 | Fluids | Febi ZH-M Hydraulic Fluid (1L) | Motonet | ~15.00 | Purchased |
| 2026-03-22 | Fluids | Febi ATF MB 236.3 Power Steering (1L) | Motonet | ~15.00 | Purchased |
| 2026-03-22 | Fluids | Coolant (Motox G11) + Distilled Water | Motonet | ~35.00 | Purchased |
| 2026-03 | Body | Ceramic Torpedo Fuses | Motonet | ~10.00 | Purchased |
| 2026-03-18 | Audio | Mercedes Special BE2210 Radio (w/ AUX) | Online Retailer | 434.97 | Purchased |
| 2026-03-20 | Wheels/Tires | Michelin PS2 275/40R17 (Rear x2) | Online Retailer | 981.99 | Purchased |
| 2026-03-20 | Wheels/Tires | Michelin PS5 245/45R17 (Front x2) | Online Retailer | 368.37 | Purchased |
| 2026-03-22 | Drivetrain | Corteco Engine Mounts x2 (80001913) | Autodoc | 90.98 | Purchased |
| 2026-03-22 | Drivetrain | Corteco Trans Mount (21652116) | Autodoc | TBD | Purchased |
| 2026-03-22 | Body | Hood Insulation Pad + Clips (IPG-87742-Set) | AMS Auto (DE) | 73.90 | Purchased |
| 2026-03-22 | Body | Shipping (DHL EU Parcel) | AMS Auto (DE) | 19.90 | Purchased |
| 2026-03-16 | Insurance | Liikennevakuutus + Full Kasko | Pohjola | — | Active |
| 2026-03-27 | Admin | Autovero (car import tax) | Verohallinto / OmaVero | 837.05 | Pending payment |
| **Total** | | **Year-to-Date Spend (parts + tax)** | | **~€3,008.16 + TBD** | |

*(Note: Estimated prices used for Motonet local purchases; will update with exact receipts. Insurance premium excluded from total (recurring cost). Electronics/hobby add-ons like Raspberry Pi, Owon oscilloscope, or custom displays are excluded from this vehicle maintenance budget.)*

## **🛠️ Tool Acquisition & Inventory**

*Transitioning from basic 1970s VW Beetle tools to a metric, precision toolset required for the M119 V8 and complex R129 chassis mechanics. Focus on high-quality, B2B-grade European brands to prevent rounding off 34-year-old fasteners.*

**📍 The Local Oulu Advantage:** Kärkkäinen in Oulu serves as a massive local asset, carrying extensive stock of premium brands (Wera, Knipex, Bahco) directly off the shelf, eliminating the need to haul heavy tools from Helsinki. There is also Motonet, MB-Osa, Puuilo, Biltema etc nearby.

### **1\. General Hand Tools**
* **Sockets & Ratchets:** Bahco S910 & SBSL25 sets (Acquired)
* **Wrenches:** Bahco Combination Wrenches (Acquired)
* **Hex & Torx:** Bondhus Torx Set, Wera Hex-Plus (Acquired)
* **Pliers:** Knipex Cobra, Diagonal Cutters, Needle-Nose (Acquired)

### **2\. Specialty & Electrical Tools**
* **36mm Socket:** Specifically for removing the M119 oil filter housing cap without cracking the plastic.
* **Torque Wrenches:** Essential for the aluminum M119 block. Need a 3/8" drive (approx. 20-100 Nm) and a 1/2" drive (up to 200 Nm for wheel bolts). (Acquired)
* **Multimeter & Oscilloscope:** Owon HDS242 required for troubleshooting the ADS system and developing the Phase 2/3 Raspberry Pi/Nordic PCB circuits. (Acquired)

## **📚 Digital Documentation & Manuals**

*A curated repository of essential PDF manuals, wiring diagrams, and guides for the 1991 R129.*

### **1\. Official Owner's Manuals**

* **1990/1991 Mercedes-Benz 300 SL & 500 SL Owner's Manual (English PDF):**  
  * *Link:* [r129-owners-manual-1990.pdf (mb.clifton.io)](https://mb.clifton.io/downloads/r129-owners-manual-1990.pdf)  
  * *Use:* General operation, fuse locations, manual soft-top override procedures, and fluid specifications.

### **2\. Specialist Repair Guides**

* **Top Hydraulics \- R129 Soft Top System:**  
  * *Link:* [Top Hydraulics R129 Instructions](https://www.tophydraulics.com/)  
  * *Use:* The absolute bible for R129 roof mechanics. Contains step-by-step PDF guides with photos for accessing, removing, and installing all 11 hydraulic roof cylinders and the windshield latches.

### **3\. Community Knowledge Bases & Wiring**

* **The Brian Clifton R129 Archive:**  
  * *Link:* [The Mercedes-Benz R129 SL Archive](https://mb.clifton.io/r129/)  
  * *Use:* A massive repository of R129 literature, radio manuals (Becker), and historical articles.  
* **BenzWorld R129 Forum:**  
  * *Link:* [BenzWorld R129 SL-Class](https://www.google.com/search?q=https://www.benzworld.org/forums/r129-sl-class.26/)  
  * *Use:* The primary source for deep-dive technical troubleshooting, specifically regarding the ADS blink-code reader builds and KE-Jetronic diagnostics.  
  * https://www.benzworld.org/threads/all-of-the-r129-pdfs-i-have-collected-over-the-years.3099517/

*(Note: The official 8,000-page "STAR Classic Service Manual Library" for the R129 is often required for deep electrical teardowns. Physical DVD copies or community-hosted files should be sourced for Phase 5 electrical integration).*