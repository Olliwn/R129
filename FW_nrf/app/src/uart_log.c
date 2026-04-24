#include "uart_log.h"

#include <zephyr/sys/printk.h>

void r129_uart_log_heartbeat(uint32_t counter, uint32_t uptime_ms)
{
    printk("R129-CTR %u uptime=%u ms\n", counter, uptime_ms);
}

void r129_uart_log_frame(const uint8_t *frame, size_t len)
{
    if (frame == NULL || len == 0) {
        return;
    }
    printk("R129-FRM");
    for (size_t i = 0; i < len; i++) {
        printk(" %02X", frame[i]);
    }
    printk("\n");
}
