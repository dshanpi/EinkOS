# EinkOS

面向墨水屏设备的开源 Linux 桌面与应用系统。

EinkOS 提供黑白电子手帐桌面、日历/农历、TXT 阅读器、手机 Wi-Fi 配网和蓝牙管理，
并为已支持的开发板发布配套 Linux 系统镜像。首版基于 TinaSDK / OpenWrt，
支持 **100ASK T113-PRO + 3.52 英寸 240×360 单色墨水屏**。

**项目状态：首个独立版本 v0.1.0，待完成发布镜像的实机验收。**
当前支持范围不包含其他板型、其他屏幕分辨率、OTA 或通用 PC 桌面。

## 下载与安装

1. 在 [EinkOS Releases](https://github.com/dshanpi/EinkOS/releases) 下载适合板型的 `.img.gz` 和 `SHA256SUMS`。
2. 校验并解压得到 `.img`。
3. 从 [DshanPI LYNX｜芯桥](https://github.com/dshanpi/lynx-releases) 获取对应电脑平台的烧录工具。
4. 按 [安装指南](docs/INSTALL.md) 绑定开发板、进入烧录模式、完成烧录。

每个软件正式版本均附带配套系统镜像。预发布版本会明确列出尚未验证的项目。

## 功能

- LVGL 8 黑白桌面；日期、星期、农历、节日和连接状态。
- 月历浏览、今日定位，1900–2100 年农历转换。
- UTF-8 / GB18030 TXT 阅读，两层目录、断点续读、书签。
- 手机热点配网、Wi-Fi 扫描、浏览器校时及失败恢复。
- 蓝牙扫描和配对；硬件不可用时显示“不可用”。
- 物理按键操作、局刷/全刷切换、断电时间记录和 NTP 校时。

操作方式、存储位置和限制见 [用户指南](docs/USER_GUIDE.md)。

## 构建与参与

```sh
git clone https://github.com/dshanpi/EinkOS.git
cd EinkOS
make test
make -j2 eink-dashboard
./eink-dashboard --version
```

以上是在 Linux 主机上构建应用并运行逻辑测试；实际显示需要目标墨水屏驱动。
完整的连接服务需要 Tina 的 `bt_manager.h`。交叉编译和配套系统构建见
[构建指南](docs/BUILD.md)，版本发布见 [发布指南](docs/RELEASING.md)。

目录：`src/` 为桌面与通用逻辑，`platforms/tina/` 为现有显示和连接适配，
`third_party/` 为固定 LVGL 源码，`packaging/` 为运行时安装文件，`tests/` 为测试。

## 软件与硬件仓库

应用代码只在本仓库维护。内核驱动、设备树、Bootloader 和系统集成继续放在
[原硬件仓库的 einkos-240x360 分支](https://github.com/DongshanPI/100ASK_T113-PRO_TinaSDK5/tree/einkos-240x360)。
硬件仓库获取固定 EinkOS 提交并校验源码包；不跟随浮动的 main。

应用使用 GPL-3.0-only；LVGL、字体和驱动接口保留各自许可证。
见 [LICENSE](LICENSE)、[第三方声明](THIRD_PARTY_NOTICES) 和 [系统源码说明](docs/SOURCES.md)。

## English

EinkOS is an open-source Linux desktop and application suite for e-paper devices.
The first target is the 100ASK T113-PRO with a 240×360 monochrome panel, using
TinaSDK/OpenWrt. Releases pair application source with board-specific `.img.gz`
firmware. Install firmware using [LYNX](https://github.com/dshanpi/lynx-releases).
Kernel drivers and board support remain in the separate hardware repository.
See [BUILD](docs/BUILD.md), [INSTALL](docs/INSTALL.md), and [CONTRIBUTING](CONTRIBUTING.md).
