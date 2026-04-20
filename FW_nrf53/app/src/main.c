/*
 * R129 Diagnostics Node - application entry.
 *
 * Boots the BLE stack, advertises as "R129-Diag", and at 1 Hz emits
 * an R129_TYPE_HEARTBEAT framed payload on two paths:
 *   - BLE GATT notify  (diagnostics stream characteristic)
 *   - console UART     (hex dump + human-readable line)
 *
 * Any future telemetry type (analog sensors, blink codes, commands)
 * plugs into the same wire format - see payload/r129_payload.h.
 */

#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>

#include "ble_diag.h"
#include "r129_payload.h"
#include "uart_log.h"

LOG_MODULE_REGISTER(r129_main, LOG_LEVEL_INF);

#define TICK_PERIOD K_SECONDS(1)

int main(void)
{
    LOG_INF("R129 diagnostics node booting (M1 framed payload)");

    int err = r129_ble_diag_start();
    if (err) {
        LOG_ERR("ble start failed (%d) - halting", err);
        return err;
    }

    uint32_t counter = 0;
    uint8_t  frame[R129_OVERHEAD + sizeof(r129_heartbeat_t)];

    while (1) {
        r129_heartbeat_t hb = {
            .uptime_ms = (uint32_t)k_uptime_get_32(),
            .counter   = counter,
        };

        int n = r129_frame_encode(R129_TYPE_HEARTBEAT, &hb, sizeof(hb),
                                  frame, sizeof(frame));
        if (n < 0) {
            LOG_ERR("frame encode failed (%d)", n);
        } else {
            r129_uart_log_heartbeat(hb.counter, hb.uptime_ms);
            r129_uart_log_frame(frame, (size_t)n);
            r129_ble_diag_notify_frame(frame, (size_t)n);
        }

        counter++;
        k_sleep(TICK_PERIOD);
    }

    return 0;
}
