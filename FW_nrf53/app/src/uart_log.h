#ifndef R129_UART_LOG_H_
#define R129_UART_LOG_H_

#include <stddef.h>
#include <stdint.h>

/* Human-readable heartbeat line on the console UART, one per tick:
 *   "R129-CTR <counter> uptime=<uptime_ms> ms\n"
 * Kept stable and greppable so capture scripts don't break. */
void r129_uart_log_heartbeat(uint32_t counter, uint32_t uptime_ms);

/* Hex dump of the encoded payload frame, one per tick:
 *   "R129-FRM AE 08 00 ... CC CC\n"
 * Useful when debugging the UART-side diagnostics path without a
 * BLE central attached. */
void r129_uart_log_frame(const uint8_t *frame, size_t len);

#endif /* R129_UART_LOG_H_ */
