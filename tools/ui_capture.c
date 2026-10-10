// SPDX-License-Identifier: GPL-3.0-only
/* Capture the real LVGL UI into a memory framebuffer, without device access. */
#include "ui.h"
#include "lvgl.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static lv_color_t pixels[EPD_WIDTH * EPD_HEIGHT];
static lv_color_t draw_buffer[EPD_WIDTH * EPD_HEIGHT];
static unsigned int flushes;

/* Fixed demo clock. Only this host executable overrides time(). */
time_t time(time_t *result)
{
    const time_t demo_time = 1791599400; /* 2026-10-10 10:30 CST */
    if (result) *result = demo_time;
    return demo_time;
}
uint32_t custom_tick_get(void) { static uint32_t tick; return ++tick; }

static void flush(lv_disp_drv_t *driver, const lv_area_t *area, lv_color_t *colors)
{
    for (int y = area->y1; y <= area->y2; y++)
        for (int x = area->x1; x <= area->x2; x++) {
            if (x >= 0 && x < (int)EPD_WIDTH && y >= 0 && y < (int)EPD_HEIGHT)
                pixels[y * EPD_WIDTH + x] = *colors;
            colors++;
        }
    flushes++;
    lv_disp_flush_ready(driver);
}

static void save(const char *directory, const char *name)
{
    char path[1024];
    snprintf(path, sizeof(path), "%s/%s.pgm", directory, name);
    FILE *file = fopen(path, "wb");
    if (!file) { perror(path); exit(1); }
    fprintf(file, "P5\n%u %u\n255\n", EPD_WIDTH, EPD_HEIGHT);
    for (unsigned int i = 0; i < EPD_WIDTH * EPD_HEIGHT; i++) {
        unsigned int c = lv_color_to16(pixels[i]);
        unsigned int r = ((c >> 11) & 31) * 255 / 31;
        unsigned int g = ((c >> 5) & 63) * 255 / 63;
        unsigned int b = (c & 31) * 255 / 31;
        /* Same threshold as platforms/tina/epd_disp.c. */
        fputc(((r * 77 + g * 150 + b * 29) >> 8) >= 128 ? 255 : 0, file);
    }
    if (fclose(file)) { perror(path); exit(1); }
}

