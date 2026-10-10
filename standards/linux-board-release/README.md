# Linux 开发板开源与发布规范

这是 dshanpi 项目的内部工程规范，供后续 Linux 开发板复用，不是外部标准组织认证。
当前规范版本为 **DSP-LINUX-001 / 1.0.0**。

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
