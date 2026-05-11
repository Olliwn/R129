# In-Car Pi → MEC HD-USB Bring-Up — Safety Procedure

**Purpose:** Step-by-step procedure for the first time the RPi5 is physically connected to the MEC HD-USB inside the car, so a stale configuration, runaway volume, or USB transient cannot fry the Hertz MP 28.3 tweeters (28 mm dome — mechanically fragile below ~500 Hz; thermally fragile above amplifier-clip levels).

**Status:** Procedure-only document; not a build log. Read once before the in-car session; tick through the checklist live.

**Sources:** Built on the bench-test safety baseline (`work/audio_bench_test.md` §5.1 + §9), the Pi-side audio prep done indoor 2026-05-11 (per `docs/diary/2026-05.md` 2026-05-11 entry), and the DSP power topology (`work/audio_upgrade_blueprint.md` §1 and §5).

---

## 1. The risk model in plain terms

The Pi never directly drives the tweeters. The DSP does. The Pi just delivers a digital audio stream to the DSP via USB UAC (the MEC HD-USB module). So the question "can plugging in the Pi blow a tweeter?" reduces to four stages from source to driver:

| Stage | What can go wrong | Bound by |
| :--- | :--- | :--- |
| **1. iPhone media volume** | iOS sends full-scale samples if media volume = 100 % | User action: set iPhone media to ≤ 25 % before first play |
| **2. Pi PipeWire output level** | Default 100 % unity gain passes full-scale through to USB UAC | **`~/bin/audio-safe.sh`** caps all sinks at 50 % (-6 dB) at any time it's run |
| **3. DSP digital input + per-channel gain + filters** | If tweeter HP filter missing or gain too high, full-bandwidth → tweeter | **`bench_test_v1` preset** (already in DSP NVRAM) has HP 3 kHz LR24 + -10 dB on Ch1/Ch2 |
| **4. DSP power amp** | Even with HP filter, excessive amp gain can put a tweeter into clipping/thermal stress | DSP master gain conservative, ramp slowly, listen for distortion |

Killing the tweeter requires *multiple* of these stages to fail simultaneously. The procedure below ensures each stage is in a known-good state before signal is first applied.

---

## 2. Pre-flight checklist (do BEFORE the in-car session, in the garage with the car off)

### 2.1 DSP-side verification (laptop with DSP PC-Tool, USB cable to the UP 6DSP)

This is the *single most important* check. Five minutes of laptop work that prevents a permanent driver kill.

