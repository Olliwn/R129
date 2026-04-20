#include "ble_diag.h"

#include <string.h>

#include <zephyr/bluetooth/bluetooth.h>
#include <zephyr/bluetooth/conn.h>
#include <zephyr/bluetooth/gatt.h>
#include <zephyr/bluetooth/hci.h>
#include <zephyr/logging/log.h>
#include <zephyr/sys/byteorder.h>

#include "r129_payload.h"

LOG_MODULE_REGISTER(r129_ble, LOG_LEVEL_INF);

static bool notify_enabled;

/* Last notified frame, so a plain GATT read returns the most recent
 * heartbeat rather than nothing. Sized for the worst case. */
static uint8_t   last_frame[R129_MAX_FRAME_LEN];
static uint16_t  last_frame_len;

static void stream_ccc_cfg_changed(const struct bt_gatt_attr *attr, uint16_t value)
{
    ARG_UNUSED(attr);
    notify_enabled = (value == BT_GATT_CCC_NOTIFY);
    LOG_INF("diag notifications %s", notify_enabled ? "enabled" : "disabled");
}

static ssize_t stream_read(struct bt_conn *conn,
                           const struct bt_gatt_attr *attr,
                           void *buf, uint16_t len, uint16_t offset)
{
    return bt_gatt_attr_read(conn, attr, buf, len, offset,
                             last_frame, last_frame_len);
}

BT_GATT_SERVICE_DEFINE(r129_svc,
    BT_GATT_PRIMARY_SERVICE(R129_UUID_SERVICE),
    BT_GATT_CHARACTERISTIC(R129_UUID_DIAG_STREAM,
                           BT_GATT_CHRC_READ | BT_GATT_CHRC_NOTIFY,
                           BT_GATT_PERM_READ,
                           stream_read, NULL, NULL),
    BT_GATT_CCC(stream_ccc_cfg_changed,
                BT_GATT_PERM_READ | BT_GATT_PERM_WRITE),
);

static const struct bt_data ad[] = {
    BT_DATA_BYTES(BT_DATA_FLAGS, (BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR)),
    BT_DATA(BT_DATA_NAME_COMPLETE, "R129-Diag", 9),
};

static const struct bt_data sd[] = {
    BT_DATA_BYTES(BT_DATA_UUID128_ALL, R129_UUID_SERVICE_VAL),
};

static void connected(struct bt_conn *conn, uint8_t err)
{
    if (err) {
        LOG_WRN("connect failed (err 0x%02x)", err);
        return;
    }
    LOG_INF("central connected");
}

static void restart_adv_work_fn(struct k_work *work)
{
    ARG_UNUSED(work);
    int err = bt_le_adv_start(BT_LE_ADV_CONN_FAST_1,
                              ad, ARRAY_SIZE(ad),
                              sd, ARRAY_SIZE(sd));
    if (err && err != -EALREADY) {
        LOG_ERR("adv restart failed (%d)", err);
    } else if (!err) {
        LOG_INF("advertising resumed");
    }
}
static K_WORK_DEFINE(restart_adv_work, restart_adv_work_fn);

static void disconnected(struct bt_conn *conn, uint8_t reason)
{
    LOG_INF("central disconnected (reason 0x%02x)", reason);
    notify_enabled = false;
    /* bt_le_adv_start cannot run from this callback context, so defer. */
    k_work_submit(&restart_adv_work);
}

BT_CONN_CB_DEFINE(conn_callbacks) = {
    .connected = connected,
    .disconnected = disconnected,
};

int r129_ble_diag_start(void)
{
    int err = bt_enable(NULL);
    if (err) {
        LOG_ERR("bt_enable failed (%d)", err);
        return err;
    }

    err = bt_le_adv_start(BT_LE_ADV_CONN_FAST_1,
                          ad, ARRAY_SIZE(ad),
                          sd, ARRAY_SIZE(sd));
    if (err) {
        LOG_ERR("bt_le_adv_start failed (%d)", err);
        return err;
    }

    LOG_INF("advertising as R129-Diag");
    return 0;
}

void r129_ble_diag_notify_frame(const uint8_t *frame, size_t len)
{
    if (frame == NULL || len == 0 || len > sizeof(last_frame)) {
        return;
    }

    memcpy(last_frame, frame, len);
    last_frame_len = (uint16_t)len;

    if (!notify_enabled) {
        return;
    }

    /* Attribute index 2 is the value handle of the diag stream characteristic
     * (0 = service, 1 = char decl, 2 = char value, 3 = CCC). */
    int err = bt_gatt_notify(NULL, &r129_svc.attrs[2], frame, (uint16_t)len);
    if (err && err != -ENOTCONN) {
        LOG_WRN("notify failed (%d)", err);
    }
}
