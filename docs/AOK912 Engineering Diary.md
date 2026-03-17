# **📖 AOK912 \- Engineering & Maintenance Diary**

**Vehicle:** 1991 Mercedes-Benz 500 SL (R129)

**Engine:** M119.960 V8 (32V, KE-Jetronic)

**Transmission:** 722.3 (4-Speed Automatic)

**Chassis:** Adaptive Damping System (ADS) Equipped

## **📅 Log Entries**

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
* **Diagnostics (Ferry Transit):** Noticed ADS dashboard warning light is completely dead (no dead-fronting outline visible). Suspect a previous owner removed the bulb to hide a system fault. Also noted the pneumatic central locking (PSE) is completely silent and inoperative.

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
*   **Electronics & Prototyping Haul (DigiKey):** Placed a comprehensive order for the UI controls, interface circuits, and project prototyping.
    *   **Controls & Haptics:** ALPS Directional Switch/Encoder (RKJXT1F42001) paired with the Kilo International (OEDNI-90-4-7) matte black machined-aluminum knob for that solid, premium OEM "iDrive" feel.
    *   **Interface ICs & Signal Processing:** CD74HC4051E (8-channel Analog Multiplexer), ADS1115 (16-bit 4-channel ADC for precision analog reading), TXB0108 (Level Shifter Breakout) for logic conversion between 3.3V and 5V.
    *   **Power Supply Design:** Sourced a mix of efficient Murata switching converters (5V/8W and 3.3V/5W OKI-78SR series) alongside traditional LDO regulators (LM2940T 5V, LD1117 3.3V) for clean power rails.
    *   **Op-Amps & Sensing:** LM358P (General Purpose Op-Amps) and INA169 (Current Monitors) to interpret analog automotive signals.
    *   **Protection Circuitry:** 1.5KE18A TVS Diodes (critical for surviving 12V automotive load dumps) and assorted Schottky/Standard Diodes (1N5819, 1N4148, 1N4007) for reverse-polarity protection.
    *   **Prototyping Essentials:** Multiple breadboards, pluggable terminal blocks, jumper wires, pin headers, and SparkFun capacitor & resistor kits.
*   **Diagnostic Tools:** Ordered an **Owon HDS242 Handheld Oscilloscope**. An absolutely essential tool for analyzing CAN/LIN signals, noisy automotive sensors, and verifying the Phase 2 PCB logic timings while in the garage.

## **📝 Task / Todo List & Quick Studies**

### **1. Windshield Wiper Parking Issue**
* **Symptom:** Wipers do not consistently park in the correct resting position when turned off.
* **Quick Study on Likely Causes:**
  * **Relay/Module Failure:** The N10 combination relay module (or K26 relay) frequently fails or gets dirty contacts, causing incorrect park detection. The internal park sensor contacts inside the wiper motor assembly could also be faulty.
  * **Mechanical Misalignment:** Loose or slipped nuts on the wiper mechanism linkage. The mechanism may need physical realignment to correct the resting blade position.
  * **Motor/Mechanism Binding:** The complex eccentric 'jumping' mono-wiper mechanism is notorious for needing periodic lubrication (under the plastic turtle-shell cover). A binding mechanism can stress the motor, slow it down, and cause erratic parking.
* **Action Item:** Lubricate the mechanism first (easiest fix), check linkage nuts, and if the issue persists, investigate the N10 relay and motor park contacts.

### **2. Washer Fluid Nozzles**
* **Symptom:** Fluid only spraying from 2 of 4 nozzles.
* **Action Item:** Clean and unclog the windshield washer nozzles. Inspect the fluid lines for cracks or leaks.

### **3. Paint Inspection (Rear Fender)**
* **Symptom:** Narrow cracks visible in the paint on the rear fender (upward-facing area just below the trunk lid) when wet and dirty.
* **Action Item:** Thoroughly wash and inspect the area once the weather improves to determine the depth/severity of the cracking and plan for potential paint correction or preservation.

