#include "r129_payload.h"

#include <string.h>

uint16_t r129_crc16(const uint8_t *data, size_t len)
{
    uint16_t crc = 0xFFFFU;
    if (data == NULL) {
        return crc;
    }
    for (size_t i = 0; i < len; i++) {
        crc ^= (uint16_t)((uint16_t)data[i] << 8);
        for (int b = 0; b < 8; b++) {
            if (crc & 0x8000U) {
                crc = (uint16_t)(((uint32_t)crc << 1) ^ 0x1021U);
            } else {
                crc = (uint16_t)((uint32_t)crc << 1);
            }
        }
    }
    return crc;
}

int r129_frame_encode(uint8_t type,
                      const void *data, uint8_t data_len,
                      uint8_t *out, size_t out_size)
{
    if (out == NULL) {
        return R129_ERR_NULL_ARG;
    }
    if (data_len > R129_MAX_DATA_LEN) {
        return R129_ERR_BAD_LENGTH;
    }
    if (data == NULL && data_len != 0) {
        return R129_ERR_NULL_ARG;
    }

    const size_t total = (size_t)R129_OVERHEAD + data_len;
    if (out_size < total) {
        return R129_ERR_OUT_TOO_SMALL;
    }

    out[0] = R129_SYNC;
    out[1] = data_len;
    out[2] = type;
    if (data_len > 0) {
        memcpy(&out[R129_HEADER_LEN], data, data_len);
    }

    const uint16_t crc = r129_crc16(out, (size_t)R129_HEADER_LEN + data_len);
    out[R129_HEADER_LEN + data_len]     = (uint8_t)(crc >> 8);
    out[R129_HEADER_LEN + data_len + 1] = (uint8_t)(crc & 0xFFU);

    return (int)total;
}

int r129_frame_peek_len(const uint8_t *in, size_t in_len)
{
    if (in == NULL) {
        return R129_ERR_NULL_ARG;
    }
    if (in_len < 2U) {
        return R129_ERR_TRUNCATED;
    }
    if (in[0] != R129_SYNC) {
        return R129_ERR_BAD_SYNC;
    }
    if (in[1] > R129_MAX_DATA_LEN) {
        return R129_ERR_BAD_LENGTH;
    }
    return (int)R129_OVERHEAD + in[1];
}

int r129_frame_decode(const uint8_t *in, size_t in_len,
                      uint8_t *out_type,
                      uint8_t *out_data_len,
                      uint8_t *data_out, size_t data_out_size)
{
    if (in == NULL || out_type == NULL || out_data_len == NULL) {
        return R129_ERR_NULL_ARG;
    }

    int peek = r129_frame_peek_len(in, in_len);
    if (peek < 0) {
        return peek;
    }
    const size_t total = (size_t)peek;
    if (in_len < total) {
        return R129_ERR_TRUNCATED;
    }

    const uint8_t data_len = in[1];
    const uint8_t type     = in[2];
    const uint16_t rx_crc  = (uint16_t)(
                                 ((uint16_t)in[R129_HEADER_LEN + data_len]     << 8) |
                                  (uint16_t)in[R129_HEADER_LEN + data_len + 1]);
    const uint16_t want    = r129_crc16(in, (size_t)R129_HEADER_LEN + data_len);
    if (rx_crc != want) {
        return R129_ERR_BAD_CRC;
    }

    if (data_len > 0) {
        if (data_out == NULL || data_out_size < data_len) {
            return R129_ERR_OUT_TOO_SMALL;
        }
        memcpy(data_out, &in[R129_HEADER_LEN], data_len);
    }

    *out_type     = type;
    *out_data_len = data_len;
    return (int)total;
}
