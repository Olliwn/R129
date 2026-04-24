/*
 * Host-side round-trip + edge-case tests for r129_payload.c.
 *
 * Build: cc -std=c99 -Wall -Wextra -Wpedantic -Werror \
 *           -I../payload ../payload/r129_payload.c test_payload.c \
 *           -o test_payload
 *
 * Or just `make` in this directory.
 */

#include "r129_payload.h"

#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int g_fail = 0;

#define CHECK(cond) do { \
    if (!(cond)) { \
        fprintf(stderr, "FAIL: %s:%d: %s\n", __FILE__, __LINE__, #cond); \
        g_fail++; \
    } \
} while (0)

#define CHECK_EQ(a, b) do { \
    long long _a = (long long)(a); \
    long long _b = (long long)(b); \
    if (_a != _b) { \
        fprintf(stderr, "FAIL: %s:%d: %s == %s (got %lld vs %lld)\n", \
                __FILE__, __LINE__, #a, #b, _a, _b); \
        g_fail++; \
    } \
} while (0)

static void test_crc_known_vector(void)
{
    /* Standard CRC-16/CCITT-FALSE check value: crc("123456789") = 0x29B1. */
    const uint8_t s[] = "123456789";
    uint16_t crc = r129_crc16(s, 9);
    CHECK_EQ(crc, 0x29B1);

    /* Empty -> init value. */
    CHECK_EQ(r129_crc16(NULL, 0), 0xFFFF);

    /* Single-bit sensitivity. */
    uint8_t a = 0x00, b = 0x01;
    CHECK(r129_crc16(&a, 1) != r129_crc16(&b, 1));
}

static void test_heartbeat_roundtrip(void)
{
    r129_heartbeat_t hb_in = { .uptime_ms = 0x12345678, .counter = 0xDEADBEEF };
    uint8_t buf[R129_MAX_FRAME_LEN];

    int n = r129_frame_encode(R129_TYPE_HEARTBEAT, &hb_in, sizeof(hb_in),
                              buf, sizeof(buf));
    CHECK_EQ(n, (int)(R129_OVERHEAD + sizeof(hb_in)));  /* 5 + 8 = 13 */
    CHECK_EQ(buf[0], R129_SYNC);
    CHECK_EQ(buf[1], sizeof(hb_in));
    CHECK_EQ(buf[2], R129_TYPE_HEARTBEAT);

    /* Little-endian check on the data section. */
    CHECK_EQ(buf[3], 0x78);  /* uptime_ms LSB */
    CHECK_EQ(buf[6], 0x12);  /* uptime_ms MSB */
    CHECK_EQ(buf[7], 0xEF);  /* counter LSB */
    CHECK_EQ(buf[10], 0xDE); /* counter MSB */

    uint8_t type = 0, dl = 0;
    uint8_t out[sizeof(r129_heartbeat_t)];
    int consumed = r129_frame_decode(buf, (size_t)n, &type, &dl, out, sizeof(out));
    CHECK_EQ(consumed, n);
    CHECK_EQ(type, R129_TYPE_HEARTBEAT);
    CHECK_EQ(dl, sizeof(hb_in));

    r129_heartbeat_t hb_out;
    memcpy(&hb_out, out, sizeof(hb_out));
    CHECK_EQ(hb_out.uptime_ms, hb_in.uptime_ms);
    CHECK_EQ(hb_out.counter, hb_in.counter);
}

static void test_zero_length_payload(void)
{
    uint8_t buf[R129_MAX_FRAME_LEN];
    int n = r129_frame_encode(R129_TYPE_CMD_CLEAR, NULL, 0, buf, sizeof(buf));
    CHECK_EQ(n, (int)R129_OVERHEAD);  /* exactly 5 bytes */

    uint8_t type = 0, dl = 0xFF;
    int consumed = r129_frame_decode(buf, (size_t)n, &type, &dl, NULL, 0);
    CHECK_EQ(consumed, n);
    CHECK_EQ(type, R129_TYPE_CMD_CLEAR);
    CHECK_EQ(dl, 0);
}

static void test_max_length_payload(void)
{
    uint8_t payload[R129_MAX_DATA_LEN];
    for (size_t i = 0; i < sizeof(payload); i++) {
        payload[i] = (uint8_t)(i * 31u + 7u);  /* arbitrary pattern */
    }
    uint8_t buf[R129_MAX_FRAME_LEN];
    int n = r129_frame_encode(R129_TYPE_ANALOG, payload, sizeof(payload),
                              buf, sizeof(buf));
    CHECK_EQ(n, (int)R129_MAX_FRAME_LEN);

    uint8_t type = 0, dl = 0;
    uint8_t out[R129_MAX_DATA_LEN];
    int consumed = r129_frame_decode(buf, (size_t)n, &type, &dl,
                                     out, sizeof(out));
    CHECK_EQ(consumed, n);
    CHECK_EQ(dl, R129_MAX_DATA_LEN);
    CHECK(memcmp(out, payload, sizeof(payload)) == 0);
}

static void test_buffer_too_small(void)
{
    uint8_t buf[4];  /* can't even fit the 5-byte overhead */
    int n = r129_frame_encode(R129_TYPE_HEARTBEAT, NULL, 0, buf, sizeof(buf));
    CHECK_EQ(n, R129_ERR_OUT_TOO_SMALL);

    uint8_t big[R129_MAX_FRAME_LEN];
    n = r129_frame_encode(R129_TYPE_HEARTBEAT, "xx", 2, big, 6);  /* need 7 */
    CHECK_EQ(n, R129_ERR_OUT_TOO_SMALL);
}

