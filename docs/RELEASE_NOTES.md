EinkOS v0.1.0 — 首个独立开源版本

- 独立的 GPL-3.0 应用仓库，包含固定 LVGL 源码和 Linux 构建入口。
- 保留日历/农历、TXT 阅读、手机配网、蓝牙管理和物理按键操作。
- 驱动与板级集成留在原硬件仓库，系统固定应用提交和下载校验和。
- 配套镜像：100ASK T113-PRO / 3.52 英寸 240×360 / evb1_auto_nand。
- 安装工具统一使用 https://github.com/dshanpi/lynx-releases 提供的 LYNX。

安装：校验 SHA256SUMS，解压 .img.gz，通过 LYNX 烧录 .img。
全量烧录清除原数据，请先备份。应用旧内部编号 2.0.0 已改为独立项目 0.1.0。

验证状态：查看 validation.json。当前没有连接目标板，尚未完成该镜像的 LYNX
实机烧录、屏幕、按键和网络回归；此版本不能标为稳定版。
完整系统对应源码和厂商组件再分发说明需齐备后才公开镜像资产。

源码与硬件：https://github.com/dshanpi/EinkOS/blob/main/docs/SOURCES.md
