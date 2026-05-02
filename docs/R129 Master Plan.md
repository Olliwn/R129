# **🏎️ R129 SL 500 (AOK912) \- The Master Action Plan**

**VIN:** WDB1290661F044414 | **Model Year:** 1991 (Pre-Eco Wiring) | **Engine:** M119 V8 | **Trans:** 722.3 (4-Speed)

**Current Status:** In Oulu. Swedish papers received. Autovero decision issued (€837.05). Liikennevakuutus active (Pohjola). **Next: pay autovero, get siirtolupa, book rekisteröintikatsastus.**

## **✅ PHASE 1, 2 & 3: Admin, Inspection & Transit**

* \[x\] Initial paperwork, plates, insurance, and declaration of use secured.  
* \[x\] M119 Engine, 722.3 Transmission, Hydraulics, and Chassis tested and approved.  
* \[x\] Ferry Transit: Kapellskär \-\> Naantali completed.  
* \[x\] **Transit Complete:** Car brought home to Oulu.  
* \[ \] **Swedish Deregistration:** Confirm with the Swedish dealer that the car has been avregistrerad in Sweden (photo of cut plates was sent). Avoid dual-country active registration.  
* \[x\] **Swedish Original Papers:** Both parts of the original Swedish registration papers received by mail in Oulu (2026-03-27).

## **🏛️ PHASE 3.5: Post-Arrival Administration (CRITICAL)**

* \[x\] **Tax Declaration (Autoveroilmoitus):** Filed in OmaVero within the required window.  
* \[x\] **Autovero Decision Received:** Verotusarvo €3,011 → Autovero **€837.05** (27.80%, CO2 238 g/km). Far below the ~€6,000 estimate.  
* \[x\] **Liikennevakuutus:** Active since 2026-03-16 (Pohjola, full kasko).  
* \[ \] **Pay Autovero & Get Rekisteröintilupa:** Pay €837.05 in OmaVero. Registration permit is issued after payment — required before ensirekisteröinti.  
* \[ \] **Siirtolupa (Transfer Permit):** Obtain temporary plates to legally drive to the katsastus station (Swedish plates are cut).  
* \[ \] **Rekisteröintikatsastus (Registration Inspection):** Book at a station in Oulu (K1 Limingantulli / A-Katsastus Oulunportti / Avainasemat). Car must be present for VIN verification. Bring: both parts of Swedish registreringsbevis (surrendered), besiktningsprotokoll 2026-01-02 (EU 2014/45 exemption for kunnon tarkastus), kauppakirja, ID, rekisteröintilupa, liikennevakuutustodistus.  
* \[ \] **Ensirekisteröinti:** At the katsastus station after passing. Receive Finnish plates.  
* \[ \] **Registration Timing Constraint:** Do not book tire installation until the car is registered, since it must be legal to drive.

## **🛠️ PHASE 4: Immediate Mechanical Priorities (Oulu \- Spring 2026\)**

* \[ \] **ADS Basic Diagnostics (PRIORITY 2):** Get at least basic diagnostic data from the car and confirm whether ADS is in safe/limp mode.  
  * *Low-risk first steps:* Check fluid levels and read the diagnostic blink-codes from the X11 port.  
* \[ \] **NRF5430 Bring-Up:** Hook the `nrf5430` into the car well enough to read at least basic diagnostic or sensor data.  
* \[ \] **Tires (PRIORITY 3, after registration):** Decide tire model, choose the shop in Oulu, and reserve an installation time only after Finnish registration is complete.  
  * *Current candidate:* **Continental PremiumContact 7** unless a better period-appropriate or comfort-focused option emerges.  
* \[ \] **Trusted Service Shop (PRIORITY 4):** Identify and reserve a slot at a trusted repair shop in Oulu that understands older `R129` cars.  
  * *Rule:* First investigate what can be safely handled DIY with low risk, then outsource the rest.  
* \[ \] **The Finnish Fueling Rule:** Exclusively use **98 Octane (E5)**.  
* \[ \] **Fluids Baseline:** Drain/fill the 722.3 transmission fluid. Change engine oil to high-quality synthetic. Flush ZH-M roof hydraulic fluid.  
* \[ \] **Engine Mounts & Steering Damper:** Replace the two fluid-filled V8 engine mounts, trans mount, and steering damper.

## **🤝 PHASE 4.5: Local Support Network**

* \[ \] **Join Local MB Club (PRIORITY 5):** Contact and join the nearby Mercedes-Benz club in Kempele.  
* \[ \] **Leverage Local Knowledge:** Ask for recommendations for trusted `R129` mechanics, parts sources, and common Oulu-area ownership tips.

