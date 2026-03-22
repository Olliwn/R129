#!/usr/bin/env python3
"""Generate SVG schematics from nRF5430 interface board SPICE netlists.

Convention: reference designator above/left, value below/right of component.
Domain separation: labeled regions derived from actual component positions.
"""

import schemdraw
schemdraw.use('svg')
import schemdraw.elements as elm
import os

OUT_DIR = os.path.join(os.path.dirname(__file__), 'schematics')
os.makedirs(OUT_DIR, exist_ok=True)

PURPLE = '#9b59b6'


def sch_power_supply():
    """01: 12V automotive -> protection -> 5V buck -> 3.3V LDO
    Now includes P-FET enable switch splitting V_PROT into always-on and diagnostics buses."""
    with schemdraw.Drawing(show=False, file=os.path.join(OUT_DIR, '01_power_supply.svg')) as d:
        d.config(fontsize=11, unit=3.5)

        bat = elm.SourceV().up().label('V_BAT', loc='top').label('12V', loc='bottom').reverse()
        elm.Ground(lead=False).at(bat.start)

        elm.Line().right().at(bat.end).length(1)
        fuse = elm.FuseUS().right().label('F1', loc='top').label('2A', loc='bottom')
        rpol = elm.Diode().right().label('D1', loc='top').label('1N4007', loc='bottom')

        j1 = elm.Dot()

        with d.hold():
            elm.Line().down().at(j1.center).length(0.5)
            elm.DiodeTVS().down().label('D2', loc='left').label('1.5KE18A', loc='right').reverse()
            elm.Ground(lead=False)

        elm.Line().right().length(1.5)
        j_prot = elm.Dot()
        elm.Label().at(j_prot.center).label('V_PROT', loc='top')

        with d.hold():
            elm.Capacitor(polar=True).down().at(j_prot.center).label('C1', loc='left').label('100µF', loc='right')
            elm.Ground(lead=False)

        # === ALWAYS-ON PATH: straight right to buck -> LDO ===
        elm.Line().right().at(j_prot.center).length(0.5)
        buck = (elm.RBox(linestyle='-').right()
                .label('OKI-78SR\n12V→5V', loc='center', halign='center')
                .label('IN', loc='left').label('OUT', loc='right'))

        elm.Line().right().length(0.5)
        j5 = elm.Dot()
        elm.Label().at(j5.center).label('5V', loc='top')

        with d.hold():
            elm.Capacitor().down().at(j5.center).label('C2', loc='left').label('100nF', loc='right')
            elm.Ground(lead=False)

        elm.Line().right().length(1.5)
        ldo = (elm.RBox(linestyle='-').right()
               .label('LD1117V33\n5V→3.3V', loc='center', halign='center')
               .label('IN', loc='left').label('OUT', loc='right'))

        elm.Line().right().length(0.5)
        j33 = elm.Dot()
        elm.Label().at(j33.center).label('3.3V', loc='top')

        with d.hold():
            elm.Capacitor().down().at(j33.center).label('C3', loc='left').label('100nF', loc='right')
            elm.Ground(lead=False)

        # === DIAGNOSTICS ENABLE PATH: down from V_PROT ===
        # P-FET high-side switch
        pfet_x = j_prot.center[0]
        pfet_y = j_prot.center[1] - 6

        elm.Line().down().at(j_prot.center).length(1.5)

        # P-channel MOSFET as high-side switch
        pfet = elm.PFet().anchor('source').label('Q_EN', loc='left').label('Si2301\nP-FET', loc='right')

        # Gate drive: NPN level shifter from MCU enable GPIO
        gate_pos = pfet.gate
        elm.Line().right().at(gate_pos).length(1)
        elm.Resistor().right().label('R_G', loc='top').label('10kΩ', loc='bottom')
        j_gate = d.here

        with d.hold():
            elm.Resistor().up().at(j_gate).label('R_GP', loc='left').label('100kΩ', loc='right')
            elm.Label().label('V_PROT')

        q_en = elm.BjtNpn().anchor('collector').at(j_gate).label('Q_LVL', loc='left').label('2N7002', loc='right')
        elm.Ground(lead=False).at(q_en.emitter)

        elm.Line().right().at(q_en.base).length(0.5)
        elm.Resistor().right().label('R_EN', loc='top').label('10kΩ', loc='bottom')
        elm.Label().label('MCU\nDIAG_EN', loc='right')

        # P-FET drain = V_DIAG bus
        elm.Line().down().at(pfet.drain).length(1)
        j_diag = elm.Dot()
        elm.Label().at(j_diag.center).label('V_DIAG (12V switched)', loc='right')

        with d.hold():
            elm.Capacitor().down().at(j_diag.center).label('C4', loc='left').label('100µF', loc='right')
            elm.Ground(lead=False)


