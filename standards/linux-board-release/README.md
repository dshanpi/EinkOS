# Linux 开发板开源与发布规范

这是 dshanpi 项目的内部工程规范，供后续 Linux 开发板复用，不是外部标准组织认证。
当前规范版本为 **DSP-LINUX-001 / 1.1.0**。

[1.1.0 双发布线门禁](v1.1.0/SPEC.md) 是当前入口：application 发布升级包，system 发布镜像。
纯应用发布不要求新硬件提交或新镜像；应用自动更新必须满足兼容、可信校验、事务恢复、回退和数据保护门禁。

新版模板：[系统契约](v1.1.0/templates/system-contract.json)、
[应用发布清单](v1.1.0/templates/application-release.json)、
[应用验收记录](v1.1.0/templates/application-validation.json)。
以下 1.0.0 材料保留用于系统镜像线；与新版不一致时，以 1.1.0 的分类及门禁为准。

- [规范正文](v1.0.0/SPEC.md)：仓库边界、版本关联、构建证据、发布资产和门禁。
- [新板接入与发布检查表](v1.0.0/ONBOARDING.md)：按顺序交付，明确负责人和证据。
- [字段约定与模板用法](v1.0.0/CONTRACT.md)：单板、多板的文件命名和关联规则。
- [板卡配置模板](v1.0.0/templates/board-profile.json)、[版本锁模板](v1.0.0/templates/release-lock.json)、
  [SDK 清单模板](v1.0.0/templates/sdk-manifest.json)、[构建记录模板](v1.0.0/templates/build-info.json)、
  [验收模板](v1.0.0/templates/validation.json)。
- [README 模板](v1.0.0/templates/README.md)、[Release 说明模板](v1.0.0/templates/RELEASE_NOTES.md)、
  [编码助手约束模板](v1.0.0/templates/AGENTS.md)。
- [T113 实例与现状](v1.0.0/examples/T113.md)。
- [可复用开发 Skill](../../skills/linux-board-release/SKILL.md)。

新项目复制整个 `standards/linux-board-release/` 和 `skills/linux-board-release/`，保留相对目录。
从模板创建实际板卡配置和发布记录，填写真实证据。模板中的占位值、null、not_run 都不是验收结果。
EinkOS 的 T113 工具位于 `scripts/`，不是本规范的通用多板实现；详情见规范中的迁移说明。

已引用的规范版本保持内容和语义稳定；后续修订放入新版本目录，发布锁明确记录采用的版本。
规范变更本身不改变旧镜像、标签或历史验证结果。
