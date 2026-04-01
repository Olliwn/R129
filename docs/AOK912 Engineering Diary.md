# AOK912 -- Engineering & Maintenance Diary

**Vehicle:** 1991 Mercedes-Benz 500 SL (R129)

**Engine:** M119.960 V8 (32V, KE-Jetronic)

**Transmission:** 722.3 (4-Speed Automatic)

**Chassis:** ADS -- Niveauregulierung mit adaptivem Dämpfungs-System (Level Control with Adaptive Damping)

## Vehicle Data Card (Datakarte) / Manufacturing Plate
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

## Quick Links

| Document | Purpose |
|----------|---------|
| [Known Issues](known_issues.md) | Current state of all confirmed defects |
| [Active Tasks](tasks.md) | Work queue with priorities and links to work/ READMEs |
| [Budget](budget.md) | Parts and service cost tracking |
| [References & Tools](references.md) | Documentation links and tool inventory |
| [r129_data/SKILL.md](../r129_data/SKILL.md) | Technical data repository search instructions |

## Swedish Registration History

First registered 1991-09-26 at 0 km. 14 total owners. Latest inspection: 2026-01-02 at 139,970 km (Besikta Vellinge). Finnish registration pending (autovero paid 2026-03-27, awaiting rekisteröintilupa).

**Odometer analysis:** Smooth readings from 2013 onward (~340 km/year by 16-year previous owner). Cluster confirmed as non-ADS swap (no ADS symbol on indicator strip) -- swap occurred before 2013.

Source: [biluppgifter.se/fordon/AOK912](https://biluppgifter.se/fordon/AOK912). Full data in [diary/2026-03.md](diary/2026-03.md).

## Timeline

*Condensed summary. Full details in the monthly diary files.*

### [March 2026](diary/2026-03.md)

| Date | Summary |
|------|---------|
| Pre-purchase | Dealer restoration: new OEM soft top (~40k SEK), front bumper repaint, driver seat leather, interior trim. ADS/PSE/cluster issues undiscovered. |
| Mar 13 | **Purchase & 700km shakedown** (Vellinge → Kapellskär). Engine healthy, ride comfortable, missing cluster lamp noticed, PSE dead. |
| Mar 14 | **Finland arrival.** ADS confirmed in failsafe/limp mode (rear sag). Hybrid R129 project kickoff -- RPi5 + components from Verkkokauppa. |
| Mar 15 | **Helsinki → Oulu transit** (600km). Wiper park issue, washer nozzles, rear fender paint cracks noted. |
| Mar 17 | **UI architecture finalized.** RPi5 + 5.5" OLED cubby display + Alps encoder. DigiKey electronics order. Owon HDS242 oscilloscope ordered. |
| Mar 18 | **First blink-code diagnostics** (X11/4). ADS Pin 9: dim glow only (low voltage). SRS/EZL/RST/ESMC codes extracted and cleared. ATA/IRCL dead. Infotainment architecture documented. Michelin tires ordered (~€1,350). |
| Mar 21 | **First wash.** No-start resolved (loose battery terminal). Belt noise discovered. Wiper blade replaced. |
| Mar 22 | **Tool procurement** (Motonet/Puuilo, €548). Autodoc baseline service parts ordered. Datakarte decoded -- ADS (211) and heated seats (873) confirmed factory options. |
| Mar 23 | **ADS MODULE ALIVE** (1 blink at >13V). Console switch works. **European ADS I includes level control** (Niveauregulierung) -- corrects earlier US-manual assumption. **Cluster swap confirmed** (2026-03-26 photo: no ADS symbol). Fahrzeugniveau switch discovered and confirmed present. Reservoir below MIN. |
| Mar 27 | **Swedish papers received.** Autovero €837.05 paid. Finnish registration process unblocked. ADS code 14 (steering angle sensor). |
| Mar 28 | **ADS back online.** Code 14 cleared by lock-to-lock steering. Both switches functional. Fluid circulating, no leaks. Rear height still static. |
| Mar 29 | **Phase 1 flush & air-lock confirmed.** Baseline ride heights measured (rear 2-3cm low). 4L ZH-M flushed. ADS went offline mid-flush (diagnostic bus dim glow). BE2210 radio installed. Seat latch repaired. |
| Mar 30 | **OVP RELAY ROOT CAUSE FOUND.** 3-4 cracked solder joints (thermal fatigue on 87L pin). Explains all intermittent ADS behavior. Deliveries: hood pad, filters, mounts. Filters installed. **Rear fuse #6 blown** -- likely PSE root cause. All 8 torpedo fuses replaced. Electronics bay mapped. |
| Mar 31 | **OVP relay re-soldered** (Sn63/Pb37). Awaiting reinstall + test. **R129 technical data repository built** (150 PDFs curated, 110 ingested, 2,435 searchable chunks). |
