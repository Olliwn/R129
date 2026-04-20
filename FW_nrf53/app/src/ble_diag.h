/*
 * R129 Diagnostics BLE service.
 *
 * One custom GATT service with one notify characteristic. From M1 on
 * the notify payload is a framed r129_payload_t (see payload/r129_payload.h);
 * M0 raw-uint32 is retired. Keeping the same UUID on purpose - the "shape"
 * of telemetry was always meant to change here, the service identity was
 * not.
 */

#ifndef R129_BLE_DIAG_H_
#define R129_BLE_DIAG_H_

#include <stddef.h>
#include <stdint.h>
#include <zephyr/bluetooth/uuid.h>

/* Base UUID: a729xxxx-5231-3239-a7e1-524531323900
 *   5231 3239  = ASCII "R1" "29"
 *   a729, a7e1 = project-specific tag
 *
 * Little-endian byte order for BT_UUID_128_ENCODE.
 */
#define R129_UUID_SERVICE_VAL \
    BT_UUID_128_ENCODE(0xa7290001, 0x5231, 0x3239, 0xa7e1, 0x524531323900)

#define R129_UUID_DIAG_STREAM_VAL \
    BT_UUID_128_ENCODE(0xa7290002, 0x5231, 0x3239, 0xa7e1, 0x524531323900)

#define R129_UUID_SERVICE     BT_UUID_DECLARE_128(R129_UUID_SERVICE_VAL)
#define R129_UUID_DIAG_STREAM BT_UUID_DECLARE_128(R129_UUID_DIAG_STREAM_VAL)

/* Start advertising and register the service. Returns 0 on success. */
int r129_ble_diag_start(void);

/* Notify an already-encoded frame to subscribed centrals. Safe to call
 * when nobody is subscribed (returns quietly). Non-blocking. */
void r129_ble_diag_notify_frame(const uint8_t *frame, size_t len);

#endif /* R129_BLE_DIAG_H_ */
