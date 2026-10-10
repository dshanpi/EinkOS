# 开发与技能要求

先阅读 [仓库边界](REPOSITORIES.md) 和 [框架实现](ARCHITECTURE.md)，再选择修改位置。
开发者及编码助手均遵循仓库根目录 [AGENTS.md](../AGENTS.md)。
可复用技能位于 [skills/einkos-development/SKILL.md](../skills/einkos-development/SKILL.md)，
包含应用修改、界面截图和发布工作流；它随仓库分发，不会自动安装或更改用户全局配置。

## 环境与基本能力

| 工作 | 要求 |
| --- | --- |
| 应用逻辑 | Linux C、GNU Make、LVGL 8、固定内存/缓冲区、文件与 UTF-8 处理 |
| 连接服务 | Unix socket、Tina Wi-Fi/蓝牙接口、HTTP 表单、进程及错误处理 |
| 板级适配 | 匹配工具链/sysroot、ioctl/evdev；涉及驱动或设备树时转到硬件仓库 |
| 文档截图 | `make screenshots`；手机网页另需 Node/npm、Playwright CLI 和 Chromium |
| 发布 | SDK 构建、LYNX 实机烧录、镜像/source SHA-256、GitHub CLI、发布门禁 |

## 开发闭环

- 保留程序名、配置路径、状态文件、socket 协议和 EPD ABI；需要改动时明确迁移。
- UI 为 240×360、1bpp。修改页面/字体/布局后重新生成截图，检查文字裁切、缺字和选中态。
- `make test` 验证逻辑及发布门禁；`make screenshots` 验证真实 UI 的无硬件渲染。
- 改网页模板后，执行 `scripts/capture-portal.sh`，更新浏览器截图及来源记录。
- `python3 scripts/check_docs.py` 检查本地链接、页面覆盖和图片来源哈希。
- 应用/后端修改需交叉编译；涉及实际显示、输入、配网、蓝牙或启动时需匹配固件的实机记录。
- 发布按 [发布指南](RELEASING.md) 操作。截图和主机测试不能替代 LYNX 烧录验收。

不在开发电脑上启动生产连接服务来截图：它会操作网络和时间。文档工具使用
内存显示与虚构数据，手机页面使用实际 HTML 模板的静态捕获。

## 提交与审查

描述问题、最终行为、测试与未验证项。界面变更附对应截图；硬件变更附关联仓库提交；
固件变更附精确板型和镜像哈希。不要提交个人 SSID/密码、蓝牙地址、令牌、状态文件，
或把 `.img.gz`、编译产物放进 Git 源码树。示例网络和密码仅为截图假数据。

自动化不得把 `not_run` 改成 `passed`，不得把草稿描述为公开下载，不得改写既有
发布文件冒充新构建。新版本应重新构建、生成校验并保留验证证据。

后续 Linux 板卡统一采用 [DSP-LINUX-001](../standards/linux-board-release/README.md)，
按新板接入表建立板卡配置与适配工具；现有 T113 版本保持原始身份与验证记录。