static void test_over_max_length(void)
{
    uint8_t buf[R129_MAX_FRAME_LEN + 16];
    int n = r129_frame_encode(R129_TYPE_ANALOG, buf, R129_MAX_DATA_LEN + 1,
                              buf, sizeof(buf));
    CHECK_EQ(n, R129_ERR_BAD_LENGTH);
}

static void test_bad_sync(void)
{
    uint8_t buf[R129_MAX_FRAME_LEN];
    int n = r129_frame_encode(R129_TYPE_HEARTBEAT, "ab", 2, buf, sizeof(buf));
    CHECK(n > 0);
    buf[0] = 0x00;  /* trash sync byte */

    uint8_t type, dl, out[4];
    int rc = r129_frame_decode(buf, (size_t)n, &type, &dl, out, sizeof(out));
    CHECK_EQ(rc, R129_ERR_BAD_SYNC);
}

static void test_bad_crc(void)
{
    uint8_t buf[R129_MAX_FRAME_LEN];
    int n = r129_frame_encode(R129_TYPE_HEARTBEAT, "ab", 2, buf, sizeof(buf));
    CHECK(n > 0);
    buf[3] ^= 0x01;  /* corrupt data byte, CRC no longer matches */

    uint8_t type, dl, out[4];
    int rc = r129_frame_decode(buf, (size_t)n, &type, &dl, out, sizeof(out));
    CHECK_EQ(rc, R129_ERR_BAD_CRC);
}

static void test_truncated(void)
{
    uint8_t buf[R129_MAX_FRAME_LEN];
    int n = r129_frame_encode(R129_TYPE_HEARTBEAT, "abcd", 4, buf, sizeof(buf));
    CHECK(n > 0);

    uint8_t type, dl, out[8];

    /* Header only — not even the full length/type yet. */
    int rc = r129_frame_decode(buf, 1, &type, &dl, out, sizeof(out));
    CHECK_EQ(rc, R129_ERR_TRUNCATED);

    /* Length says 4 data + CRC, but we hand over fewer bytes. */
    rc = r129_frame_decode(buf, (size_t)(n - 1), &type, &dl, out, sizeof(out));
    CHECK_EQ(rc, R129_ERR_TRUNCATED);

    /* Exact length -> success. */
    rc = r129_frame_decode(buf, (size_t)n, &type, &dl, out, sizeof(out));
    CHECK_EQ(rc, n);
    CHECK_EQ(dl, 4);
}

static void test_peek_len(void)
{
    uint8_t buf[R129_MAX_FRAME_LEN];
    int n = r129_frame_encode(R129_TYPE_HEARTBEAT, "xyz", 3, buf, sizeof(buf));
    CHECK(n > 0);

    CHECK_EQ(r129_frame_peek_len(buf, 2), n);  /* just the first two bytes suffice */
    CHECK_EQ(r129_frame_peek_len(buf, 1), R129_ERR_TRUNCATED);
    uint8_t bad[] = { 0xFF, 0x00 };
    CHECK_EQ(r129_frame_peek_len(bad, 2), R129_ERR_BAD_SYNC);
    uint8_t too_long[] = { R129_SYNC, (uint8_t)(R129_MAX_DATA_LEN + 1) };
    CHECK_EQ(r129_frame_peek_len(too_long, 2), R129_ERR_BAD_LENGTH);
}

static void test_back_to_back_encoded_frames(void)
{
    /* Simulate a small TLV byte stream: two frames back-to-back,
     * decoded sequentially. This is how the RPi5 will consume UART data. */
    uint8_t stream[2 * R129_MAX_FRAME_LEN];
    r129_heartbeat_t hb1 = { .uptime_ms = 1000, .counter = 1 };
    r129_heartbeat_t hb2 = { .uptime_ms = 2000, .counter = 2 };

    int n1 = r129_frame_encode(R129_TYPE_HEARTBEAT, &hb1, sizeof(hb1),
                               stream, sizeof(stream));
    CHECK(n1 > 0);
    int n2 = r129_frame_encode(R129_TYPE_HEARTBEAT, &hb2, sizeof(hb2),
                               stream + n1, sizeof(stream) - (size_t)n1);
    CHECK(n2 > 0);

    size_t pos = 0;
    uint8_t type, dl, data[sizeof(r129_heartbeat_t)];
    r129_heartbeat_t out;

    int c = r129_frame_decode(stream + pos, (size_t)(n1 + n2 - (int)pos),
                              &type, &dl, data, sizeof(data));
    CHECK_EQ(c, n1);
    memcpy(&out, data, sizeof(out));
    CHECK_EQ(out.counter, 1);
    pos += (size_t)c;

    c = r129_frame_decode(stream + pos, (size_t)(n1 + n2) - pos,
                          &type, &dl, data, sizeof(data));
    CHECK_EQ(c, n2);
    memcpy(&out, data, sizeof(out));
    CHECK_EQ(out.counter, 2);
    pos += (size_t)c;

    CHECK_EQ(pos, (size_t)(n1 + n2));
}

int main(void)
{
    test_crc_known_vector();
    test_heartbeat_roundtrip();
    test_zero_length_payload();
    test_max_length_payload();
    test_buffer_too_small();
    test_over_max_length();
    test_bad_sync();
    test_bad_crc();
    test_truncated();
    test_peek_len();
    test_back_to_back_encoded_frames();

    if (g_fail == 0) {
        printf("all tests passed\n");
        return 0;
    }
    fprintf(stderr, "%d test check(s) failed\n", g_fail);
    return 1;
}
