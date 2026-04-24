/*
 * R129 diagnostics wire format - portable C99, no dependencies beyond
 * <stdint.h> / <stddef.h>. Shared by the nRF5340 firmware (app/src/) and
 * the host-side unit tests (host_test/). Same source compiles under
 * Zephyr arm-zephyr-eabi and host clang/gcc unchanged.
 *
 * Frame layout (on-wire, big-endian CRC for dump readability):
 *
 *   offset  field   bytes   notes
 *   0       SYNC    1       = 0xAE
 *   1       LEN     1       = N (Data byte count; 0..R129_MAX_DATA_LEN)
 *   2       TYPE    1       r129_type_t
 *   3..2+N  DATA    N       type-specific payload
 *   3+N     CRC_HI  1       CRC-16/CCITT-FALSE MSB, over SYNC..DATA
 *   4+N     CRC_LO  1       CRC-16/CCITT-FALSE LSB
 *   total = 5 + N bytes
 *
 * Integer fields inside DATA (e.g. uint32 counters, int16 ADC samples)
 * are little-endian. The CRC itself is big-endian so a raw hex dump
 * reads left-to-right in the same order a human would write it.
 *
 * Fits within the 247-byte configured BLE ATT MTU with R129_MAX_DATA_LEN
 * set at 240. Also fits comfortably in a legacy 20-byte MTU for small
 * payloads (HEARTBEAT: 9 bytes total).
 */

#ifndef R129_PAYLOAD_H_
#define R129_PAYLOAD_H_

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Framing constants ---------------------------------------------------------*/
#define R129_SYNC           ((uint8_t)0xAE)
#define R129_HEADER_LEN     3U   /* SYNC + LEN + TYPE */
#define R129_CRC_LEN        2U
#define R129_OVERHEAD       (R129_HEADER_LEN + R129_CRC_LEN)
#define R129_MAX_DATA_LEN   240U
#define R129_MAX_FRAME_LEN  (R129_OVERHEAD + R129_MAX_DATA_LEN)

/* Payload type enum. Values are wire constants - do not renumber. */
typedef enum {
    R129_TYPE_HEARTBEAT = 0x00,  /* see r129_heartbeat_t */
    R129_TYPE_ANALOG    = 0x02,  /* reserved, M3 */
    R129_TYPE_BLINK     = 0x03,  /* reserved, M4 */
    R129_TYPE_CMD_CLEAR = 0x10,  /* reserved, M4 */
} r129_type_t;

typedef enum {
    R129_OK                = 0,
    R129_ERR_OUT_TOO_SMALL = -1,
    R129_ERR_BAD_SYNC      = -2,
    R129_ERR_BAD_CRC       = -3,
    R129_ERR_TRUNCATED     = -4,
    R129_ERR_BAD_LENGTH    = -5,
    R129_ERR_NULL_ARG      = -6,
} r129_err_t;

/* Fixed payload layouts ----------------------------------------------------*/
/* HEARTBEAT (8 bytes): uptime + counter. Sent at 1 Hz as the M0/M1
 * keep-alive. Host uses the counter to detect dropped notifications and
 * the uptime to detect reboots. Byte order: little-endian. */
typedef struct {
    uint32_t uptime_ms;   /* le */
    uint32_t counter;     /* le */
} r129_heartbeat_t;

/* Public API ---------------------------------------------------------------*/

/* Compute CRC-16/CCITT-FALSE over `data[0..len)`. Poly 0x1021, init 0xFFFF,
 * no reflection, xor-out 0x0000. Standard check value: crc16("123456789") = 0x29B1. */
uint16_t r129_crc16(const uint8_t *data, size_t len);

/* Encode one frame into `out[0..out_size)`. `data` may be NULL iff `data_len` is 0.
 * Returns the number of bytes written (>= R129_OVERHEAD) on success, or a negative
 * r129_err_t value on error. */
int r129_frame_encode(uint8_t type,
                      const void *data, uint8_t data_len,
                      uint8_t *out, size_t out_size);

/* Decode one frame from `in[0..in_len)`. On success fills *out_type, *out_data_len,
 * and copies the payload into data_out[0..*out_data_len) (if data_out != NULL and
 * data_out_size is large enough). Returns total consumed bytes (>= R129_OVERHEAD),
 * or a negative r129_err_t on error. Use `r129_frame_peek_len` to size data_out. */
int r129_frame_decode(const uint8_t *in, size_t in_len,
                      uint8_t *out_type,
                      uint8_t *out_data_len,
                      uint8_t *data_out, size_t data_out_size);

/* Cheap prefix check: returns the declared total frame length (>= R129_OVERHEAD)
 * if the first two bytes are plausibly a frame header, else a negative
 * r129_err_t. Does not validate the CRC - useful for stream re-synchronization. */
int r129_frame_peek_len(const uint8_t *in, size_t in_len);

#ifdef __cplusplus
}
#endif

#endif /* R129_PAYLOAD_H_ */
