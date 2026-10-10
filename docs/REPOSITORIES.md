# 仓库与代码边界

| 位置 | 负责内容 |
| --- | --- |
| [dshanpi/EinkOS](https://github.com/dshanpi/EinkOS) | 桌面、应用、连接服务、用户态适配、测试、使用文档、开发技能、截图及发布工具 |
| [DongshanPI/100ASK_T113-PRO_TinaSDK5](https://github.com/DongshanPI/100ASK_T113-PRO_TinaSDK5/tree/einkos-240x360) | 内核驱动、设备树、Bootloader、板级配置、硬件测试工具、OpenWrt 集成及系统镜像构建 |
| [EinkOS Releases](https://github.com/dshanpi/EinkOS/releases) | 应用版的源码与升级包；系统版的配套 `.img.gz`；各自的清单、校验和、构建/验收记录及说明 |
| [dshanpi/lynx-releases](https://github.com/dshanpi/lynx-releases) | 用户统一获取 LYNX 安装及烧录工具的入口 |

## 应用与板级交界

应用只在 EinkOS 维护；硬件仓库保留原历史，但不维护第二份应用副本。
EinkOS 的 `platforms/tina/` 是调用现有 Linux/厂商接口的用户态代码，不包含
内核驱动、GPIO 设备树或波形实现。必要 UAPI 声明可按明确上游提交和许可证引用。

EinkOS 维护应用自带的 procd 服务、默认配置、字体及示例书籍。
硬件仓库维护 OpenWrt 包配方、板级依赖选择和镜像布局；其中 `epd-test` 仍为硬件诊断工具。
配方以完整应用提交和下载 SHA-256 锁定版本，不从浮动 main 构建发布固件。

## 独立应用发布

底层接口不变时，EinkOS 只在应用仓库开发、构建、验证和发布升级包，不要求硬件仓库跟随提交，
也不重建 SDK/镜像。应用清单声明系统契约、架构/依赖与升级路径，执行
[应用更新门禁](../standards/linux-board-release/v1.1.0/SPEC.md)。系统镜像仍保留其出厂应用记录，
设备当前应用版本另行维护。只有改变底层或制作新系统镜像时才走下面的跨仓库流程。

## 系统镜像变更如何跨仓库

1. 在 EinkOS 修改应用、测试、文档和对应截图，提交并通过 CI。
2. 需要发新固件时，在硬件仓库更新应用版本、固定提交、归档哈希和源码时间。
3. 使用配套 SDK 重新构建系统、打包、验收，再将镜像与对应应用源码放进 EinkOS Release。
4. 安装说明统一链接 LYNX；不把 EinkOS 固件混入 LYNX 工具发布仓库。

README、截图、技能等文档更新可以晚于既有固件提交；不能把旧固件的 build-info
改写为新的文档 HEAD。每个 Release 必须指向其实际构建的应用提交。
应用源码包不能代替完整系统对应源码；完整 SDK 基线与本地补丁也需要可追溯。

## 问题归属

界面/阅读/配网逻辑问题在 EinkOS 报告；设备不探测、引脚/BUSY/启动/分区问题在
硬件仓库报告；LYNX 安装与烧录工具问题在 LYNX 项目报告。跨界问题相互链接，
保留板型、应用提交、硬件提交和镜像 SHA-256，不复制维护相同代码。

具体 Release 对应的应用标签、硬件分支/标签、SDK 组件和镜像哈希见 [版本关联](VERSIONS.md)。

后续 Linux 板卡统一采用 [DSP-LINUX-001](../standards/linux-board-release/README.md)，
按新板接入表建立板卡配置与适配工具；现有 T113 版本保持原始身份与验证记录。
