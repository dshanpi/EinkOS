# EinkOS 文档站

网站框架、正文、截图和部署配置与应用放在同一个仓库中。阅读 [站点维护说明](SITE.md)，从 [文档首页](OVERVIEW.md)进入内容。

```bash
cd docs
npm ci
npm run dev
npm run build
```

需要 Node.js 22.12.0 或更高版本。正文编辑 `docs/*.md`，不要编辑自动生成的 `src/content/docs/`。原有 GitHub 文档链接和截图路径继续可用。
