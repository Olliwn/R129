# nRF5430 Interface Board: Breadboard Wiring Guides

Because CAD tools are redundant at the physical prototyping stage, this document provides explicit, row-by-row wiring instructions for assembling the hardware subsystems directly onto standard 400-tie or 830-tie breadboards.

---

## Guide 1: The Power Supply Build (Phase 2)
**Goal:** Convert raw, spiky 12V vehicle power down to an ultra-clean 3.3V logic supply, capable of surviving load dumps and reverse polarity.

**Required Components:**
*   1x Breadboard (e.g., SparkFun 08808)
*   1x 1N4007 Diode
*   1x 1.5KE18A TVS Diode
*   1x Murata OKI-78SR-5/1.5-W36-C (5V Buck Converter)
*   1x STMicroelectronics LD1117V33 (3.3V LDO Regulator)
*   Assorted Jumper Wires

### 1. Establishing the Rails
We will use the top and bottom power rails on the breadboard to route our three different voltage domains.
*   **Top Red Rail (+):** `12V_CLEAN` (Protected output from TVS diode)
*   **Bottom Red Rail (+):** `5V_BUS` (Output from Murata Buck)
*   **Bottom Blue/Black Rail (-):** `GND` (Star Point Ground for all DC returns)
*   **Top Blue/Black Rail (-):** `3.3V_LOGIC` (Output from the LDO, *Note: We are hijacking a ground rail to distribute the 3.3V logic power*)

### 2. Input Protection Stage
1.  **Raw 12V In:** Connect your 12V bench power supply positive clip directly to **Row 1, Column A**.
2.  **Raw GND In:** Connect your bench power negative clip directly to the **Bottom Blue/Black Rail (GND)**.
3.  **Reverse Diode (1N4007):**
    *   Insert the Anode (non-striped end) into **Row 1, Column B**.
    *   Insert the Cathode (striped end) into **Top Red Rail (12V_CLEAN)**.
    *(Now, the entire top red rail contains power protected from battery reversal).*
4.  **TVS Clamp (1.5KE18A):**
    *   Insert the Cathode (striped end) into **Top Red Rail (12V_CLEAN)**.
    *   Insert the Anode (non-striped end) into the **Bottom Blue/Black Rail (GND)**.
    *(Now, any voltage spike above 15V on the top red rail will be instantly shunted to ground).*

### 3. Step-Down Stage 1 (12V to 5V)
1.  **Murata OKI-78SR-5 Buck Converter:**
    *   Insert Pin 1 (+VIN) into **Top Red Rail (12V_CLEAN)**.
    *   Insert Pin 2 (GND) into **Bottom Blue/Black Rail (GND)**.
    *   Insert Pin 3 (+VOUT) into **Bottom Red Rail (5V_BUS)**.
    *(Now, the entire bottom red rail provides a very efficient 5V logic supply).*

### 4. Step-Down Stage 2 (5V to 3.3V Ultra-Clean)
1.  **LD1117V33 LDO Regulator:** (Assuming TO-220 package)
    *   Insert the regulator freely into the middle of the board, spanning **Row 15, Columns A, B, and C**.
    *   **Pin 1 (GND):** Jumper **Row 15, Col A** to **Bottom Blue/Black Rail (GND)**.
    *   **Pin 2 (VOUT):** Jumper **Row 15, Col B** to **Top Blue/Black Rail (3.3V_LOGIC)**.
    *   **Pin 3 (VIN):** Jumper **Row 15, Col C** to **Bottom Red Rail (5V_BUS)**.

### Testing Phase 2 Verification
Do not plug in the nRF5430 yet!
1.  Turn on your 14V bench supply.
2.  Use a multimeter to measure the **Bottom Red Rail**. It should read a stable `5.0V`.
3.  Measure the **Top Blue/Black Rail**. It should read a stable `3.3V`.
4.  If both are correct, the power subsystem is safe to power the delicate logic in Phase 3!

---

## Guide 2: Galvanic Isolation & Analog Front-End
*(Instructions to be drafted when you are ready to assemble Phase 3 on the second breadboard. Let me know when you reach this step!)*