def sch_rx_channel():
    """02: Car blink-code -> optocoupler -> MCU GPIO (inverted)"""
    with schemdraw.Drawing(show=False, file=os.path.join(OUT_DIR, '02_rx_single_channel.svg')) as d:
        d.config(fontsize=11, unit=3.5)

        # --- CAR DIAGNOSTIC PORT MODEL ---
        vbat = elm.SourceV().up().label('V_BAT', loc='top').label('12V', loc='bottom').reverse()
        elm.Ground(lead=False).at(vbat.start)

        rpu = elm.Resistor().right().at(vbat.end).label('R_PULL', loc='top').label('680Ω', loc='bottom')

        j_diag = elm.Dot()
        elm.Label().at(j_diag.center).label('DIAG PIN', loc='top')

        # Region label anchored to first component
        elm.Label().at((vbat.center[0], vbat.end[1] + 2)).label(
            '── CAR DIAGNOSTIC PORT MODEL ──', fontsize=10)

        with d.hold():
            q_ecu = elm.BjtNpn().at(j_diag.center).anchor('collector').flip()
            elm.Ground(lead=False).at(q_ecu.emitter)
            elm.Line().left().at(q_ecu.base).length(0.5)
            elm.SourcePulse().down().label('BLINK', loc='left').label('CTRL', loc='right').flip()
            elm.Ground(lead=False)

        # --- INTERFACE BOARD ---
        rrx = elm.Resistor().right().at(j_diag.center).label('R_RX', loc='top').label('1kΩ', loc='bottom')

        opto_a = d.here
        led = elm.LED().right().label('TLP521', loc='top').label('LED', loc='bottom')
        led_end = d.here

        # Region label anchored between R_RX and LED
        elm.Label().at((rrx.center[0], vbat.end[1] + 2)).label(
            '── INTERFACE BOARD ──', fontsize=10)

        elm.Line().down().length(0.5)
        elm.Ground(lead=False)

        # Isolation barrier anchored to LED end position
        iso_x = led_end[0] + 1.2
        barrier_top = led_end[1] + 1.5
        barrier_bot = led_end[1] - 5
        elm.Line().at((iso_x, barrier_top)).to((iso_x, barrier_bot)).linestyle('--').color(PURPLE).linewidth(2.5)
        elm.Label().at((iso_x, barrier_top + 0.3)).label('ISOLATION', fontsize=8, color=PURPLE)

        # --- MCU SIDE ---
        elm.Line().right().at(led_end).length(2.5)
        q_photo = elm.BjtNpn(circle=True).anchor('base').drop('collector').label(
            'TLP521\nphoto-NPN', loc='right')

        # Region label anchored to photo-NPN position
        elm.Label().at((q_photo.collector[0], vbat.end[1] + 2)).label(
            '── MCU SIDE (3.3V) ──', fontsize=10)

        elm.Line().down().at(q_photo.emitter).length(0.5)
        elm.Ground(lead=False)

        elm.Line().up().at(q_photo.collector).length(1)
        j_mcu = elm.Dot()
        elm.Label().at(j_mcu.center).label('MCU_RX', loc='right')

        elm.Resistor().up().at(j_mcu.center).label('R_PU', loc='left').label('13kΩ', loc='right')
        elm.Label().label('VCC 3.3V')


