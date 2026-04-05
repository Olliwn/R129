"""
R129 Driver UI -- Gauge Preview Mockup
Classic Mercedes-Benz VDO instrument style: dark background, amber dials.
Fullscreen on the Waveshare 5.5" AMOLED (1920x1080 landscape).
"""

import sys
import math
import time
import pygame

SCREEN_W, SCREEN_H = 1920, 1080

BG = (5, 5, 8)
AMBER = (255, 160, 30)
AMBER_DIM = (140, 80, 10)
AMBER_DARK = (60, 35, 5)
NEEDLE_RED = (200, 40, 30)
WHITE_DIM = (160, 155, 140)
BEZEL = (30, 28, 25)

def draw_gauge(surface, cx, cy, radius, value, min_val, max_val,
               label, unit, major_ticks, minor_per_major=4,
               redline_start=None, start_angle=225, sweep=270):
    """Draw a single circular gauge."""

    pygame.draw.circle(surface, BEZEL, (cx, cy), radius + 4)
    pygame.draw.circle(surface, (12, 12, 15), (cx, cy), radius)
    pygame.draw.circle(surface, AMBER_DARK, (cx, cy), radius, 2)

    for i, tick_val in enumerate(major_ticks):
        frac = (tick_val - min_val) / (max_val - min_val)
        angle_deg = start_angle - frac * sweep
        angle = math.radians(angle_deg)

        in_redline = redline_start is not None and tick_val >= redline_start
        color = NEEDLE_RED if in_redline else AMBER

        r_outer = radius - 8
        r_inner = radius - 28
        x0 = cx + r_inner * math.cos(angle)
        y0 = cy - r_inner * math.sin(angle)
        x1 = cx + r_outer * math.cos(angle)
        y1 = cy - r_outer * math.sin(angle)
        pygame.draw.line(surface, color, (x0, y0), (x1, y1), 3)

        font_size = max(18, radius // 8)
        font = pygame.font.SysFont("sans", font_size)
        tick_label = str(int(tick_val))
        txt = font.render(tick_label, True, color)
        r_text = radius - 40
        tx = cx + r_text * math.cos(angle) - txt.get_width() / 2
        ty = cy - r_text * math.sin(angle) - txt.get_height() / 2
        surface.blit(txt, (tx, ty))

        if i < len(major_ticks) - 1:
            next_val = major_ticks[i + 1]
            for m in range(1, minor_per_major + 1):
                mval = tick_val + m * (next_val - tick_val) / (minor_per_major + 1)
                mfrac = (mval - min_val) / (max_val - min_val)
                mangle = math.radians(start_angle - mfrac * sweep)
                mr_outer = radius - 8
                mr_inner = radius - 18
                mx0 = cx + mr_inner * math.cos(mangle)
                my0 = cy - mr_inner * math.sin(mangle)
                mx1 = cx + mr_outer * math.cos(mangle)
                my1 = cy - mr_outer * math.sin(mangle)
                in_red_m = redline_start is not None and mval >= redline_start
                pygame.draw.line(surface, NEEDLE_RED if in_red_m else AMBER_DIM,
                                 (mx0, my0), (mx1, my1), 1)

    label_font = pygame.font.SysFont("sans", max(20, radius // 7), bold=True)
    lt = label_font.render(label, True, AMBER_DIM)
    surface.blit(lt, (cx - lt.get_width() / 2, cy + radius * 0.18))

    unit_font = pygame.font.SysFont("sans", max(14, radius // 10))
    ut = unit_font.render(unit, True, AMBER_DARK)
    surface.blit(ut, (cx - ut.get_width() / 2, cy + radius * 0.35))

    val_frac = max(0, min(1, (value - min_val) / (max_val - min_val)))
    needle_angle = math.radians(start_angle - val_frac * sweep)
    needle_len = radius - 30
    nx = cx + needle_len * math.cos(needle_angle)
    ny = cy - needle_len * math.sin(needle_angle)
    tail_len = radius * 0.15
    tx = cx - tail_len * math.cos(needle_angle)
    ty = cy + tail_len * math.sin(needle_angle)
    pygame.draw.line(surface, AMBER, (tx, ty), (nx, ny), 3)

    pygame.draw.circle(surface, AMBER, (cx, cy), 8)
    pygame.draw.circle(surface, BG, (cx, cy), 5)


def draw_bar_gauge(surface, x, y, w, h, value, min_val, max_val, label, unit):
    """Draw a horizontal bar gauge for oil/water temp style."""
    pygame.draw.rect(surface, AMBER_DARK, (x, y, w, h), 1)

    fill_frac = max(0, min(1, (value - min_val) / (max_val - min_val)))
    fill_w = int((w - 4) * fill_frac)
    if fill_w > 0:
        pygame.draw.rect(surface, AMBER, (x + 2, y + 2, fill_w, h - 4))

    font = pygame.font.SysFont("sans", 18, bold=True)
    lt = font.render(label, True, AMBER_DIM)
    surface.blit(lt, (x, y - 22))

    vt = font.render(f"{int(value)} {unit}", True, AMBER)
    surface.blit(vt, (x + w - vt.get_width(), y - 22))


def draw_title_bar(surface):
    """Draw top info bar."""
    font = pygame.font.SysFont("sans", 22, bold=True)
    t = font.render("R129  ·  500 SL  ·  AOK912", True, AMBER_DIM)
    surface.blit(t, (SCREEN_W // 2 - t.get_width() // 2, 12))

    small = pygame.font.SysFont("sans", 16)
    ts = small.render(time.strftime("%H:%M"), True, AMBER_DARK)
    surface.blit(ts, (SCREEN_W - ts.get_width() - 20, 14))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.FULLSCREEN)
    pygame.display.set_caption("R129 Driver UI")
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    t0 = time.time()
    running = True

    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN and ev.key in (pygame.K_ESCAPE, pygame.K_q):
                running = False
            elif ev.type == pygame.FINGERDOWN:
                running = False

        elapsed = time.time() - t0

        rpm = 800 + 400 * math.sin(elapsed * 0.3) + 200 * math.sin(elapsed * 0.7)
        speed = 60 + 30 * math.sin(elapsed * 0.2) + 10 * math.sin(elapsed * 0.5)
        oil_temp = 90 + 8 * math.sin(elapsed * 0.1)
        coolant_temp = 85 + 5 * math.sin(elapsed * 0.15)
        fuel = 65 + 10 * math.sin(elapsed * 0.05)
        volts = 13.8 + 0.3 * math.sin(elapsed * 0.4)

        screen.fill(BG)
        draw_title_bar(screen)

        tacho_x, tacho_y, tacho_r = 380, SCREEN_H // 2 + 20, 280
        draw_gauge(screen, tacho_x, tacho_y, tacho_r,
                   rpm / 1000, 0, 7,
                   "RPM", "× 1000",
                   [0, 1, 2, 3, 4, 5, 6, 7],
                   minor_per_major=4,
                   redline_start=6.2)

        speedo_x, speedo_y, speedo_r = SCREEN_W // 2, SCREEN_H // 2 + 20, 300
        draw_gauge(screen, speedo_x, speedo_y, speedo_r,
                   speed, 0, 260,
                   "km/h", "",
                   [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260],
                   minor_per_major=3)

        fuel_x, fuel_y, fuel_r = SCREEN_W - 380, SCREEN_H // 2 + 20, 280
        draw_gauge(screen, fuel_x, fuel_y, fuel_r,
                   coolant_temp, 40, 130,
                   "COOLANT", "°C",
                   [40, 60, 80, 100, 120, 130],
                   minor_per_major=4,
                   redline_start=110)

        bar_y = SCREEN_H - 80
        draw_bar_gauge(screen, 60, bar_y, 250, 20, oil_temp, 40, 150, "OIL TEMP", "°C")
        draw_bar_gauge(screen, 380, bar_y, 250, 20, fuel, 0, 100, "FUEL", "%")
        draw_bar_gauge(screen, SCREEN_W - 560, bar_y, 250, 20, volts, 10, 16, "VOLTAGE", "V")

        ads_font = pygame.font.SysFont("sans", 18, bold=True)
        ads_mode = "SPORT" if int(elapsed) % 10 < 5 else "COMFORT"
        ads_color = NEEDLE_RED if ads_mode == "SPORT" else AMBER
        at = ads_font.render(f"ADS: {ads_mode}", True, ads_color)
        screen.blit(at, (SCREEN_W - at.get_width() - 20, bar_y + 2))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
