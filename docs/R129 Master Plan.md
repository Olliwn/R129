# **🏎️ R129 SL 500 (AOK912) \- The Master Action Plan**

**VIN:** WDB1290661F044414 | **Model Year:** 1991 (Pre-Eco Wiring) | **Engine:** M119 V8 | **Trans:** 722.3 (4-Speed)

**Current Status:** Safe in Helsinki. Swedish plates removed. Direct drive to Oulu planned for Sunday.

## **✅ PHASE 1, 2 & 3: Admin, Inspection & Transit (COMPLETED)**

* \[x\] Paperwork, Plates, Insurance, Vero Declaration all secured.  
* \[x\] M119 Engine, 722.3 Transmission, Hydraulics, and Chassis tested and approved.  
* \[x\] Ferry Transit: Kapellskär \-\> Naantali completed.  
* \[x\] **Swedish Deregistration:** Plates cut, photo sent to Vellinge Bilbolag. Original SWE registration papers requested via tracked mail to Oulu.

## **🏛️ PHASE 3.5: Post-Arrival Administration (CRITICAL)**

* \[ \] **Tax Declaration (Autoveroilmoitus):** Log into OmaVero and file the final tax declaration **within 5 days** of the initial declaration of use (Käyttöönottoilmoitus). Wait for the tax decision and the Swedish original papers before booking Katsastus.

## **🛠️ PHASE 4: Post-Purchase Bulletproofing (Oulu \- Spring 2026\)**

* \[ \] **Tires (PRIORITY 1):** Order and install **Continental PremiumContact 7** locally in Oulu (Wait until closer to driving season).  
* \[ \] **The ADS Mystery:** System confirmed in Failsafe (Rear did not rise on startup).  
  * *Diagnostic Step:* Check fluid levels and read the diagnostic blink-codes from the X11 port.  
* \[ \] **The Finnish Fueling Rule:** Exclusively use **98 Octane (E5)**.  
* \[ \] **Fluids Baseline:** Drain/fill the 722.3 transmission fluid. Change engine oil to high-quality synthetic. Flush ZH-M roof hydraulic fluid.  
* \[ \] **Engine Mounts & Steering Damper:** Replace the two fluid-filled V8 engine mounts, trans mount, and steering damper.

## **💻 PHASE 5: "Hybrid R129" Telematics & GUI Architecture (2026/2027)**

*Developing the distributed edge-node system for period-correct modernization.*

### **Phase 2.1: Power & Proximity Prototype (Desktop Development)**

* \[ \] **Hardware Acquisition:** Secure Raspberry Pi 5 & Display (Verkkokauppa). Secure Nordic Dev Board, MOSFETs, and UPS HAT.  
* \[ \] **Zephyr BLE Scanner:** Code the Nordic node to scan for the owner's smartphone MAC address with RSSI thresholding and hysteresis to prevent false triggers.  
* \[ \] **GPIO Trigger Logic:** Configure the Nordic node to trigger a GPIO pin (controlling the MOSFET) upon positive BLE identification.  
* \[ \] **Pi 5 Boot Optimization:** Configure the Pi 5 to boot from NVMe in \<15 seconds directly into a full-screen application.

### **Phase 2.2: Engine Sensor Node (Future)**

* \[ \] Remove battery from Nordic Thingy:53. Add RC filters for ADS1115. Mount inside F32 ECU box.

### **Phase 2.3: Retro GUI (Future)**

* \[ \] Develop PyQt/PySide6 UI using DIN 1451 font and amber VDO styling. Interface with EC11 rotary encoders.