def sch_tx_channel():
    """03: MCU GPIO -> optocoupler (emitter-follower) -> 2N2222 driver -> car pin"""
    with schemdraw.Drawing(show=False, file=os.path.join(OUT_DIR, '03_tx_single_channel.svg')) as d:
        d.config(fontsize=11, unit=3.5)

        # --- MCU SIDE ---
        vgpio = elm.SourcePulse().up().label('MCU_TX', loc='top').label('0/3.3V', loc='bottom').reverse()
        elm.Ground(lead=False).at(vgpio.start)

        elm.Label().at((vgpio.center[0], vgpio.end[1] + 2)).label(
            '── MCU SIDE (3.3V) ──', fontsize=10)

        rtx = elm.Resistor().right().at(vgpio.end).label('R_TX', loc='top').label('330Ω', loc='bottom')

        opto_a = d.here
        led = elm.LED().right().label('TLP521', loc='top').label('LED', loc='bottom')
        led_end = d.here
        elm.Line().down().length(0.5)
        elm.Ground(lead=False)

        # Isolation barrier
        iso_x = led_end[0] + 1.2
        barrier_top = led_end[1] + 3
        barrier_bot = led_end[1] - 8
        elm.Line().at((iso_x, barrier_top)).to((iso_x, barrier_bot)).linestyle('--').color(PURPLE).linewidth(2.5)
        elm.Label().at((iso_x, barrier_top + 0.3)).label('ISOLATION', fontsize=8, color=PURPLE)

        # --- INTERFACE BOARD: CAR SIDE ---
        vbat_pos = (led_end[0] + 3, led_end[1] + 3)
        elm.Label().at(vbat_pos).label('V_DIAG 12V')

        elm.Label().at((vbat_pos[0], vgpio.end[1] + 2)).label(
            '── INTERFACE: CAR SIDE (12V) ──', fontsize=10)

        r_oc = elm.Resistor().down().at(vbat_pos).label('R_OC', loc='left').label('1kΩ', loc='right')

        q_opto = elm.BjtNpn(circle=True).anchor('collector').drop('emitter').label(
            'TLP521', loc='left').label('photo-NPN\n(emitter-follower)', loc='right', fontsize=8)

        j_emit = elm.Dot()

        with d.hold():
            elm.Resistor().down().at(j_emit.center).label('R_PD', loc='left').label('10kΩ', loc='right')
            elm.Ground(lead=False)

        elm.Line().right().at(j_emit.center).length(1.5)
        q_drv = elm.BjtNpn().anchor('base').label('Q_DRV', loc='left').label('2N2222', loc='right')

        elm.Line().down().at(q_drv.emitter).length(0.5)
        elm.Ground(lead=False)

        elm.Line().up().at(q_drv.collector).length(1)
        j_pin = elm.Dot()
        elm.Label().at(j_pin.center).label('DIAG PIN', loc='top')

        # --- CAR PORT MODEL ---
        elm.Label().at((j_pin.center[0] + 3, vgpio.end[1] + 2)).label(
            '── CAR PORT MODEL ──', fontsize=10)

        elm.Resistor().up().at(j_pin.center).label('R_PULL', loc='left').label('680Ω', loc='right')
        elm.Label().label('V_BAT 12V')

        with d.hold():
            elm.Line().right().at(j_pin.center).length(0.5)
            cp = d.here
            elm.Capacitor().down().at(cp).label('C_CABLE', loc='left').label('500pF', loc='right')
            elm.Ground(lead=False)


