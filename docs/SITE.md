# 维护文档站

文档站使用 Astro 7.3.4 和 Starlight 0.42.3，参考 [YuzukiNeko docs](https://github.com/YuzukiHD/YuzukiNeko/tree/a6cc7ea3fc8426d08e7e53684e5c9cb27abbedb2/docs)的同仓库集成方式。本站保留 EinkOS 的原始 Markdown 和截图路径，构建时生成网站页面。

## 理解目录职责

| 路径 | 维护内容 | 是否提交 Git |
| --- | --- | --- |
| `docs/*.md` | 权威文档正文，GitHub 与站点共用 | 是 |
| `docs/screenshots/` | 已有截图及来源清单 | 是 |
| `docs/routes.mjs` | 页面来源、网址、分组和显示名称 | 是 |
| `docs/astro.config.mjs` | 站点地址、Starlight、样式和插件 | 是 |
| `docs/package.json`、`package-lock.json` | 固定依赖与构建命令 | 是 |
| `docs/scripts/` | 同步源文件、检查链接和构建结果 | 是 |
| `docs/src/content/docs/` | 自动生成的 Starlight 页面 | 否 |
| `docs/public/screenshots/`、`public/vendor/` | 构建时复制的图片和浏览器依赖 | 否 |
| `docs/dist/` | 静态站点产物 | 否 |
| `.github/workflows/docs.yml` | CI 构建和 Pages 部署 | 是 |

YuzukiNeko 使用英文根目录和中文目录；EinkOS 当前资料以中文为主，因此本站使用简体中文作为根语言，暂不展示没有完整译文的语言入口。

## 安装并预览

在开发电脑安装 Node.js 22.12.0 或更高版本，CI 使用 Node.js 24。进入 EinkOS 仓库的 `docs` 目录：

```bash
npm ci
npm run dev
```

打开终端显示的本地地址，默认页面路径为 `/EinkOS/`。开发模式会跟踪已登记的 Markdown 文件；新增页面或修改路由配置后重启开发服务器。

## 修改或增加页面

修改 `docs/*.md` 中的正文。每篇文件以一个一级标题开头，构建时会将标题转换为 Starlight 前置信息，编辑链接仍指向原文件。

增加页面时，在 `routes.mjs` 登记 source、slug、group 和 title。slug 使用小写英文与连字符，保持已有网址稳定。

正文链接使用相对 Markdown 路径，例如 `[安装](INSTALL.md)`。构建插件会把站内文档转换为带 `/EinkOS/` 前缀的网址，将源码引用转换为 GitHub 链接。

图片继续使用 `screenshots/01-home.png` 这类相对路径，不改写现有截图或来源清单。

## 绘制架构图

在 Markdown 中使用 Mermaid 代码块。浏览器脚本从本站静态资源加载 Mermaid；不依赖第三方 CDN。图表失败时保留源文本供排查。

终端录像支持 asciinema。元素使用 `asciinema-cast not-content` 类，`data-src` 属性填写以 `public/casts/` 开头的实际录像路径；对应文件放在 `docs/public/casts/`。构建时该路径转换为站点内的静态资源地址。添加后必须通过静态资源检查，不能把不存在的示例文件写成可播放录像。

## 执行检查

在仓库根目录执行文档来源和链接检查：

```bash
python3 scripts/check_docs.py
```

在 `docs` 目录执行：

```bash
npm run build
```

构建依次同步正文、运行链接转换测试、生成站点、检查页面路径/锚点/静态资源。检查通过后可运行 `npm run preview` 查看构建产物。

文档工具发生变化时，按仓库要求另在 Linux 环境运行 `make test`。产品 UI 未修改时无需用新图片替换现有截图；后续修改产品 UI 则仍需重新生成并验证截图。

## 发布到 GitHub Pages

1. 合并已验证的文档变更。
2. 在仓库 Settings → Pages 将 Source 设置为 GitHub Actions。
3. 在 Actions 中手动运行 “EinkOS documentation”，勾选 deploy。
4. 检查构建和部署任务均成功，再打开任务返回的地址。
5. 需要 main 分支后续自动部署时，设置仓库 Actions 变量 `DOCS_PAGES_ENABLED=true`。

预配置地址为 `https://dshanpi.github.io/EinkOS/`。配置文件中的地址不代表站点已发布；以部署任务返回结果为准。

## 核对写作与事实

客户操作文档采用 `write-professional-guides` 风格：说明适用对象与执行位置，按准备、操作、检查和必要异常处理展开，提供可观察的成功判据。

系统版本、路径、协议和烧录动作以实际源码和对应板卡资料为准。GitHub 发布状态、主机测试和实机验收分别记录；不能因更新文档而改写旧镜像来源。

参考仓库使用 CC0；Astro、Starlight、Mermaid、asciinema 等依赖遵循各自许可证。EinkOS 应用与现有第三方许可保持原规定。
