// Canonical Markdown remains at docs/*.md; generated pages are ignored by Git.
export const site = 'https://dshanpi.github.io';
export const base = '/EinkOS';
export const repository = 'https://github.com/dshanpi/EinkOS';
export const routes = [
  {
    "source": "docs/OVERVIEW.md",
    "slug": "index",
    "group": "开始使用",
    "title": "认识 EinkOS"
  },
  {
    "source": "docs/FEATURES.md",
    "slug": "features",
    "group": "开始使用",
    "title": "核对系统特性"
  },
  {
    "source": "docs/HARDWARE.md",
    "slug": "hardware",
    "group": "开始使用",
    "title": "确认硬件与系统"
  },
  {
    "source": "docs/SYSTEMS.md",
    "slug": "systems",
    "group": "开始使用",
    "title": "在不同系统安装与使用"
  },
  {
    "source": "docs/INSTALL.md",
    "slug": "install",
    "group": "开始使用",
    "title": "烧录配套系统"
  },
  {
    "source": "docs/QUICKSTART.md",
    "slug": "quickstart",
    "group": "开始使用",
    "title": "完成首次启动"
  },
  {
    "source": "docs/USER_GUIDE.md",
    "slug": "user-guide",
    "group": "使用桌面",
    "title": "操作桌面与应用"
  },
  {
    "source": "docs/CONFIGURATION.md",
    "slug": "configuration",
    "group": "使用桌面",
    "title": "调整配置与备份数据"
  },
  {
    "source": "docs/TROUBLESHOOTING.md",
    "slug": "troubleshooting",
    "group": "使用桌面",
    "title": "定位常见问题"
  },
  {
    "source": "docs/GALLERY.md",
    "slug": "gallery",
    "group": "使用桌面",
    "title": "查看界面截图"
  },
  {
    "source": "docs/ARCHITECTURE.md",
    "slug": "architecture",
    "group": "开发与架构",
    "title": "理解系统架构"
  },
  {
    "source": "docs/BOARD_PORTING.md",
    "slug": "board-porting",
    "group": "开发与架构",
    "title": "接入新板卡与屏幕"
  },
  {
    "source": "docs/BUILD.md",
    "slug": "build",
    "group": "开发与架构",
    "title": "编译应用与系统"
  },
  {
    "source": "docs/REPOSITORIES.md",
    "slug": "repositories",
    "group": "开发与架构",
    "title": "选择修改仓库"
  },
  {
    "source": "docs/VERSIONS.md",
    "slug": "versions",
    "group": "开发与架构",
    "title": "核对版本关联"
  },
  {
    "source": "docs/DEVELOPMENT.md",
    "slug": "development",
    "group": "开发与架构",
    "title": "遵循开发要求"
  },
  {
    "source": "docs/SCREENSHOTS.md",
    "slug": "screenshots",
    "group": "开发与架构",
    "title": "生成真实界面截图"
  },
  {
    "source": "docs/APPLICATION_OTA.md",
    "slug": "application-ota",
    "group": "发布与维护",
    "title": "接入应用发布与自动更新"
  },
  {
    "source": "docs/SYSTEM_OTA.md",
    "slug": "system-ota",
    "group": "发布与维护",
    "title": "区分应用与系统 OTA"
  },
  {
    "source": "docs/RELEASING.md",
    "slug": "releasing",
    "group": "发布与维护",
    "title": "验证发布资料"
  },
  {
    "source": "docs/RELEASE_NOTES.md",
    "slug": "release-notes",
    "group": "发布与维护",
    "title": "查看版本说明"
  },
  {
    "source": "docs/SOURCES.md",
    "slug": "sources",
    "group": "发布与维护",
    "title": "查阅源码与许可"
  },
  {
    "source": "docs/SITE.md",
    "slug": "site",
    "group": "发布与维护",
    "title": "维护文档站"
  }
];
export const sidebar = [...new Set(routes.map((page) => page.group))].map((label) => ({
  label,
  items: routes.filter((page) => page.group === label).map((page) => ({
    label: page.title, slug: page.slug,
  })),
}));