def sch_analog_conditioning():
    """04: Battery voltage + airflow pot -> dividers -> buffers -> RC filters -> ADC"""
    with schemdraw.Drawing(show=False, file=os.path.join(OUT_DIR, '04_analog_conditioning.svg')) as d:
        d.config(fontsize=10, unit=3.0)

        # PATH 1: Battery Voltage
        vbat = elm.SourceV().up().at((0, -1)).label('V_BAT', loc='top').label('12V', loc='bottom').reverse()
        elm.Ground(lead=False).at(vbat.start)

        elm.Label().at((vbat.center[0], vbat.end[1] + 1.5)).label(
            'PATH 1: BATTERY VOLTAGE (0–14.4V → 0–2.6V)', fontsize=11)

        r_hi = elm.Resistor().right().at(vbat.end).label('R1', loc='top').label('10kΩ', loc='bottom')
        j_div = elm.Dot()

        with d.hold():
            elm.Resistor().down().at(j_div.center).label('R2', loc='left').label('2.2kΩ', loc='right')
            elm.Ground(lead=False)

        with d.hold():
            elm.Diode().up().at(j_div.center).label('D1', loc='left').label('1N4148', loc='right')
            elm.Label().label('3.3V')

        with d.hold():
            elm.Line().down().at(j_div.center).length(0.3)
            elm.Diode().down().flip().label('D2', loc='left').label('1N4148', loc='right')
            elm.Ground(lead=False)

        elm.Line().right().at(j_div.center).length(0.5)
        opamp = elm.Opamp(sign=True).anchor('in1').label('LM358', loc='center', fontsize=8)

        # Feedback routed outside (below) the opamp
        elm.Wire('c', k=-1.5).at(opamp.out).to(opamp.in2).color('gray')

        elm.Resistor().right().at(opamp.out).label('R3', loc='top').label('1kΩ', loc='bottom')
        j_filt = elm.Dot()
        elm.Label().at(j_filt.center).label('ADC_BAT', loc='top')

        with d.hold():
            elm.Capacitor().down().at(j_filt.center).label('C1', loc='left').label('100nF', loc='right')
            elm.Ground(lead=False)

        elm.Line().right().at(j_filt.center).length(0.5)
        elm.Resistor().down().label('R_ADC', loc='left').label('10MΩ', loc='right')
        elm.Ground(lead=False)

        # PATH 2: Airflow Pot
        y_off = -7.5
        vair = elm.SourceV().up().at((0, y_off)).label('V_AIR', loc='top').label('0–5V', loc='bottom').reverse()
        elm.Ground(lead=False).at(vair.start)

        elm.Label().at((vair.center[0], vair.end[1] + 1.5)).label(
            'PATH 2: AIRFLOW POTENTIOMETER (0–5V → 0–2.5V)', fontsize=11)

        r_hi2 = elm.Resistor().right().at(vair.end).label('R4', loc='top').label('10kΩ', loc='bottom')
        j_div2 = elm.Dot()

        with d.hold():
            elm.Resistor().down().at(j_div2.center).label('R5', loc='left').label('10kΩ', loc='right')
            elm.Ground(lead=False)

        with d.hold():
            elm.Diode().up().at(j_div2.center).label('D3', loc='left').label('1N4148', loc='right')
            elm.Label().label('3.3V')

        with d.hold():
            elm.Line().down().at(j_div2.center).length(0.3)
            elm.Diode().down().flip().label('D4', loc='left').label('1N4148', loc='right')
            elm.Ground(lead=False)

        elm.Line().right().at(j_div2.center).length(0.5)
        opamp2 = elm.Opamp(sign=True).anchor('in1').label('LM358', loc='center', fontsize=8)
        elm.Wire('c', k=-1.5).at(opamp2.out).to(opamp2.in2).color('gray')

        elm.Resistor().right().at(opamp2.out).label('R6', loc='top').label('1kΩ', loc='bottom')
        j_filt2 = elm.Dot()
        elm.Label().at(j_filt2.center).label('ADC_AIR', loc='top')

        with d.hold():
            elm.Capacitor().down().at(j_filt2.center).label('C2', loc='left').label('100nF', loc='right')
            elm.Ground(lead=False)

        elm.Line().right().at(j_filt2.center).length(0.5)
        elm.Resistor().down().label('R_ADC', loc='left').label('10MΩ', loc='right')
        elm.Ground(lead=False)