int main(int argc, char **argv)
{
    if (argc != 2) { fprintf(stderr, "usage: ui-capture OUTPUT_DIRECTORY\n"); return 2; }
    setenv("TZ", "CST-8", 1); tzset(); lv_init();
    static lv_disp_draw_buf_t buffer;
    static lv_disp_drv_t driver;
    lv_disp_draw_buf_init(&buffer, draw_buffer, NULL, EPD_WIDTH * EPD_HEIGHT);
    lv_disp_drv_init(&driver);
    driver.hor_res = EPD_WIDTH; driver.ver_res = EPD_HEIGHT;
    driver.draw_buf = &buffer; driver.flush_cb = flush;
    driver.full_refresh = 1; driver.antialiasing = 0;
    lv_disp_t *display = lv_disp_drv_register(&driver);
    desktop_ui_init();
    struct dashboard_settings settings;
    settings_defaults(&settings);
    struct system_stats stats = { .cpu_percent = 8, .load_average = .12,
        .memory_total_kb = 128 * 1024, .memory_available_kb = 86 * 1024,
        .storage_available_kb = 180 * 1024, .temperature_millic = 42000, .uptime_sec = 7200 };
    strcpy(stats.hostname, "EinkOS"); strcpy(stats.kernel, "5.4.61");
    strcpy(stats.interface, "wlan0"); strcpy(stats.ip_address, "192.0.2.20");
    struct epd_100ask_info epd = { .width = 240, .height = 360, .frame_size = 10800,
        .full_refreshes = 12, .partial_refreshes = 83, .skipped_refreshes = 4 };
    struct reader_state reader = {0};
    struct eink_connect_status connect = { .magic = EINK_CONNECT_MAGIC,
        .version = EINK_CONNECT_VERSION, .wifi_mode = EINK_WIFI_STA,
        .wifi_connected = 1, .bt_state = EINK_BT_ON, .wifi_count = 3, .bt_count = 2 };
    strcpy(connect.wifi_ssid, "EinkOS-Demo"); strcpy(connect.ip_address, "192.0.2.20");
    strcpy(connect.wifi[0].ssid, "EinkOS-Demo"); connect.wifi[0].signal = -42;
    strcpy(connect.wifi[1].ssid, "Reading-Room"); connect.wifi[1].signal = -58;
    strcpy(connect.wifi[2].ssid, "Guest"); connect.wifi[2].signal = -71;
    strcpy(connect.bt[0].name, "Demo Keyboard"); connect.bt[0].paired = 1; connect.bt[0].connected = 1;
    strcpy(connect.bt[1].name, "Demo Phone");
    enum eink_time_quality quality = EINK_TIME_ACCURATE;
    int error = 0;
#define CAPTURE(name, screen, selection, offset) do { \
    unsigned int previous = flushes; \
    desktop_ui_render(screen, selection, offset, &settings, &stats, &epd, &reader, &connect, quality, error); \
    lv_refr_now(display); \
    if (flushes == previous) { fprintf(stderr, "No rendered frame: %s\n", name); return 1; } \
    save(argv[1], name); \
} while (0)
    CAPTURE("01-home", DESKTOP_HOME, 0, 0);
    settings.language = DASH_LANG_EN;
    CAPTURE("02-home-en", DESKTOP_HOME, 1, 0);
    settings.language = DASH_LANG_ZH;
    quality = EINK_TIME_RESTORED; CAPTURE("03-time-restored", DESKTOP_HOME, 0, 0);
    quality = EINK_TIME_INVALID; CAPTURE("04-time-unset", DESKTOP_HOME, 0, 0);
    quality = EINK_TIME_ACCURATE;
    CAPTURE("05-calendar", DESKTOP_CALENDAR, 0, 0);
    CAPTURE("06-calendar-next", DESKTOP_CALENDAR, 0, 1);
    CAPTURE("07-reader-empty", DESKTOP_READER, 0, 0);
    reader.file_count = 3; reader.selection = 0;
    strcpy(reader.files[0].name, "墨水屏阅读示例.txt");
    strcpy(reader.files[1].name, "使用指南.txt"); strcpy(reader.files[2].name, "每日笔记.txt");
    CAPTURE("08-library", DESKTOP_READER, 0, 0);
    reader.opened = 1;
    size_t offsets[] = {0}; reader.page_offsets = offsets;
    strcpy(reader.page, "这是 EinkOS 的阅读页面。\n\n黑白文字，安静阅读。\n\n按 K1 / K3 向前或向后\n翻页，按 K2 打开菜单。\n\n阅读位置可以自动保存，\n下次打开继续阅读。\n\n此处为截图演示文本。");
    CAPTURE("09-reader", DESKTOP_READER, 0, 0);
    reader.bookmark_set = 1; CAPTURE("10-reader-bookmark", DESKTOP_READER, 0, 0);
    reader.action_menu = 1; reader.action_selection = 1;
    CAPTURE("11-reader-menu", DESKTOP_READER, 0, 0);
    CAPTURE("12-connect", DESKTOP_CONNECT, 0, 0);
    CAPTURE("13-wifi", DESKTOP_WIFI, 1, 0);
    connect.wifi_mode = EINK_WIFI_PORTAL; connect.wifi_connected = 0;
    connect.portal_seconds_left = 285;
    strcpy(connect.portal_ssid, "EINKOS-DEMO"); strcpy(connect.portal_password, "12345678");
    CAPTURE("14-wifi-portal", DESKTOP_WIFI, 0, 0);
    connect.wifi_mode = EINK_WIFI_STA; strcpy(connect.message, "连接失败");
    CAPTURE("15-wifi-failure", DESKTOP_WIFI, 0, 0);
    connect.wifi_connected = 1; connect.message[0] = 0;
    CAPTURE("16-bluetooth", DESKTOP_BLUETOOTH, 2, 0);
    connect.bt_state = EINK_BT_SCANNING;
    CAPTURE("17-bluetooth-scan", DESKTOP_BLUETOOTH, 1, 0);
    connect.bt_state = EINK_BT_ON; connect.pair_pending = 1;
    strcpy(connect.pair_device, "Demo Keyboard"); connect.pair_passkey = 123456;
    CAPTURE("18-bluetooth-confirm", DESKTOP_BLUETOOTH, 0, 0);
    connect.pair_input = 2; connect.pair_cursor = 2;
    CAPTURE("19-bluetooth-pin", DESKTOP_BLUETOOTH, 0, 0);
    connect.pair_pending = 0; connect.bt_state = EINK_BT_UNAVAILABLE; connect.bt_count = 0;
    CAPTURE("20-bluetooth-unavailable", DESKTOP_BLUETOOTH, 0, 0);
    CAPTURE("21-more", DESKTOP_MORE, 0, 0);
    CAPTURE("22-resources", DESKTOP_RESOURCES, 0, 0);
    CAPTURE("23-diagnostics", DESKTOP_DIAGNOSTICS, 0, 0);
    error = 5; CAPTURE("24-diagnostics-error", DESKTOP_DIAGNOSTICS, 0, 0); error = 0;
    CAPTURE("25-settings", DESKTOP_SETTINGS, 0, 0);
    CAPTURE("26-about", DESKTOP_ABOUT, 0, 0);
    return 0;
}
