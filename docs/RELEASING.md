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
