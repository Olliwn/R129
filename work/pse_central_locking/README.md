# PSE Central Locking Investigation

## Overview
The central locking system on the 1991 Mercedes-Benz R129 500 SL is completely silent and inoperative. The locks currently only operate manually. This project documents the investigation and repair of the Pneumatic System Equipment (PSE) that controls the central locking, orthopedic seats (if equipped), and climate control vacuum reservoirs.

## Symptoms
- No audible sound from the PSE pump when actuating physical locks.
- Central locking does not engage/disengage from either door or the trunk.

## Known Architecture
- The PSE (Pneumatic System Equipment) pump is located under the right-side storage compartment (behind the passenger seat).
- It operates based on electrical signals from the door and trunk lock actuators.
- A completely silent pump usually indicates a loss of power, a blown fuse, a burned-out pump motor, or a failed internal control module. A vacuum leak would typically result in the pump running excessively before timing out.

## Diagnostic Steps / Action Plan

1. **Verify Fuses:**
   - Check the primary fuse for the central locking system in the main fuse box (trunk location for R129, specifically check the fuse assignment index for the PSE pump).
   - Inspect for any blown or heavily oxidized aluminum fuses. Replace with brass/copper core fuses if they are oxidized.

2. **Access the PSE Pump:**
   - Remove the right rear storage compartment liner.
   - Extract the PSE pump from its foam noise-isolation casing.

3. **Electrical Testing at the Pump:**
   - Disconnect the main wiring harness from the pump.
   - Use a multimeter to verify +12V constant power and a good ground at the main supply pins.
   - Test the trigger pins (from the doors/trunk): manually actuate a door lock and verify the signal voltage changes at the connector.

4. **Pump Motor Bench Test:**
   - If power and signals are present but the pump is silent, carefully open the PSE pump casing.
   - Check the internal circuit board for burned traces or cold solder joints (common on ancient modules).
   - Apply 12V directly to the internal motor leads to see if the carbon brushes/motor are completely dead.

## Log / Notes
*Notes from investigation procedures will be documented here.*
