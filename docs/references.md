# AOK912 -- References & Tools

**Vehicle:** 1991 Mercedes-Benz 500 SL (R129) | VIN: WDB 129066 1F 044414

---

## Local Searchable Knowledge Base (r129_data/)

110 factory manuals and diagnostic guides ingested into 2,435 searchable chunks with image transcriptions. Full details: see [r129_data/SKILL.md](../r129_data/SKILL.md).

| Method | Command / Approach | When to Use |
|--------|-------------------|-------------|
| **Semantic search** | `cd r129_data && source .venv/bin/activate && python -m r129_data search-docs "query"` | Broad technical questions |
| **YAML lookup** | `python -m r129_data search --fuse F6` | Exact lookups (fuses, relays, fluids, torques) |
| **Raw file search** | Grep on `r129_data/references/chunks/all_chunks.jsonl` | Quick keyword search, Cursor AI agent |

Curation decisions: `r129_data/references/curation.yaml`

---

## Online Documentation & Manuals

### Official Owner's Manuals
* [r129-owners-manual-1990.pdf (mb.clifton.io)](https://mb.clifton.io/downloads/r129-owners-manual-1990.pdf) -- General operation, fuse locations, manual soft-top override.

### Specialist Repair Guides
* [Top Hydraulics R129 Instructions](https://www.tophydraulics.com/) -- Step-by-step guides for all 11 hydraulic roof cylinders.
* [STAR TekInfo R129 Library](https://manual.startekinfo.com/manual/JSP/model129.jsp) -- Factory diagnostic manuals.

### Community Knowledge Bases
* [The Brian Clifton R129 Archive](https://mb.clifton.io/r129/) -- Literature, radio manuals, historical articles.
* [BenzWorld R129 Forum](https://www.benzworld.org/forums/r129-sl-class.26/) -- Deep-dive troubleshooting (ADS blink-code, KE-Jetronic).
* [BenzWorld R129 PDF collection](https://www.benzworld.org/threads/all-of-the-r129-pdfs-i-have-collected-over-the-years.3099517/)

*(Much of the STAR Classic Service Manual Library for the 1991 R129 has been ingested into the local `r129_data/` repository.)*

---

## Tool Inventory

*Metric, precision toolset for the M119 V8 and R129 chassis. Focus on B2B-grade European brands.*

**Local suppliers:** Kärkkäinen (Wera, Knipex, Bahco off the shelf), Motonet, MB-Osa, Puuilo, Biltema.

### General Hand Tools
* **Sockets & Ratchets:** Bahco S910 & SBSL25 sets (Acquired)
* **Wrenches:** Bahco Combination Wrenches (Acquired)
* **Hex & Torx:** Bondhus Torx Set, Wera Hex-Plus (Acquired)
* **Pliers:** Knipex Cobra, Diagonal Cutters, Needle-Nose (Acquired)

### Specialty & Electrical Tools
* **36mm Socket:** For M119 oil filter housing cap.
* **Torque Wrenches:** 3/8" (20-100 Nm) and 1/2" (up to 200 Nm). (Acquired)
* **Hose Clamp Pliers:** MTX letkunsulkijapihtisarja. (Acquired 2026-03-28)
* **Multimeter & Oscilloscope:** Owon HDS242. (Acquired)

### Power Tools (DeWalt 20V MAX / 18V XR Platform)
* **DeWalt DCS438 Cordless 3" Cut-Off Tool:** Brushless, 20,000 RPM, 22mm max depth. Incl. abrasive, diamond multi-material & diamond tile wheels. (Acquired 2026-04, Puuilo, €129)