- [ ] **Connect laptop to UP 6DSP via USB.** DSP PC-Tool detects the device. Hit the "🔄 Read from device" icon to pull the *active running* preset (not what's saved on disk on the laptop).
- [ ] **Verify Ch1 (L Tweeter):**
  - High-pass filter **enabled**, frequency **2.5–3 kHz**, slope **LR 24 dB/oct** (or steeper).
  - Low-pass filter either **disabled** or > 20 kHz.
  - Channel gain trim **≤ -6 dB** (bench-test preset has -10 dB; anything safer is fine).
- [ ] **Verify Ch2 (R Tweeter):** same as Ch1.
- [ ] **Verify Ch3 (L Woofer):** HP 80 Hz LR24, LP 2.5–3 kHz LR24 (active crossover handover to Ch1), gain ≤ -6 dB.
- [ ] **Verify Ch4 (R Woofer):** same as Ch3.
- [ ] **Verify Ch5 + Ch6 (Sub DVC coils):** HP 45 Hz LR24 (subsonic protection), LP 80 Hz LR24, gain ≤ -6 dB. **Both coils same polarity / same level.**
- [ ] **Master gain / output volume** at conservative starting point (mid-range or below; **not 0 dB / unity**).
- [ ] **If any of the above are NOT as expected:** re-load `bench_test_v1` from the saved file or fix in PC-Tool. **Click "Save & Store" (disk icon)** to persist to NVRAM. Without Save & Store, the change is preview-only and won't survive a power cycle (per `audio_bench_test.md` §6.2).

### 2.2 Pi-side verification (SSH from laptop, Pi running indoors or already in the cubby)

- [ ] `ssh pi@r129.local` succeeds.
- [ ] `wpctl status` shows PipeWire 1.4.2 active. **Default sink should be "Dummy Output"** (or any other sink at ≤ 50 % volume — see next step).
- [ ] **Run `~/bin/audio-safe.sh`** to cap all sinks at 50 % (-6 dB). Verify the script reports the sink(s) it touched. (If no real sinks present yet, that's fine — the MEC will appear in §3.)
- [ ] iPhone listed in `bluetoothctl devices Paired` and `bluetoothctl devices Trusted`. Will auto-reconnect when in BT range.

### 2.3 iPhone-side verification (any time)

- [ ] **iPhone media volume set to 25 % (~ ⅛ of the way up).** Bluetooth A2DP volume on iOS syncs with the sink's per-stream volume on the Pi, but the iPhone's *source*-side level still gates dynamic range.
- [ ] **Disable iOS "Sound Check" / "Volume Limit"** — these can interact unpredictably with the BT A2DP volume curve. Cleaner to control level with iPhone media slider only.
- [ ] **No music playing** at the moment of plug-in.

### 2.4 Amplifier / DSP power state

- [ ] **REM line OFF** before plugging the MEC USB into the Pi. The DSP currently has a REM-to-+12 V jumper (per `audio_upgrade_blueprint.md` §Phase 1 "Auto-wake caveat" and `docs/diary/2026-05.md` 2026-05-07 entry), so "REM off" means either:
  - Disconnect the +12 V feed to the DSP at the AGU fuse, **OR**
  - Temporarily lift the REM jumper inside the DSP.
- [ ] **Battery maintainer connected** if the session is expected to run > 30 min — DSP + Pi + measurement laptop together pull enough to drop a marginal battery.

---

## 3. Plug-in sequence — the actual bring-up

Do this **once** the pre-flight is complete. Order matters.

1. [ ] **Confirm REM is OFF (DSP not powered).** No audible amplifier hum. LEDs on the DSP either off or showing standby.
2. [ ] **Plug the MEC HD-USB cable into one of the Pi's USB-A ports.** (The cable is already pulled and terminating at a temp location per `audio_upgrade_blueprint.md` §Phase 1 step 4.) USB-A 3.0 (blue) is preferred but USB 2.0 also works fine — MEC HD-USB is bus-powered Full Speed UAC.
3. [ ] **Wait ~5 seconds**, then over SSH: `wpctl status`. New sink should appear, something like `alsa_output.usb-Audiotec_Fischer_*.iec958-stereo`.
4. [ ] **Re-run `~/bin/audio-safe.sh`** so the freshly-appeared MEC sink starts at 50 % volume.
5. [ ] **Set MEC as default sink:** `wpctl set-default <id>` where `<id>` is the new MEC's node number from step 3. Then `wpctl get-volume @DEFAULT_AUDIO_SINK@` should report `Volume: 0.50`.
6. [ ] **iPhone auto-reconnect:** within ~30 s the iPhone should auto-pair to `r129` (trusted device). `wpctl status` should show the iPhone as a bluez5 device with an active stream routed to the MEC sink.

At this point: digital audio is flowing iPhone → BT/SBC-XQ → Pi/PipeWire → USB UAC → MEC → DSP. **The amplifier is still OFF so no sound exits the speakers.** This is intentional — we want to confirm the whole digital chain is wired correctly before any acoustic energy is produced.

---

## 4. First sound — ramp-up sequence (REM on, low-volume listen)

1. [ ] **No music playing on iPhone.** Pause Spotify / Apple Music.
2. [ ] **REM ON** (reconnect +12 V feed or re-install jumper). DSP wakes. Listen for ~5 s in silence — should hear:
   - Faint power-on click as DSP relays engage.
   - No continuous hiss / hum / buzz beyond very faint amp noise floor.
   - **If you hear loud buzz, hum, or a sustained tone:** REM OFF immediately. Don't continue. Diagnose before reapplying power.
3. [ ] **Press play on iPhone** at the 25 % phone volume already set. Choose **vocal-forward acoustic material** (single instrument, vocals, no heavy bass) as the first test track — easy to spot if the tweeter is getting bass content.
4. [ ] **Listen at low DSP output.** You should hear:
   - **Both tweeters producing HF content** (vocal presence, cymbal shimmer, sibilants) — sit forward and check both sides at ear height.
   - **Both woofers producing midbass** through midrange (body of voice, lower instruments). No HF buzz / harshness from the woofers.
   - **Sub producing low bass only** below ~80 Hz. Should be felt more than heard at low level.
   - **No "thin" tweeter sound** with bass artifacts (would indicate HP filter not engaged).
   - **No distortion, popping, or thermal odor** (the latter is the alarm to cut power instantly).
5. [ ] **Ramp DSP master gain** (or system volume on the iPhone) **gradually**, in ~3 dB steps with a few seconds between, until you reach a comfortable listening level. Listen for distortion at each step.
6. [ ] **If at any point** something sounds wrong — distortion, missing channel, thin/bass-loaded tweeter, smell — **kill REM immediately** and diagnose.

---

## 5. Kill switches (know where they are before you start)

In order of "fastest to cut" first:

1. **iPhone pause button** — cuts source signal in ~50 ms. Always reachable.
2. **`wpctl set-volume @DEFAULT_AUDIO_SINK@ 0` over SSH** — drops Pi output to zero immediately without disconnecting anything.
3. **REM line disconnect** — drops the DSP to standby. Cuts amp output. The +12 V jumper is in the rear passenger cubby; pulling it is a 5-second physical operation.
4. **40 A AGU fuse pull** at the battery — total kill. Nuclear option.

---

## 6. Post-bring-up — saving the safe state

Once the first sound test is successful and you're listening at comfortable level without issues:

- [ ] **Note the DSP master gain setting** that gives comfortable listening at iPhone media volume = 50 %. This becomes your "reference level" for tuning.
- [ ] **Pi-side volume:** leave the MEC sink at 50 % (-6 dB) as the long-term default. Adjustments happen at the DSP and the iPhone, not on the Pi.
- [ ] **Append to `docs/diary/2026-05.md`** a short bring-up entry: DSP preset confirmed safe, MEC enumerated, iPhone auto-reconnect verified, first listen subjective notes.
- [ ] **Update `work/audio_upgrade_blueprint.md` Phase 1 step #4** status from "⚠️ Pending — Pi → MEC integration" to "✅ Complete".

---

## 7. Quick-reference one-screen checklist

For when you're in the garage and don't want to re-read the whole doc:

```
PRE-FLIGHT (REM off, car off):
  [ ] DSP PC-Tool: Ch1/Ch2 HP @ 2.5-3 kHz LR24, gain ≤ -6 dB    [bench_test_v1]
  [ ] DSP PC-Tool: Master gain conservative, not unity
  [ ] DSP PC-Tool: Save & Store if anything changed
  [ ] Pi SSH:  wpctl status sane, audio-safe.sh just ran        [sinks at 50%]
  [ ] iPhone:  media volume 25%, not playing
  [ ] REM:     OFF (jumper out OR AGU pulled)

PLUG-IN:
  [ ] MEC USB into Pi
  [ ] wpctl status shows new MEC sink
  [ ] audio-safe.sh (caps MEC sink at 50%)
  [ ] wpctl set-default <MEC-id>
  [ ] iPhone auto-reconnects (visible in wpctl status as bluez5)

FIRST SOUND:
  [ ] REM ON, listen 5s silence for hum/buzz
  [ ] iPhone press play (vocal-forward track)
  [ ] Listen: both tweeters HF, both woofers midbass, sub LF only
  [ ] Ramp DSP master in 3 dB steps to comfortable level

IF ANYTHING SOUNDS WRONG:
  iPhone pause -> wpctl vol 0 -> REM off -> AGU pull
```

---

## 8. Why this is conservative (and why it's worth it)

You may be tempted to skip the DSP PC-Tool pre-flight ("the preset is already in NVRAM, it's been working in-car since May 7"). That's a reasonable assumption — and it's probably right. **The cost of being wrong is a €100+ pair of tweeters and an unhappy day of resoldering.** The cost of doing the pre-flight is ~5 minutes with a laptop. The expected-value math is overwhelming in favor of the pre-flight.

The bench-test preset was designed by your past self specifically as a "minimum-safe preset" with the -10 dB across-the-board trim explicitly characterised as "insurance against a wiring error blowing a driver" (per `work/audio_bench_test.md` §5.1). Use the insurance.