## **💻 PHASE 5: "Hybrid R129" Telematics & GUI Architecture (2026/2027)**

*Developing the distributed edge-node system for period-correct modernization.*

### **Phase 5.1: Hardware Bring-Up & Shopping List**

* \[ \] **Shopping List Consolidation:** Finalize the current shopping list for tools, connectors, power components, and development hardware.  
* \[ \] **Core Hardware Status:** Continue work already started on the `nrf5430` and Raspberry Pi 5 onboard-computer stack.  
* \[ \] **Vehicle-Side Prototype Goal:** Move from bench setup to a minimal in-car prototype that can read useful live data.

### **Phase 5.2: Power & Proximity Prototype (Desktop Development)**

* \[ \] **Hardware Acquisition:** Secure Raspberry Pi 5 & Display (Verkkokauppa). Secure Nordic Dev Board, MOSFETs, and UPS HAT.  
* \[ \] **Zephyr BLE Scanner:** Code the Nordic node to scan for the owner's smartphone MAC address with RSSI thresholding and hysteresis to prevent false triggers.  
* \[ \] **GPIO Trigger Logic:** Configure the Nordic node to trigger a GPIO pin (controlling the MOSFET) upon positive BLE identification.  
* \[ \] **Pi 5 Boot Optimization:** Configure the Pi 5 to boot from NVMe in \<15 seconds directly into a full-screen application.

### **Phase 5.3: Engine Sensor Node (Future)**

* \[ \] Remove battery from Nordic Thingy:53. Add RC filters for ADS1115. Mount inside F32 ECU box. **Scope narrowed 2026-04-26** — engine-bay node now owns *only* under-hood-only signals (`X11` blink codes, `EHA`, airflow pot, lambda, engine-side `ECT`). Cabin-side signals are owned by Phase 5.5 below. See `docs/nRF5430_Interface_Design.md` and `docs/cabin_signal_survey.md`.

### **Phase 5.4: Retro GUI (Future)**

* \[ \] Develop PyQt/PySide6 UI using DIN 1451 font and amber VDO styling. Interface with EC11 rotary encoders.

### **Phase 5.5: Always-On Cabin Signal Node (Future, added 2026-04-26)**

* \[ \] **Always-on cabin signal node bring-up.** A small `nRF54L15` MCU (same family as the engine-bay node, single Nordic toolchain) mounted alongside the RPi5 in the front cubby, powered always-on from `F20_6` permanent 12 V via a low-Iq buck, wired to the Pi by USB-CDC. Acquires every cabin-side vehicle signal (cluster gauge senders + lamp drives, `VSS`, `TD` at cluster, brake-light feed, kickdown switch `S16/3`, reverse, hand-brake, `KL15`/`KL30`/`KL58`, console rocker switches, door / hood / trunk ajar) plus cabin ambient sensors (`BME280`, IMU, `TSL2591`). Reuses the engine-bay node's protection topology and most of its BOM. Survey + ownership table: `docs/cabin_signal_survey.md`. Bring-up plan and stage gates: `work/cabin_signal_node/README.md`.
* \[ \] **Sentry node folded in.** The previously planned standalone "always-on sentry" node is deleted as a separate device; its three responsibilities (BLE wake / Pi `5 V` high-side switch / IRCL→PSE keyless drive replacing the dead IR remote keys per `docs/known_issues.md`) are absorbed into this cabin node, which is already in the right place and already BLE-aware. One always-on Nordic MCU in the car instead of two.
* \[ \] **BLE proximity-based central locking.** Replaces the factory IR remote keys (one fob hardware-dead, the other rolling-code de-synced; MB Star re-pairing not cost-effective per the 2026-04-06 decision). Owner phone bonded to the cabin node; RSSI hysteresis controls lock / unlock pulses fed to a small **trunk-side PSE drive board** via one spare CAT6 pair on the existing passenger-side BE2210 trim run. Tap is *additive* on the IRCL→PSE wire so any future re-paired IR fob still works.
* \[ \] **Stage 0 gates (do during the Priority 3 cluster-pull window):** finalize the cabin pin-out by photographing the (non-`ADS`) instrument cluster connectors **and** identify the IRCL → PSE signal wire at the trunk IRCL controller (probe with a scope while actuating the working passenger-side mechanical key — its pulse mirrors the IRCL output). Both must complete before ordering the cabin MCU module and the trunk PSE drive board parts.