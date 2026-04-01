# AOK912 -- Active Tasks

**Vehicle:** 1991 Mercedes-Benz 500 SL (R129) | VIN: WDB 129066 1F 044414

*Work queue for open engineering and maintenance tasks. Detailed procedures live in the linked `work/` READMEs. Known issues are tracked separately in [known_issues.md](known_issues.md).*

---

## HIGH Priority

### 12. OVP Relay Reinstall + Test
Re-solder complete (2026-03-31). Reinstall OVP → reconnect battery → test Pin 9 → read/clear codes → verify both switches.
**Work plan:** [work/ads_diagnostic/README.md](../work/ads_diagnostic/README.md) Phase 0

### 13. Battery Health Verification
Measure internal resistance and cranking voltage drop (Owon HDS242). Varta H3, 100Ah, 890A CCA, manufactured Aug 2025. One deep discharge event. If CCA is marginal → replace at Motonet.
**Method:** V_oc vs V_load under high beams (target R_internal <25 mΩ). Cranking voltage must hold >10V.

### 10. M119 Upper Timing Components & Oil Bridge Clip Upgrade
Valve cover-off inspection of upper timing chain guides (plastic, brittle) and camshaft oil bridge clips (plastic, loosen). Upgrade clips to billet aluminum. Replace valve cover gaskets, breather hose, spark plugs.
**Work plan:** [work/m119_upper_timing/README.md](../work/m119_upper_timing/README.md)

### 14. Predictive Electronics Maintenance -- Capacitor & Solder Joint Audit
Prompted by OVP relay failure. Inspect/reflow solder joints and electrolytic capacitors in N4/1 (E-Gas), MAS (fuel pump), instrument cluster, and EZL (thermal paste refresh). See hit list with ranked priorities in [work/electronics_audit/README.md](../work/electronics_audit/README.md).

### 11. Baseline Service -- Unknown History
Full consumables flush: engine oil, ATF, brake fluid, coolant, power steering fluid. Filters, spark plugs, belts, hoses. 30-item checklist.
**Work plan:** [work/baseline_service/README.md](../work/baseline_service/README.md)

### 4. Suspension Refresh (ADS & Mechanical)
Front: replace LCA complete units. Rear: replace 5-link set + squeak bushings. Steering: replace damper + idler arm bushing. ADS: replace nitrogen accumulators if needed after OVP fix.
**Work plan:** [work/ads_diagnostic/README.md](../work/ads_diagnostic/README.md)

---

## MEDIUM Priority

### 5. Central Locking (PSE)
Fuse #6 replaced (2026-03-30). Awaiting test. If pump activates → resolved. If fuse blows → investigate short.
**Work plan:** [work/pse_central_locking/README.md](../work/pse_central_locking/README.md)

### 6. Engine Bay Maintenance (Intake, Filters & Fluids)
Air filters: DONE (2026-03-30). Remaining: replace intake hoses (L: A 119 094 00 82, R: A 119 094 01 82), power steering flush + filter, coolant top-up.
**Work plan:** [work/power_steering_flush/README.md](../work/power_steering_flush/README.md)

### 9. Center Console Refresh
Wood polish, switch cleaning/re-lubrication, RPi5 cable routing (AUX, CAT6, power). Three jobs, one disassembly.
**Work plan:** [work/center_console_refresh/README.md](../work/center_console_refresh/README.md)

### 8. Hood Insulation Pad Replacement
Part received (2026-03-30). Pending: remove old adhesive from aluminum hood, then install.
**Work plan:** [work/hood_pad_replacement/README.md](../work/hood_pad_replacement/README.md)

---

## LOW Priority

### 1. Windshield Wiper Parking Issue
Lubricate mechanism first, check linkage nuts, then investigate N10 relay.
**Work plan:** [work/wiper_system/README.md](../work/wiper_system/README.md)

### 2. Washer Fluid Nozzles
Clean and unclog nozzles. Inspect fluid lines.
**Work plan:** [work/wiper_system/README.md](../work/wiper_system/README.md)

### 3. Paint Inspection (Rear Fender & Hood)
Test hood with magnet (aluminum vs steel). Source OEM touch-up paint (199 Blauschwarz). Inspect once weather improves.

---

## Finnish Registration (Admin)

Autovero paid (€837.05, 2026-03-27). Waiting for rekisteröintilupa. Then: siirtolupa → rekisteröintikatsastus → ensirekisteröinti → Finnish plates.
