# REPLACE_PRODUCT

> 模板：替换占位内容，保留实际实现范围；未实现能力不要写成已支持。

项目定位：REPLACE_PURPOSE。
遵循 DSP-LINUX-001 1.0.0，规范放在 `standards/linux-board-release/`。

## 支持板卡与当前阶段

| board_id / 硬件修订 | CPU/架构 | 存储/显示 | SDK | 当前阶段 | 已验证能力及限制 |
| --- | --- | --- | --- | --- | --- |
| REPLACE_BOARD | REPLACE_SOC | REPLACE_VARIANT | REPLACE_BASELINE | 适配中 | REPLACE_FACTS |

## UI 截图与功能

按页面列出实际截图及主要成功/失败状态，说明来源是主机渲染还是实机拍摄、对应源码与生成命令。
无 UI 时明确注明，并提供适用的命令行使用示例。不要将规划图或渲染截图当作实机验收。
逐项列出功能、实际实现入口、支持范围与已知限制。

## 架构与接口

描述进程、框架、应用状态、连接服务、用户态/内核边界及数据流。
说明阻塞/异步行为、配置/状态路径、ABI 和升级兼容方式；不能照抄其他板未实现的架构。

## 当前 Release 对应版本

| 发布版本 | 应用标签/完整提交 | board_id | 硬件标签/完整提交 | SDK 清单 | 镜像/验收记录 |
| --- | --- | --- | --- | --- | --- |
| REPLACE_VERSION | REPLACE_APP | REPLACE_BOARD | REPLACE_HARDWARE | REPLACE_SDK | REPLACE_ASSETS |

链接实际 Release、版本锁与源码位置。说明开发分支可以前进，复现镜像使用固定提交。

## 安装与恢复

应用 Releases：REPLACE_RELEASE_URL。
烧录工具统一获取入口：[LYNX](https://github.com/dshanpi/lynx-releases)。
列出实测工具版本/主机系统、板卡模式、SHA256SUMS 校验、`.img.gz` 解压、目标存储确认、
备份要求、烧录步骤、首次启动和故障恢复；填入真实操作文档，不提供未经验证的命令。

## 构建与开发

给出依赖、工具链及 SDK 获取方式、固定输入的 checkout/应用补丁顺序、主机测试、目标构建、
系统打包、UI 截图与门禁命令。注明哪些命令操作真实设备或网络。
链接本项目 AGENTS、Skill、架构、版本关联、支持矩阵和发布规范。

## 仓库边界与许可证

列出应用仓库、硬件/SDK 仓库、应用 Releases、LYNX 各自职责。
给出应用许可证、第三方声明、完整系统对应源码和厂商组件说明的实际位置。