### **4. Suspension Refresh (ADS & Mechanical)**
* **Engineering Record: 1991 Mercedes-Benz R129 500 SL**
* **1. Vehicle Baseline & Current Status**
  * **Model:** 1991 500 SL (R129) with ADS I (Adaptive Damping System).
  * **Observed Symptoms:** 
    * Rear ride height is low (1-2 finger gap) vs. Front (3 finger gap).
    * ADS Lift Switch is non-functional.
    * ADS Warning Lamp likely disabled/removed by previous owner.
    * System likely in "Limp/Safe Mode" (Defaulted to maximum stiffness).
  * **Mechanical Condition:** Nitrogen Accumulators (Spheres) passed the "Bounce Test" (system is firm but not "rock hard" or bouncing/oscillating), suggesting diaphragms are currently intact.
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

  * *Note:* If the rear is significantly lower, check the Rear Level Control Valve linkage for adjustment or the Spring Pads (nubs 1 through 4) for incorrect thickness.
* **5. Next Diagnostic Steps**
  * **ADS Code Extraction:** Use a blink-code reader on Pin 9 of the 16-pin Diagnostic Connector. *(See project: [ADS Blink-Code Reader](../work/ads_blink_reader/README.md))*
  * **Warning Lamp Restoration:** Reinstall the ADS bulb in the instrument cluster to confirm system communication.
  * **Hydraulic Flush:** Plan for a full system flush with Pentosin/ZH-M fluid and a 10-micron filter replacement following mechanical work.

### **5. Central Locking (PSE) Inoperative**
* **Symptom:** Central locking system does not work. There is no sign of life from the vacuum pump; locks only operate manually.
* **Initial Assessment:** The PSE (Pneumatic System Equipment) pump is located under the right rear storage compartment. Since it is completely silent, it's likely an electrical issue (blown fuse, dead pump motor, or bad connection) rather than just a vacuum leak.
* **Action Item:** Investigate PSE pump and system. *(See project: [PSE Central Locking](../work/pse_central_locking/README.md))*

### **6. Engine Bay Maintenance (Intake, Filters & Fluids)**
* **Observation (March 17, 2026):** Checked engine bay during garage storage (cold engine, 10-15°C).
  * **Intake Hoses:** Passenger side intake hose is worn with holes in the flexible/thin section.
  * **Metal Cylinder (Front of engine):** Fluid level is just below the minimum line and very dark.
  * **Plastic Reservoir (Next to washer fluid):** Fluid level is just below the minimum line and clearer in color. 
* **Diagnosis:**
  * **Intake Hoses:** Brittle plastic/rubber hoses are a known M119 wear item. Vacuum leaks here bypass the MAF and allow unfiltered air.
  * **Metal Cylinder = Power Steering/SLS Pump Reservoir:** Sits directly behind the distributor on the front left (driver side) of the engine. Dark fluid means the old ATF/hydraulic fluid is oxidized and needs changing. Inside this canister, under the spring, is a replaceable paper filter. 
  * **Plastic Reservoir = Engine Coolant Expansion Tank:** Situated on the front right (passenger) side. Since it's cold, the coolant has contracted, but being below the minimum line requires a top-up to prevent air induction.
* **Action Items:**
  * **Air Intake & Filters:** Replace both left and right intake hoses entirely. Perform an engine air filter replacement (Left/Right) while the airbox is open.
  * **Power Steering Flush:** Syringe out old fluid, replace the internal reservoir filter (Part No. `A 000 466 21 04`), and refill/flush with MB 236.3 spec fluid (or equivalent approved ATF). 
  * **Coolant Top-up:** Top up the expansion tank to the cold fill line using a 50/50 mix of distilled water and MB 325.0 spec coolant (e.g., Glysantin G48/Blue-Green). Monitor for slow leaks.
* **Parts Needed:**
  * Right Intake Hose (Passenger Side): A 119 094 01 82
  * Left Intake Hose (Driver Side): A 119 094 00 82
  * Engine Air Filter Set (Left & Right)
  * Power Steering Filter: A 000 466 21 04
  * MB 236.3 Power Steering Fluid (1-2 Liters)
  * MB 325.0 Spec Coolant (Glysantin G48)
* **Sourcing:** MB-osat (primary source), Autodoc.fi, or local Kärkkäinen/Motonet for fluids.

## **🛠️ Tool Acquisition & Inventory**

*Transitioning from basic 1970s VW Beetle tools to a metric, precision toolset required for the M119 V8 and complex R129 chassis mechanics. Focus on high-quality, B2B-grade European brands to prevent rounding off 34-year-old fasteners.*

