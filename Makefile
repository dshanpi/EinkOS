# EinkOS user-space build. No dependency on a fixed SDK directory layout.
.DEFAULT_GOAL := all
CC ?= cc
HOSTCC ?= cc
PLATFORM ?= tina
LVGL_DIR ?= third_party/lvgl
BUILD_DIR ?= build
SYSROOT ?=
BT_INCLUDE_DIR ?= $(if $(SYSROOT),$(SYSROOT)/usr/include)
VERSION := $(shell cat VERSION)
COMMIT ?= $(shell cat SOURCE_COMMIT 2>/dev/null || git rev-parse HEAD 2>/dev/null || echo source)
SOURCE_DATE_EPOCH ?= $(shell cat SOURCE_DATE_EPOCH 2>/dev/null || git log -1 --format=%ct 2>/dev/null || echo 0)
BUILD_EPOCH ?= $(SOURCE_DATE_EPOCH)
STATIC ?= 0

ifneq ($(PLATFORM),tina)
$(error Supported platform: tina)
endif

override CPPFLAGS += -Isrc -Iinclude/uapi -I$(BUILD_DIR)/generated -I$(LVGL_DIR) -I$(LVGL_DIR)/.. -DLV_CONF_INCLUDE_SIMPLE -DLV_LVGL_H_INCLUDE_SIMPLE
CFLAGS ?= -O2
override CFLAGS += -Wall -Wextra -Werror=implicit-function-declaration -MMD -MP
LDLIBS += -lm -lpthread
ifneq ($(SYSROOT),)
override CPPFLAGS += --sysroot=$(SYSROOT)
override LDFLAGS += --sysroot=$(SYSROOT)
endif
ifeq ($(STATIC),1)
override LDFLAGS += -static
endif

APP_SRCS := $(addprefix src/,main.c connect_client.c input.c lunar.c reader.c settings.c system_stats.c tick.c time_state.c ui.c font_cjk_16.c) platforms/tina/epd_disp.c
CONNECT_SRCS := platforms/tina/connectd.c src/time_state.c src/wifi_results.c
LVGL_SRCS := $(foreach dir,core draw draw/sw font hal misc widgets,$(wildcard $(LVGL_DIR)/src/$(dir)/*.c)) $(LVGL_DIR)/src/extra/lv_extra.c
APP_OBJS := $(patsubst %.c,$(BUILD_DIR)/app/%.o,$(APP_SRCS))
CONNECT_OBJS := $(patsubst %.c,$(BUILD_DIR)/connect/%.o,$(CONNECT_SRCS))
LVGL_OBJS := $(patsubst $(LVGL_DIR)/%.c,$(BUILD_DIR)/lvgl/%.o,$(LVGL_SRCS))
TEST_NAMES := lunar reader protocol settings wifi_results
TEST_BINS := $(addprefix $(BUILD_DIR)/tests/,$(TEST_NAMES))

.PHONY: all clean test install FORCE
all: eink-dashboard eink-connectd

$(BUILD_DIR)/generated/version.h: FORCE
	@mkdir -p $(@D)
	@printf '#define EINK_VERSION "%s"\n#define EINK_COMMIT "%s"\n#define EINK_BUILD_EPOCH %s\n' '$(VERSION)' '$(COMMIT)' '$(BUILD_EPOCH)' > $@.tmp
	@cmp -s $@.tmp $@ || mv $@.tmp $@
	@rm -f $@.tmp

eink-dashboard: $(APP_OBJS) $(LVGL_OBJS)
	$(CC) $^ $(LDFLAGS) $(LDLIBS) -o $@
eink-connectd: $(CONNECT_OBJS)
	$(CC) $^ $(filter-out -static,$(LDFLAGS)) $(LDLIBS) -ldl -o $@

$(BUILD_DIR)/app/%.o: %.c $(BUILD_DIR)/generated/version.h
	@mkdir -p $(@D)
	$(CC) $(CPPFLAGS) $(CFLAGS) -include $(BUILD_DIR)/generated/version.h -c $< -o $@
$(BUILD_DIR)/connect/%.o: %.c $(BUILD_DIR)/generated/version.h
	@mkdir -p $(@D)
	$(CC) $(CPPFLAGS) $(if $(BT_INCLUDE_DIR),-I$(BT_INCLUDE_DIR)) $(CFLAGS) -include $(BUILD_DIR)/generated/version.h -c $< -o $@
$(BUILD_DIR)/lvgl/%.o: $(LVGL_DIR)/%.c
	@mkdir -p $(@D)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/tests/protocol: tests/protocol_test.c src/connect_proto.h
	@mkdir -p $(@D)
	$(HOSTCC) -O2 -Wall -Wextra -Isrc $< -o $@
$(BUILD_DIR)/tests/%: tests/%_test.c src/%.c $(wildcard src/*.h)
	@mkdir -p $(@D)
	$(HOSTCC) -O2 -Wall -Wextra -Isrc $< src/$*.c -o $@
test: $(TEST_BINS)
	@set -e; for t in $(TEST_BINS); do "$$t"; done
	python3 -m unittest discover -s tests -p 'test_*.py'

install: all
	install -d $(DESTDIR)/usr/bin $(DESTDIR)/etc/init.d $(DESTDIR)/etc/eink-os $(DESTDIR)/usr/share/eink-os/books $(DESTDIR)/usr/share/eink-os/licenses
	install -m755 eink-dashboard eink-connectd $(DESTDIR)/usr/bin/
	install -m755 packaging/openwrt/eink-dashboard.init $(DESTDIR)/etc/init.d/eink-dashboard
	install -m755 packaging/openwrt/eink-connectd.init $(DESTDIR)/etc/init.d/eink-connectd
	install -m644 packaging/openwrt/eink-dashboard.conf $(DESTDIR)/etc/
	install -m644 LICENSE THIRD_PARTY_NOTICES VERSION $(DESTDIR)/usr/share/eink-os/
	printf '%s\n' '$(COMMIT)' > $(DESTDIR)/usr/share/eink-os/SOURCE_COMMIT
	install -m644 LICENSES/* $(DESTDIR)/usr/share/eink-os/licenses/
	install -m644 assets/books/* $(DESTDIR)/usr/share/eink-os/books/

clean:
	rm -rf $(BUILD_DIR) eink-dashboard eink-connectd

-include $(APP_OBJS:.o=.d) $(CONNECT_OBJS:.o=.d) $(LVGL_OBJS:.o=.d)

# Separate host objects keep screenshot capture independent of ARM build artifacts.
PREVIEW_SRCS := tools/ui_capture.c src/ui.c src/lunar.c src/settings.c src/font_cjk_16.c
PREVIEW_OBJS := $(patsubst %.c,$(BUILD_DIR)/app/%.o,$(PREVIEW_SRCS))
-include $(PREVIEW_OBJS:.o=.d)
.PHONY: screenshots ui-capture
ui-capture: $(BUILD_DIR)/ui-capture
$(BUILD_DIR)/ui-capture: $(PREVIEW_OBJS) $(LVGL_OBJS)
	$(CC) $^ $(LDFLAGS) $(LDLIBS) -o $@
screenshots:
	$(MAKE) BUILD_DIR=build/preview CC="$(HOSTCC)" SYSROOT= CFLAGS="-O2" LDFLAGS= ui-capture
	mkdir -p build/preview/frames
	build/preview/ui-capture build/preview/frames
	python3 scripts/screenshots.py
