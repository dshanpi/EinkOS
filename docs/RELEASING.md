# 发布流程

首次独立版本为 v0.1.0。旧 SDK 软件包的 2.0.0 是迁移前内部编号，
不表示本项目 v0.1.0 已完成硬件验收。后续版本按语义化版本递增。

1. 更新 VERSION 和发布说明，运行测试及交叉编译，提交应用代码。
2. 在硬件仓库固定应用提交和 GitHub 源码归档 SHA-256，重新构建并打包系统。
3. 使用该镜像进行 LYNX 烧录与实机验证；逐项记录 passed / not_run / failed。
4. 核对系统组件源码可获取性和厂商二进制分发信息，见 SOURCES.md。
5. 为实际镜像填写 validation.json，使用以下工具生成发布资产：

```sh
python3 scripts/release.py \
  --sdk /path/to/T113-tina5v1.2-sdk \
  --hardware /path/to/100ASK_T113-PRO_TinaSDK5 \
  --rootfs /path/to/staged/rootfs \
  --image /path/to/out/t113_linux_evb1_auto_nand_uart0.img \
  --compiler /path/to/arm-linux-gnueabi-gcc \
  --validation /path/to/validation.json
```

验证记录格式：

```json
{
  "image_sha256": "实际未压缩镜像的 SHA-256",
  "checks": {
    "cold_boot": "not_run",
    "keys": "not_run",
    "display_refresh": "not_run",
    "reader_resume": "not_run",
    "wifi_success_and_recovery": "not_run",
    "time_restore_and_sync": "not_run",
    "bluetooth_or_unavailable": "not_run",
    "lynx_flash": "not_run"
  },
  "notes": "验证环境和观察结果"
}
```

工具检查安装的应用版本及提交与源码一致，镜像晚于应用安装，验证报告对应
镜像 SHA-256；生成不带原文件名和时间戳的 gzip、完整应用源码包、构建信息、
验证记录及 SHA256SUMS。该检查不能替代镜像内容检查或实机验证。
SDK 本地修改必须通过硬件覆盖层或发布补丁保留，不得仅靠提交号声称可复现。

已登录 GitHub CLI 后运行 `scripts/publish-release.sh dist` 创建 Draft Release。
草稿使用 prerelease 标志，避免漏验证时误发布为稳定版。发布前检查所有资产及
对应源码链接；实机未验证只能公开为预发布，源码或再分发条件不齐备则保持草稿。
已完成全部验收后才移除 prerelease 标志。不要覆盖已公开版本的资产；修订需新版本。

CI 在普通 GitHub runner 运行逻辑测试、Linux 应用构建和独立源码包构建。
完整 SDK 构建在维护者已有 SDK 环境执行；不在公共 PR 工作流中运行板级烧录。

## 发布门禁：草稿、预发布、正式版

| 门禁 | Draft 草稿 | 公开 Pre-release | 正式 Stable |
| --- | --- | --- | --- |
| 完整源码包、`.img.gz`、SHA256SUMS、build-info、validation | 必须完整 | 必须完整 | 必须完整 |
| 压缩包/解压镜像哈希、源码包版本与提交相符 | 必须通过 | 必须通过 | 必须通过 |
| 应用与硬件提交、明确板型、逐项验证状态 | 必须记录 | 必须记录 | 必须记录 |
| 逻辑测试、工具测试、独立源码构建、ARM、系统构建/打包、根文件系统版本核对 | 记录实际结果 | 全部通过 | 全部通过 |
| 完整系统对应源码可获取、厂商组件分发说明 | 可以待补齐 | 必须完成并记录证据 | 必须完成并记录证据 |
| 冷启动、按键、全/局刷、阅读恢复、配网成功/恢复、时间、蓝牙降级、LYNX 烧录 | 可记录 not_run/failed | 可有 not_run，不能有 failed | 全部 passed |
| 对外可见性 | 仅有权限的维护者 | 公众可下载，明确未验证项 | 公众可下载 |

应用仓库中有源码，不代表整套系统对应源码已经齐备；预发布也不能省略来源说明。
截图只能证明特定数据下的 UI 渲染结果，不能把 `lynx_flash` 或 `display_refresh` 写成 passed。
本仓库普通 CI 不控制真实硬件，也不提供自动化虚假的实机通过结果。

```sh
# 可离线运行，失败会给出具体缺项
python3 scripts/check_release.py dist --channel draft
python3 scripts/check_release.py dist --channel prerelease
python3 scripts/check_release.py dist --channel stable

# 上传资产为草稿；读取 build-info 的版本/提交，允许文档 HEAD 更晚
scripts/publish-release.sh dist

# 获得发布任务授权且材料齐备后，检查远端实际附件并公开
scripts/promote-release.sh v0.1.0 prerelease
# 实机全部通过后才能提升为 stable
scripts/promote-release.sh v0.1.0 stable
```

`promote-release.sh` 下载当前 Release 附件到临时目录再验门禁，避免只检查本地
副本却发布了远端不同文件。失败立即停止，不调用公开发布 API。
现有公开资产不应覆盖；修订应用/固件应发布新版本。网络写入返回不明确错误时，
先查询 Release 与已上传附件，再决定是否补传，不能直接重复创建或覆盖。

源码/厂商说明审核由维护者依据实际资料完成，工具只验证记录与本次镜像绑定，
不会替代资料核对或自动宣称许可合规。在 `validation.json` 中记录：

```json
{
  "distribution_review": {
    "status": "passed",
    "reviewer": "实际审核者",
    "image_sha256": "本次未压缩镜像的 SHA-256",
    "source_url": "https://可公开获取完整对应源码的位置",
    "vendor_notices_url": "https://实际厂商组件来源和分发说明"
  }
}
```

以上是字段格式，不是本版本已经通过的审核证据。缺少对应资料时保持 pending 或不填，
门禁将阻止公开。更新验证记录后重新生成其 SHA256SUMS；不要修改镜像/应用提交来规避检查。

## 当前 v0.1.0 记录

现有镜像对应应用提交 `087cbaf80cebcbc5d101d37ab3520b3c6fe461c5`、硬件提交
`d24ebd7af24d4b07b0912b19f06a6dad22123eb5`。已完成主机测试、交叉编译、SDK 构建、
打包及镜像内容核对；实机项目尚未执行，完整系统对应源码/厂商资料审核尚待补齐。
因此满足草稿资产门禁，不满足公开预发布或正式版门禁。最新文档与截图不改写这些历史构建信息。
