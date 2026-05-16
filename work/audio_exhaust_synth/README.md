# R129 Exhaust Synth Prototype

Procedural V8 cabin-augmentation synth for the R129 M119, built in
gated phases per the parent plan:

| Gate | Where | What | Pass criterion |
| :--- | :--- | :--- | :--- |
| 0 | Mac → living-room speakers | Procedural V8 driven by synthetic RPM | The roar is musical, not cartoonish |
| 1 | Mac, offline | Same synth phase-locked to a recorded exhaust WAV | Mic + synth downmix sounds coherent |
| 2 | Paper design | Sensor strategy, PipeWire topology, DSP gain staging, UI | Concrete BOM and topology |
| 3 | In car | Driveway bench test + REW captures + bypass A/B | One preset survives a real drive |
| Final | In car | Permanent install + settings UI + telemetry roadmap | — |

This directory only contains Gate 0 / Gate 1 code plus the design notes
for Gates 2–Final. No `UI_rpi5/` or DSP changes are made until Gate 2.

## Pre-rendered listening pack

A reference set of WAVs is available under `renders/` after running the
generator commands below. **For the subjective Gate 0 + Gate 1 evaluation,
play these through the living-room rig. The companion guide is
[`LISTENING_GUIDE.md`](LISTENING_GUIDE.md)** — it lists every file, the
order to listen in, and the pass criteria for each gate.

## Setup

```bash
cd work/audio_exhaust_synth
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`sounddevice` is optional. If you can't install it (no PortAudio), you can
still render WAVs with `--out` and play them in any audio app, including
through the living-room rig.

## Gate 0 — Living-room V8 preview

Pure procedural synth driven by a synthetic RPM curve. No mic, no car,
no feedback.

```bash
# Smooth 800 ↔ 3000 rpm triangle sweep on the "luxury cruiser" preset
python3 prototype.py preview --preset luxury --mode sweep \
    --start 800 --end 3000 --cycle 8 --duration 20

# Steady 2000 rpm hold — useful for evaluating timbre at a fixed pitch
python3 prototype.py preview --preset amg --mode hold --rpm 2000 --duration 8

# Lopey idle (800 rpm with ±30 rpm wobble)
python3 prototype.py preview --preset luxury --mode idle --duration 10

# Throttle stabs (900 → 4000 → 900 rpm every 2 sec)
python3 prototype.py preview --preset sport --mode stab \
    --start 900 --end 4000 --cycle 2 --duration 12

# Render every preset back-to-back into one WAV for A/B listening
python3 prototype.py compare --out-dir renders/compare
```

### Presets

| Preset | Target character | Intended use |
| :--- | :--- | :--- |
| `off` | silent | bypass |
| `oem` | subtle V8 body fill | "miss it when off" |
| `luxury` | refined cruiser, 2nd-order burble, restrained top | the goal preset |
| `amg` | more burble + more upper growl | character demo |
| `sport` | loud and toothy | the "too far" reference |

### Pass criterion for Gate 0

Play the `luxury` sweep on the Genelec G3 + SVS sub system at moderate
volume. Verdict:

- **Pass** → the roar sounds plausibly like a refined V8 — engaging, not
  cartoonish, not obviously a sawtooth. Proceed to Gate 1.
- **Fail** → revisit the synth model (more harmonics? formant filtering?
  sample-based? cross-plane firing-interval modulation?) or abandon.

Use `compare` to listen to all presets back-to-back; that is the fastest
way to triangulate where on the cartoon ↔ realistic axis the synth sits.

## Gate 1 — Offline tracker (no car required)

Once Gate 0 passes, capture an exhaust clip with the phone or UMIK-1 at
the rear bumper / engine bay, e.g. `clips/idle.wav`. Then:

```bash
python3 prototype.py track --wav clips/idle.wav --preset luxury \
    --duration 20 \
    --synth-out renders/track_synth.wav \
    --downmix-out renders/track_downmix.wav \
    --side-out renders/track_side.wav \
    --play downmix
```

Outputs:

- **`track_synth.wav`** — synth alone, phase-locked to the mic. Listen
  for any warble / jitter, especially during slow revs.
- **`track_downmix.wav`** — mic + synth at the gain-staging target the
  in-car DSP will use (mic −6 dBFS, synth −9 dBFS). This is the
  "would the cabin sound good?" deliverable.
- **`track_side.wav`** — L = mic, R = synth. Solo each channel in
  Audacity / REW to see the alignment.

The console prints tracker confidence statistics. Low confidence on real
recordings usually means the bandpass window is wrong or the mic was
picking up too much wind noise — try recording with the engine cover
acting as a windscreen and the mic 30 cm from the exhaust.

### No recording yet?

Generate a synthetic test clip and run the tracker against it
end-to-end:

```bash
python3 prototype.py make-clip --out clips/fake.wav --duration 20
python3 prototype.py track --wav clips/fake.wav --preset luxury \
    --duration 20 --downmix-out renders/fake_downmix.wav --play downmix
```

This proves the tracker pipeline works before any garage trip. It is
**not** a substitute for a real M119 recording — the synthetic clip uses
the same harmonic structure as the synth, so locking is trivially easy.

### Pass criterion for Gate 1

- Tracker confidence stays above ~0.5 across a 1500–3000 rpm slow sweep
  recording.
- The downmix sounds like one coherent exhaust on living-room speakers,
  not two stacked signals.
- The synth visibly fades down on engine-off / between-recording silence.

## Files

| File | Role |
| :--- | :--- |
| [`v8_synth.py`](v8_synth.py) | Procedural V8 synth, preset palette, soft limiter |
| [`rpm_source.py`](rpm_source.py) | `RpmSource` interface + `SyntheticSource` (G0) + `WavFileSource` (G1) |
| [`engine_tracker.py`](engine_tracker.py) | Bandpass + FFT peak + slew-limited PLL |
| [`prototype.py`](prototype.py) | CLI runner: `preview`, `compare`, `track`, `make-clip` |
| [`requirements.txt`](requirements.txt) | numpy / scipy / soundfile / sounddevice |
| [`gate2_car_integration_design.md`](gate2_car_integration_design.md) | Paper design for car integration (post-Gate-1) |
| [`gate3_in_car_validation.md`](gate3_in_car_validation.md) | Driveway + REW validation procedure |
| [`final_permanent_build.md`](final_permanent_build.md) | Commit checklist (gated on Gate 3) |

## Safety notes

- The synth always ends in a soft `tanh` limiter at ≈ −3 dBFS. Master
  gain is hard-capped at 1.0 internally.
- Playback uses your default Mac output. Set the system volume sensibly
  before running `preview`; nothing here boosts above the synth's own
  ceiling.
- No driver-head feedback loop is implemented at any stage — the
  reference signal in Gate 1 is a pre-recorded WAV, not a live mic.

## What this prototype deliberately is not

- Not a fake AMG mimic — the goal is "the M119 you can hear from inside
  with the soft top up," not a Mercedes-AMG knock-off.
- Not real-time car telemetry — `rpm` field in
  [`UI_rpi5/src/vehicle_state.py`](../../UI_rpi5/src/vehicle_state.py)
  will become a `CanBusSource` later, but Gate 0 / Gate 1 use synthetic
  or WAV-tracked RPM only.
- Not a closed-loop active-noise system — that's a separate idea
  (anti-drone) that's deliberately not on this critical path.
