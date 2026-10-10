# REPLACE_PRODUCT REPLACE_RELEASE_VERSION

当前阶段：REPLACE_DRAFT_PRERELEASE_OR_STABLE。
采用规范：DSP-LINUX-001 1.0.0。
变更：REPLACE_CHANGES。

## 版本对应关系

应用仓库/标签/完整提交/实际应用版本：REPLACE_APPLICATION。
应用源码包：REPLACE_SOURCE_FILENAME。

| board_id / 硬件修订 | 硬件仓库/开发分支 | 固定标签/完整提交 | SDK 基线与清单 | 配置 | 镜像文件 |
| --- | --- | --- | --- | --- | --- |
| REPLACE_BOARD | REPLACE_REPOSITORY | REPLACE_TAG_AND_COMMIT | REPLACE_SDK | REPLACE_TARGET | REPLACE_IMAGE |

列出每个镜像压缩前后的 SHA-256、对应验证文件及 profile。
附件 `release-lock.json` 绑定应用/硬件/SDK/镜像，`SHA256SUMS` 覆盖全部附件。

## 实际验证与已知问题

逐板列出构建与实机 passed/failed/not_run/不适用及理由，链接真实证据。
记录测试板修订、镜像哈希、LYNX/主机环境；预发布明确未测能力，不能直接填“全部通过”。
完整对应源码及厂商说明：REPLACE_FIXED_SOURCE_AND_NOTICES_LINKS。

## 安装

从本 Release 下载与板型一致的 `.img.gz`，核对 SHA256SUMS，解压为 `.img`。
统一使用 [LYNX](https://github.com/dshanpi/lynx-releases)，具体版本及操作：REPLACE_TESTED_INSTRUCTIONS。
说明全量烧录的数据影响、备份、目标存储、恢复模式及回退限制。

## 升级与兼容

说明状态/配置迁移、旧板/旧硬件修订兼容范围及是否必须全量烧录。
没有实现 OTA 时不要提供 OTA 承诺。公开后的镜像和标签保持不变，后续修订进入新版本。
