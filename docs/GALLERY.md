# 查看界面截图

以下 **29 张截图**覆盖全部 11 个桌面路由、阅读/连接/异常等主要状态，以及手机配网网页。
桌面直接运行生产 `ui.c`、LVGL 和同一套字体，输出 240×360 黑白帧；手机页面由浏览器
捕获生产 HTML 模板。时间、网络、设备和资源数据均为虚构演示数据。
**这些是源码渲染截图，不是实机照片或硬件验收证明。** 当前长提示裁切与部分符号缺字也如实保留。

| 主页 | 英文主页 | 时间恢复待校准 |
| --- | --- | --- |
| <img src="screenshots/01-home.png" width="240" alt="主页"> | <img src="screenshots/02-home-en.png" width="240" alt="英文主页"> | <img src="screenshots/03-time-restored.png" width="240" alt="时间恢复待校准"> |

| 时间未设置 | 本月日历 | 月份浏览 |
| --- | --- | --- |
| <img src="screenshots/04-time-unset.png" width="240" alt="时间未设置"> | <img src="screenshots/05-calendar.png" width="240" alt="本月日历"> | <img src="screenshots/06-calendar-next.png" width="240" alt="月份浏览"> |

| 空书库 | 书库 | 阅读正文 |
| --- | --- | --- |
| <img src="screenshots/07-reader-empty.png" width="240" alt="空书库"> | <img src="screenshots/08-library.png" width="240" alt="书库"> | <img src="screenshots/09-reader.png" width="240" alt="阅读正文"> |

| 书签状态 | 阅读操作菜单 | 连接入口 |
| --- | --- | --- |
| <img src="screenshots/10-reader-bookmark.png" width="240" alt="书签状态"> | <img src="screenshots/11-reader-menu.png" width="240" alt="阅读操作菜单"> | <img src="screenshots/12-connect.png" width="240" alt="连接入口"> |

| Wi-Fi 扫描结果 | 手机配网热点 | Wi-Fi 失败状态 |
| --- | --- | --- |
| <img src="screenshots/13-wifi.png" width="240" alt="Wi-Fi 扫描结果"> | <img src="screenshots/14-wifi-portal.png" width="240" alt="手机配网热点"> | <img src="screenshots/15-wifi-failure.png" width="240" alt="Wi-Fi 失败状态"> |

| 蓝牙设备列表 | 蓝牙扫描 | 蓝牙配对确认 |
| --- | --- | --- |
| <img src="screenshots/16-bluetooth.png" width="240" alt="蓝牙设备列表"> | <img src="screenshots/17-bluetooth-scan.png" width="240" alt="蓝牙扫描"> | <img src="screenshots/18-bluetooth-confirm.png" width="240" alt="蓝牙配对确认"> |

| PIN / Passkey 输入 | 蓝牙不可用 | 更多应用 |
| --- | --- | --- |
| <img src="screenshots/19-bluetooth-pin.png" width="240" alt="PIN / Passkey 输入"> | <img src="screenshots/20-bluetooth-unavailable.png" width="240" alt="蓝牙不可用"> | <img src="screenshots/21-more.png" width="240" alt="更多应用"> |

| 系统资源 | 设备诊断 | 刷新失败诊断 |
| --- | --- | --- |
| <img src="screenshots/22-resources.png" width="240" alt="系统资源"> | <img src="screenshots/23-diagnostics.png" width="240" alt="设备诊断"> | <img src="screenshots/24-diagnostics-error.png" width="240" alt="刷新失败诊断"> |

| 系统设置 | 关于 EinkOS | 手机配网表单 |
| --- | --- | --- |
| <img src="screenshots/25-settings.png" width="240" alt="系统设置"> | <img src="screenshots/26-about.png" width="240" alt="关于 EinkOS"> | <img src="screenshots/27-phone-portal.png" width="240" alt="手机配网表单"> |

| 手机配网成功 | 手机配网失败 |  |
| --- | --- | --- |
| <img src="screenshots/28-phone-success.png" width="240" alt="手机配网成功"> | <img src="screenshots/29-phone-failure.png" width="240" alt="手机配网失败"> |  |

生成方法和来源哈希见 [截图说明](SCREENSHOTS.md)。新增页面必须同步扩充截图覆盖。
