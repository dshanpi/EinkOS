# UI 截图与复现

README 展示全部 11 个桌面路由及主要状态变体，共 26 张 240×360 黑白截图；
另有 3 张手机配网表单/成功/失败网页截图，共 29 张。

这些是**实际 UI 源码的主机渲染截图**：桌面调用生产 `src/ui.c`、固定 LVGL 8.3.1
和同一套字体，注册内存 framebuffer，并使用与显示适配一致的黑白阈值。
不是实机照片，不包含屏幕物理残影、刷新耗时或按键/网络验收结果。
时间、CPU/内存、书籍文字、SSID、蓝牙设备和密码都是固定演示数据。

## 桌面生成

```sh
make -j2 screenshots
python3 scripts/check_docs.py
```

只需要 Linux 主机 C 编译器、Make 和 Python 3，不需要 SDK、墨水屏、root 权限
或 SDL。工具使用 `build/preview/` 的独立主机对象，避免与 ARM 对象混用。
C 程序先输出完整 PGM 帧，Python 标准库将其编码成无损 PNG；不做布局重绘或美化。

`docs/screenshots/manifest.json` 记录渲染输入的 SHA-256 和每张图的哈希。
`check_docs.py` 确保所有 `desktop_screen` 路由都有捕获、PNG 都在 README 中引用，
并检查来源哈希和本地文档链接。新增页面或状态时同步扩充捕获场景和图库。

## 手机配网页生成

```sh
make screenshots
# 安装 Node/npm，并确保 Playwright CLI 可用及 Chrome/Chromium 已安装
scripts/capture-portal.sh
python3 scripts/check_docs.py
```

脚本从生产 `connectd.c` 提取 HTML 模板，填入虚构网络，启动仅绑定 127.0.0.1 的
静态服务器，并用 Playwright CLI 在 390×760 视口捕获。生成过程不执行真实配网，
也不启动连接服务。模板改变但提取逻辑失效时脚本会报错，而不是默默生成过期页面。

需要自定义 Chromium 路径时，用 `PW_CONFIG=/path/to/cli.config.json` 指定 Playwright
CLI 配置。中间截图和浏览器日志位于被 Git 忽略的 `output/playwright/`；正式图片
进入 `docs/screenshots/`，`phone-manifest.json` 记录来源和哈希。占用端口为 8769。

## 当前截图展示出的限制

长按键提示在 240 像素宽度下存在裁切，部分符号在当前字体子集中显示缺字框；
部分页面虽然能切换主页语言，内部提示仍为中文。这些保留为当前真实效果，
没有用替代图片掩盖。后续 UI 修复需重新生成截图，并进行对应实机回归。

一张状态截图不代表每个菜单项、月份、书籍、网络或蓝牙设备组合都已验收。
真实设备验证记录应另外写入与镜像 SHA-256 绑定的 `validation.json`。