def sch_full_diag_channel():
    """05: Complete bidirectional diagnostic channel (RX + TX + car model)"""
    with schemdraw.Drawing(show=False, file=os.path.join(OUT_DIR, '05_full_diag_channel.svg')) as d:
        d.config(fontsize=10, unit=3.0)

        # ── CAR DIAGNOSTIC PORT MODEL (left) ──
        vbat = elm.SourceV().up().at((0, 0)).label('V_BAT', loc='top').label('12V', loc='bottom').reverse()
        elm.Ground(lead=False).at(vbat.start)

        rpu = elm.Resistor().right().at(vbat.end).label('R_PULL', loc='top').label('680Ω', loc='bottom')
        j_diag = elm.Dot()
        elm.Label().at(j_diag.center).label('DIAG PIN', loc='top')

        elm.Label().at((vbat.center[0] + 1.5, vbat.end[1] + 1.5)).label(
            '── CAR PORT MODEL ──', fontsize=10)

        with d.hold():
            q_ecu = elm.BjtNpn().at(j_diag.center).anchor('collector').flip()
            elm.Ground(lead=False).at(q_ecu.emitter)
            elm.Line().left().at(q_ecu.base).length(0.5)
            elm.SourcePulse().down().label('ECU', loc='left').label('blink', loc='right').flip()
            elm.Ground(lead=False)

        # ── INTERFACE: RX PATH (upper right) ──
        rrx = elm.Resistor().right().at(j_diag.center).label('R_RX', loc='top').label('1kΩ', loc='bottom')
        rx_led = elm.LED().right().label('RX opto', loc='top').label('LED', loc='bottom')
        rx_led_end = d.here

        elm.Label().at((rrx.center[0], vbat.end[1] + 1.5)).label(
            '── RX PATH ──', fontsize=10)

        elm.Line().down().length(0.5)
        elm.Ground(lead=False)

        # RX isolation
        iso_x = rx_led_end[0] + 1.2
        iso_top_y = vbat.end[1] + 1
        iso_bot_y = vbat.start[1] - 10
        elm.Line().at((iso_x, iso_top_y)).to((iso_x, iso_bot_y)).linestyle('--').color(PURPLE).linewidth(2.5)
        elm.Label().at((iso_x, iso_top_y + 0.3)).label('ISOLATION', fontsize=8, color=PURPLE)

        # RX MCU side
        elm.Line().right().at(rx_led_end).length(2.5)
        q_rx = elm.BjtNpn(circle=True).anchor('base').drop('collector').label(
            'RX photo-NPN', loc='right', fontsize=8)

        elm.Label().at((q_rx.collector[0], vbat.end[1] + 1.5)).label(
            '── MCU SIDE (3.3V) ──', fontsize=10)

        elm.Line().down().at(q_rx.emitter).length(0.5)
        elm.Ground(lead=False)

        elm.Line().up().at(q_rx.collector).length(1)
        j_mcu_rx = elm.Dot()
        elm.Label().at(j_mcu_rx.center).label('MCU_RX', loc='right')
        elm.Resistor().up().at(j_mcu_rx.center).label('R_PU', loc='left').label('13kΩ', loc='right')
        elm.Label().label('VCC 3.3V')

        # ── TX PATH (below) ──
        # MCU TX source
        tx_x = iso_x + 3
        tx_y = vbat.start[1] - 4
        vtx = elm.SourcePulse().up().at((tx_x, tx_y)).label('MCU_TX', loc='top').label('0/3.3V', loc='bottom').reverse()
        elm.Ground(lead=False).at(vtx.start)

        elm.Resistor().right().at(vtx.end).label('R_TX', loc='top').label('330Ω', loc='bottom')
        tx_led = elm.LED().right().label('TX opto', loc='top').label('LED', loc='bottom')
        tx_led_end = d.here
        elm.Line().down().length(0.5)
        elm.Ground(lead=False)

        # TX car-side driver
        tx_drv_x = iso_x - 3
        tx_drv_top_y = tx_y + 5

        elm.Label().at((tx_drv_x, tx_drv_top_y)).label('V_DIAG 12V')

        elm.Label().at((tx_drv_x - 2, vbat.end[1] + 1.5)).label(
            '── TX DRIVER ──', fontsize=10)

        elm.Resistor().down().at((tx_drv_x, tx_drv_top_y)).label('R_OC', loc='left').label('1kΩ', loc='right')

        q_tx_opto = elm.BjtNpn(circle=True).anchor('collector').drop('emitter').label(
            'TX photo-NPN', loc='left', fontsize=8).label('(E-follower)', loc='right', fontsize=7)

        j_tx_emit = elm.Dot()

        with d.hold():
            elm.Resistor().down().at(j_tx_emit.center).label('R_PD', loc='left').label('10kΩ', loc='right')
            elm.Ground(lead=False)

        elm.Line().left().at(j_tx_emit.center).length(1.5)
        q_drv = elm.BjtNpn().anchor('base').flip().label('Q_DRV', loc='right').label('2N2222', loc='left')

        elm.Line().down().at(q_drv.emitter).length(0.5)
        elm.Ground(lead=False)

        elm.Line().up().at(q_drv.collector).toy(j_diag.center)
        elm.Line().right().tox(j_diag.center)
        elm.Dot()


def main():
    print("Generating schematics...")
    funcs = [
        ("01_power_supply", sch_power_supply),
        ("02_rx_single_channel", sch_rx_channel),
        ("03_tx_single_channel", sch_tx_channel),
        ("04_analog_conditioning", sch_analog_conditioning),
        ("05_full_diag_channel", sch_full_diag_channel),
    ]
    for name, func in funcs:
        try:
            func()
            print(f"  OK  {name}.svg")
        except Exception as e:
            print(f"  ERR {name}: {e}")
            import traceback
            traceback.print_exc()
    print(f"\nOutput: {OUT_DIR}")


if __name__ == '__main__':
    main()