**📍 The Local Oulu Advantage:** Kärkkäinen in Oulu serves as a massive local asset, carrying extensive stock of premium brands (Wera, Knipex, Bahco) directly off the shelf, eliminating the need to haul heavy tools from Helsinki.

### **1\. Core Ratchets & Sockets (1/4", 3/8", 1/2" Drive)**

* **Primary Target:** **Proxxon Industrial** (Comprehensive set in green steel case). Industry standard for European mechanics.  
* **Alternative:** **Bahco S106** or **Bahco S138** (Excellent durability, widely available at Kärkkäinen and Motonet).

### **2\. Hex (Insex) & Torx Keys**

* ![][image2]**Primary Target:** **Wera Hex-Plus** (Color-coded L-Key set). Available at Kärkkäinen.  
* *Engineering Note:* Wera's patented Hex-Plus profile grips the flats of the bolt rather than the corners. Absolutely mandatory to prevent stripping seized hex bolts on the M119 distributor caps, valve covers, and engine trim.

### **3\. Screwdrivers**

* **Primary Target:** **Wera Kraftform Plus** (with Laser-tip for extreme grip) or **Bahco Ergo**.  
* **Requirement:** Full set of Slotted and Phillips/Pozidriv.

### **4\. Pliers & Cutters**

* **Primary Target:** **Knipex** (No compromises here, available at Kärkkäinen).  
* **Specific Models Needed:**  
  * *Knipex Cobra:* High-tech water pump pliers for chassis work and seized linkages.  
  * *Knipex Diagonal Cutters (Sidavbitare):* For wiring and zip-ties.  
  * *Knipex Needle-Nose (Spetstång):* Essential for vacuum lines and the Phase 2 electronics project.

### **5\. Combination Wrenches (Spanners)**

* **Primary Target:** **Bahco** or **IKH Pro Series**.  
* **Requirement:** Metric sizes from 8mm up to 24mm. Long handles preferred for suspension leverage (vital for future ADS accumulator replacement).

### **6\. Specialty & Electrical Tools (To acquire later)**

* **36mm Socket:** Specifically for removing the M119 oil filter housing cap without cracking the plastic.  
* **Torque Wrenches:** Essential for the aluminum M119 block. Need a 3/8" drive (approx. 20-100 Nm) and a 1/2" drive (up to 200 Nm for wheel bolts).  
* **Multimeter:** High-quality unit (e.g., Fluke 107 or Brymen) required for troubleshooting the ADS system and developing the Phase 2/3 Raspberry Pi/Nordic PCB circuits.

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

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAAAyCAYAAADhjoeLAAACXklEQVR4Xu3asWoUURQG4NVOwUJRlGXdzCbBRUVESzstfAsbQbAQUYK+gKAWFlY2lqIIgpVtKpu0igRBqxQKliJIIETPXe+N12E229jt98Fh7jlnZtjyZ5JeDwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIFlYWHgWdbI9L2L3q9VfTLPhcLhRz/PuVdo1TfNwym6r3+/vb82vRn2NWq/nAABzLwLSz6iVHL5OtfdJ2tWBLYJYE/e+rPdd59FodDT6N127OP8o53jXlXjl9Wr3TzgEAKD3JyR1BbaYP4q6MS2U5X5zaWnp+JTdpI9A9jjOT6r5hajP9T3VTmADAGjbJbClYDUrsH2Mep6+vHXsJn26Rt0p87j1WL0r89LHb7lWzwAA5l4OSadbs+18nRXY3kV9irrUsdsJZfH+m2Ue54O7Bbaop/UMAGDupZA0GAzOVKO94/H4QN7NCmwfot4uLi6e6NjthLKmaW6Veb/fPzwjsN2rZwAAcy+FpNFodLbuo7ajNqO2cr9Zdn+fnPRfhsPh/Sm7Esq+1SGsDnddz8RvuVzPAADmXg5k59rzJOYv6lAV5/XBYHCo6nf7+jbp0/+sRb0v8wh4d2O3ku+Z/Om1aL8DAGCuRTh6nYJUDmzpi9pqa7+ad6nWqvkkVC0vLx+J8/cyjyD2IN53O583Itjtq58pu3Yoy/2euJ6vgx0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8H/8BjeprFvCYla5AAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,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>