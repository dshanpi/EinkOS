# 模板字段与多板交付约定

本目录模板是 **DSP-LINUX-001 / 1.0.0** 的通用记录格式 `dsp-linux-release-v1`，
需由各项目的适配工具实现校验。它不是 EinkOS T113 旧 `schema_version: 1` 的直接替换。
JSON 模板可解析不代表数据完整或门禁通过；`REPLACE_*`、null、空列表必须按实际输入补齐。

## 复制到哪里

| 模板 | 项目工作文件 | Release 附件名 |
| --- | --- | --- |
| [board-profile.json](templates/board-profile.json) | `boards/<board-id>/board-profile.json` | `board-profile-<board-id>.json` |
| [release-lock.json](templates/release-lock.json) | `releases/<version>/release-lock.json` | `release-lock.json` |
| [sdk-manifest.json](templates/sdk-manifest.json) | 构建输入归档目录 | `sdk-manifest-<board-id>.json` |
| [build-info.json](templates/build-info.json) | 构建输出目录 | `build-info-<board-id>.json` |
| [validation.json](templates/validation.json) | 实机/构建验证记录目录 | `validation-<board-id>.json` |

应用版本字段与源码包中的 VERSION 一致，发布锁必须单独记录实际应用版本。
Release 产品版本和应用版本通常一致；系统独立修订时可以使用新的产品发布版本并复用
应用提交，但必须保留实际应用版本，不能把旧源码 VERSION 改写成新值。应用发布标签
`v<release-version>` 指向这个实际应用提交，锁内同时记录发布版本和应用版本的差异。
使用这种版本方式前必须扩展现有 T113 工具；旧工具要求二者一致，不能直接套用。

## 锁与哈希的方向

`release-lock` 包含共享应用信息和 `boards[]`。每板项记录 board_id、硬件仓库/分支/标签/提交、
实际集成配方及其来源/哈希、profile 和 SDK/build-info 的文件名及 SHA-256、镜像两种哈希。
源码包作为顶层共享附件。validation 单独绑定镜像哈希；它和 lock 一起由 SHA256SUMS 覆盖，
避免验收证据引用锁时出现互相哈希的循环。

顶层 `artifacts[]` 列出源码包及每板所有附件的文件名、角色、board_id 和哈希；
不包含锁自身及 SHA256SUMS。不能出现重复文件名、缺少必需角色、未知 board_id 或目录穿越。
各处同一文件/提交出现多次时必须逐项相等；不能只验证文件存在或哈希字符串长度。
Git 对象 ID 使用完整值；当前 Git SHA-1 是 40 位，使用其他对象格式时同时标明算法。
资产校验统一 SHA-256（64 位十六进制）。时间用包含时区的 ISO 8601 格式。

发布阶段以 GitHub Release 状态和已记录门禁结果为准，锁文件不固定草稿/预发布/正式状态，
避免仅提升阶段就需要修改不可变的输入身份。

## SDK 输入不能只记版本名

`sdk-manifest.projects[]` 每个条目包含组件路径、源码获取位置、完整提交或源码包哈希。
`overlays[]` 固定硬件覆盖层提交；`patches[]` 列出实际补丁附件/地址、SHA-256、目标组件及应用顺序；
`extra_inputs[]` 列出未跟踪源码、额外配置、厂商二进制等输入的获取位置及 SHA-256。
`excluded_paths[]` 只用于已审查的缓存/构建输出，不用于隐藏来源不明的输入。
`input_capture_complete` 仅在输入全部归档并核对后设为 true。
私有 Git 地址不满足公众获取对应源码的要求，需提供匹配的公开来源或归档。

## 验证记录与适配器

每项 `checks` 包含状态、测试者、时间、证据和可选不适用理由。构建与硬件检查分开，
都绑定同一个解压镜像哈希。来源审核记录实际审核者、时间、对应源码及厂商说明的固定位置。
扩展检查项必须有执行方法；只要属于板卡声明能力，就不能从发布门禁中删除以绕过失败。

各板适配器负责：读取 profile；提取该 SDK 的真实组件/补丁/配置；读取实际包配方的应用固定值；
执行目标构建；识别镜像内标识；生成记录和资产；验证本地关系与远端标签/附件。
Buildroot、Yocto、OpenWrt 或其他系统可以采用不同命令，但必须交付相同的关联证据。
JSON 字段校验不替代上述操作。新增适配器需有错配拒绝测试，详见 [接入流程](ONBOARDING.md)。

## 多板与兼容

GitHub Release 附件处于同一命名空间，因此每板的镜像、profile、SDK、build-info 和 validation
均使用 board_id 后缀；不能给每板都上传同名 `build-info.json`。一个公共 lock 与 SHA256SUMS
覆盖全部支持板。新增板或更换镜像进入下一次产品发布，不能静默给已冻结的正式版替换资产。

历史 T113 v0.1.0 保留单板命名与原始 schema，版本对应关系见 [实例](examples/T113.md)。
其应用、镜像和标签不因规范发布改变；不把尚缺证据的旧草稿标为符合本规范的正式版。
